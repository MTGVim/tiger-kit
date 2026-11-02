// Run with /usr/bin/osascript -l JavaScript. See provider-knowledge.md#macos-launch.
ObjC.import('AppKit');

function run(argv) {
    var result = {ok: false, pid: null, prior_frontmost_pid: null,
        final_frontmost_pid: null, self_activation_suppressed: false,
        activation_count: 0, late_activations: 0, error: null};
    var workspace = $.NSWorkspace.sharedWorkspace;
    var center = workspace.notificationCenter;
    var prior = workspace.frontmostApplication;
    var observer = null;
    var completed = false;
    var launched = null;
    var interrupted = false;
    var restoreFailed = false;
    var targetActive = false;
    var deadline = 0;
    var expectedBundlePath;
    var expectedExecutablePath;

    function present(value) { return value && !value.isNil(); }
    function pid(app) { return present(app) ? Number(app.processIdentifier) : null; }
    function path(url) {
        return present(url) ? ObjC.unwrap(url.URLByResolvingSymlinksInPath.path) : null;
    }
    function now() { return Number($.NSProcessInfo.processInfo.systemUptime); }
    function matches(app) {
        return present(app) && path(app.bundleURL) === expectedBundlePath &&
            path(app.executableURL) === expectedExecutablePath;
    }
    function observe(app) {
        if (interrupted || now() >= deadline) return;
        var activePid = pid(app);
        if (activePid === result.prior_frontmost_pid) {
            targetActive = false;
            return;
        }
        if (!matches(app) || (result.pid !== null && activePid !== result.pid)) {
            interrupted = true; // Preserve a user switch; never suppress arbitrary apps.
            result.error = 'frontmost_changed';
            return;
        }
        result.pid = activePid; // Notifications can precede the first process-list read.
        if (!targetActive) {
            result.activation_count++;
            if (completed) result.late_activations++;
        }
        targetActive = true;
        // A queued notification can outlive the activation it describes.
        var current = workspace.frontmostApplication;
        if (pid(current) !== activePid) {
            if (pid(current) !== result.prior_frontmost_pid) {
                interrupted = true;
                result.error = 'frontmost_changed';
            }
            return;
        }
        if (prior.isTerminated || !prior.activateWithOptions(0)) {
            restoreFailed = true;
            result.error = 'restore_failed';
        }
    }
    function refreshLaunch() {
        var apps = workspace.runningApplications;
        for (var j = 0; j < Number(apps.count); j++) {
            var candidate = apps.objectAtIndex(j);
            if (candidate.isTerminated || !matches(candidate)) continue;
            if (result.pid !== null && result.pid !== pid(candidate)) {
                result.error = 'launch_identity_ambiguous';
                return;
            }
            launched = candidate;
            result.pid = pid(candidate);
            if (candidate.isFinishedLaunching) completed = true;
        }
    }

    try {
        if (argv.length !== 2 || ['--bundle-id', '--path'].indexOf(argv[0]) < 0 || !argv[1]) {
            throw new Error('usage: --bundle-id ID | --path /absolute/App.app[/Contents/MacOS/executable]');
        }
        var url;
        var executableInput = null;
        if (argv[0] === '--bundle-id') {
            url = workspace.URLForApplicationWithBundleIdentifier(argv[1]);
        } else {
            if (argv[1][0] !== '/') throw new Error('absolute_path_required');
            var marker = argv[1].lastIndexOf('.app/Contents/MacOS/');
            var appPath = argv[1];
            if (marker >= 0) {
                appPath = argv[1].slice(0, marker + 4);
                executableInput = path($.NSURL.fileURLWithPath(argv[1]));
            }
            if (!/\.app$/.test(appPath)) throw new Error('raw_executable_requires_owned_app_wrapper');
            url = $.NSURL.fileURLWithPath(appPath);
        }
        if (!present(url)) throw new Error('app_not_found');
        var bundle = $.NSBundle.bundleWithURL(url);
        if (!present(bundle) || !present(bundle.executableURL) || !present(bundle.bundleIdentifier)) {
            throw new Error('invalid_app_bundle');
        }
        if (argv[0] === '--bundle-id' && ObjC.unwrap(bundle.bundleIdentifier) !== argv[1]) {
            throw new Error('bundle_identity_mismatch');
        }
        expectedBundlePath = path(url);
        expectedExecutablePath = path(bundle.executableURL);
        if (executableInput !== null && executableInput !== expectedExecutablePath) {
            throw new Error('executable_identity_mismatch');
        }
        if (!present(prior) || prior.isTerminated) throw new Error('prior_frontmost_unavailable');
        result.prior_frontmost_pid = pid(prior);
        var running = workspace.runningApplications;
        for (var i = 0; i < Number(running.count); i++) {
            var app = running.objectAtIndex(i);
            if (matches(app) || ObjC.unwrap(app.bundleIdentifier) === ObjC.unwrap(bundle.bundleIdentifier)) {
                throw new Error('app_already_running_reuse_existing_window');
            }
        }

        ObjC.registerSubclass({name: 'TigerKitBackgroundLaunchObserver', methods: {
            'didActivate:': {types: ['void', ['id']], implementation: function (note) {
                observe(note.userInfo.objectForKey($.NSWorkspaceApplicationKey));
            }}
        }});
        observer = $.TigerKitBackgroundLaunchObserver.alloc.init;
        deadline = now() + 5;
        center.addObserverSelectorNameObject(observer, 'didActivate:',
            $.NSWorkspaceDidActivateApplicationNotification, null);
        // Recheck after observer installation, before requesting any launch.
        if (pid(workspace.frontmostApplication) !== result.prior_frontmost_pid) {
            throw new Error('frontmost_changed_before_launch');
        }
        var configuration = $.NSWorkspaceOpenConfiguration.configuration;
        configuration.activates = false;
        configuration.addsToRecentItems = false;
        // AppKit invokes completion handlers on a concurrent queue. Keep all JS
        // state on this run loop instead; a missing ready signal times out.
        workspace.openApplicationAtURLConfigurationCompletionHandler(url, configuration, null);
        while (now() < deadline && !interrupted && !restoreFailed && !result.error) {
            $.NSRunLoop.currentRunLoop.runUntilDate($.NSDate.dateWithTimeIntervalSinceNow(0.025));
            refreshLaunch();
            observe(workspace.frontmostApplication);
        }
        if (!completed && !result.error) result.error = 'launch_timeout';
        if (launched !== null && launched.isTerminated && !result.error) result.error = 'target_terminated';
        result.final_frontmost_pid = pid(workspace.frontmostApplication);
        result.self_activation_suppressed = launched !== null && !launched.isTerminated &&
            !interrupted && !restoreFailed && !result.error &&
            result.final_frontmost_pid === result.prior_frontmost_pid;
        if (!result.error && !result.self_activation_suppressed) result.error = 'focus_not_preserved';
        if (!result.error && result.activation_count > 0) result.error = 'focus_changed_then_restored';
        result.ok = result.self_activation_suppressed && result.error === null;
    } catch (error) {
        result.error = String(error.message || error);
    } finally {
        if (observer !== null) center.removeObserver(observer);
        result.final_frontmost_pid = pid(workspace.frontmostApplication);
    }
    return JSON.stringify(result);
}
