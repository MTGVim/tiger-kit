"""Exercise durable paths with real Git worktrees and isolated settings."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1];SPEC=importlib.util.spec_from_file_location('durable_artifacts',ROOT/'skills/tk-explain/scripts/durable_artifacts.py')
module=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(module)

class DurableArtifactsTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();self.config=self.root/'config';self.repo=self.root/'projects'/'same';self.repo.mkdir(parents=True)
        self.env=patch.dict(os.environ,{'XDG_CONFIG_HOME':str(self.config)});self.env.start()
        self.git(self.repo,'init','-q');self.git(self.repo,'config','user.name','Test');self.git(self.repo,'config','user.email','test@example.invalid')
        (self.repo/'tracked').write_text('first');self.git(self.repo,'add','tracked');self.git(self.repo,'commit','-qm','initial')
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def git(self,repo,*args):return subprocess.run(['git','-C',str(repo),*args],check=True,text=True,capture_output=True).stdout.strip()
    def test_missing_choice_fallback_and_noninteractive_does_not_write(self):
        self.assertEqual(module.status()['status'],'missing')
        path=module.resolve(self.repo,'explanations','topic')
        self.assertEqual(path['source'],'repository');self.assertEqual(Path(path['path']),self.repo/'.tigerkit/explanations/topic.html')
        self.assertFalse(self.config.exists());self.assertFalse((self.repo/'.tigerkit').exists())
    def test_each_package_helper_exposes_status_without_writing(self):
        for owner in ('tk-explain',):
            with self.subTest(owner=owner):
                result=subprocess.run(['python3',str(ROOT/'skills'/owner/'scripts/durable_artifacts.py'),'status'],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr);self.assertTrue(json.loads(result.stdout)['needs_choice'])
        self.assertFalse(self.config.exists())

    def test_disable_preserves_theme_and_does_not_reask(self):
        settings=self.config/'tigerkit/settings.json';settings.parent.mkdir(parents=True);settings.write_text('{"html":{"theme":"dark"},"other":7}')
        self.assertEqual(module.choose(disable=True,repo=self.repo)['status'],'disabled')
        self.assertEqual(json.loads(settings.read_text()),{'html':{'theme':'dark'},'other':7,'artifacts':{'durableRoot':None}})
        self.assertFalse(module.status()['needs_choice']);self.assertEqual(module.resolve(self.repo,'study','cache')['source'],'repository')
        with self.assertRaises(ValueError):module.choose(disable=True,repo=self.repo)
    def test_recorded_root_preserves_existing_settings_and_unicode_topic(self):
        settings=self.config/'tigerkit/settings.json';settings.parent.mkdir(parents=True)
        settings.write_text('{"html":{"theme":"light"},"other":{"value":3}}')
        module.choose(str(self.root/'durable'),repo=self.repo)
        self.assertFalse(module.status()['needs_choice'])
        data=json.loads(settings.read_text());self.assertEqual(data['html']['theme'],'light');self.assertEqual(data['other'],{'value':3})
        home=Path(module.resolve(self.repo,'study','한국어',create=True)['path'])
        self.assertEqual(home.name,'한국어');self.assertEqual(module.resume_homes(self.repo,'한국어')['homes'],[str(home)])

    def test_worktrees_share_key_and_durable_survives_removal(self):
        wt=self.root/'worktree';self.git(self.repo,'worktree','add','-qb','second',str(wt))
        durable=self.root/'private';module.choose(str(durable),repo=self.repo)
        excludes=self.root/'excludes';excludes.write_text('/.tigerkit/\n');self.git(self.repo,'config','core.excludesFile',str(excludes))
        scratch=wt/'.tigerkit/tmp';scratch.mkdir(parents=True);(scratch/'ignored').write_text('local')
        one=module.resolve(wt,'explanations','topic',create=True);target=Path(one['path'])
        package=ROOT/'skills/tk-explain'
        build=subprocess.run(['python3',str(package/'scripts/build_html.py'),'--body',str(package/'assets/reader-example.html'),'--title','Durable example','--output',str(target),'--theme','system'],text=True,capture_output=True)
        self.assertEqual(build.returncode,0,build.stderr);original=target.read_bytes();self.assertIn(b'<!doctype html>',original);self.assertNotIn(b'<script src=',original)
        two=module.resolve(self.repo,'explanations','topic',create=True)
        self.assertEqual(one['repo_key'],two['repo_key']);self.assertEqual(Path(two['path']).name,'topic-2.html')
        self.assertEqual(stat.S_IMODE(durable.stat().st_mode),0o700)
        self.assertFalse((wt/'.gitignore').exists());self.git(self.repo,'worktree','remove',str(wt));self.assertEqual(target.read_bytes(),original)
    def test_same_named_repositories_are_distinct(self):
        other=self.root/'other'/'same';other.mkdir(parents=True);self.git(other,'init','-q')
        module.choose(str(self.root/'durable'),repo=self.repo)
        a=module.resolve(self.repo,'explanations','topic');b=module.resolve(other,'explanations','topic')
        self.assertNotEqual(a['repo_key'],b['repo_key']);self.assertNotEqual(a['path'],b['path'])
    def test_explicit_path_wins_and_does_not_create_durable_root(self):
        durable=self.root/'durable';module.choose(str(durable),repo=self.repo)
        result=module.resolve(self.repo,'explanations',None,explicit='reports/custom.html',create=True)
        self.assertEqual(result['source'],'explicit');self.assertEqual(result['path'],str(self.repo/'reports/custom.html'));self.assertFalse(durable.exists())
        cli=subprocess.run(['python3',str(ROOT/'skills/tk-explain/scripts/durable_artifacts.py'),'resolve','--repo',str(self.repo),'--kind','explanations','--explicit','reports/custom.html'],capture_output=True,text=True)
        self.assertEqual(cli.returncode,0,cli.stderr);self.assertEqual(json.loads(cli.stdout)['path'],result['path'])
    def test_resume_finds_durable_and_both_existing_local_homes(self):
        module.choose(str(self.root/'durable'),repo=self.repo)
        durable=Path(module.resolve(self.repo,'study','cache',create=True)['path'])
        local=self.repo/'.tigerkit/teach/cache';legacy=self.repo/'.tigerkit/study/cache';local.mkdir(parents=True);legacy.mkdir(parents=True)
        self.assertEqual(set(module.resume_homes(self.repo,'cache')['homes']),{str(durable),str(local),str(legacy)})
        self.assertEqual(set(module.resume_homes(self.repo)['homes']),{str(durable),str(local),str(legacy)})
        with self.assertRaises(ValueError):module.resume_homes(self.repo,'../escape')
    def test_invalid_settings_and_symlink_paths_are_never_rewritten(self):
        settings=self.config/'tigerkit/settings.json';settings.parent.mkdir(parents=True);settings.write_text('{invalid')
        result=module.resolve(self.repo,'explanations','topic');self.assertEqual(result['settings']['status'],'invalid');self.assertEqual(settings.read_text(),'{invalid')
        target=self.root/'real';target.mkdir();link=self.root/'link';link.symlink_to(target,target_is_directory=True)
        settings.write_text(json.dumps({'artifacts':{'durableRoot':str(link)}}));original=settings.read_bytes()
        self.assertEqual(module.status()['status'],'invalid');self.assertEqual(settings.read_bytes(),original)
        with self.assertRaises(ValueError):module.resolve(self.repo,'explanations','topic',explicit=str(link/'file.html'))
        with self.assertRaises(ValueError):module.resolve(self.repo,'explanations','topic',explicit=str(link/'..'/'file.html'))
    def test_invalid_configured_root_falls_back_without_modifying_settings(self):
        settings=self.config/'tigerkit/settings.json';settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({'artifacts':{'durableRoot':str(self.repo/'inside')}}));before=settings.read_bytes()
        result=module.resolve(self.repo,'explanations','topic',create=True)
        self.assertEqual(result['source'],'repository');self.assertEqual(result['settings']['status'],'invalid')
        self.assertEqual(settings.read_bytes(),before);self.assertFalse((self.repo/'inside').exists());self.assertFalse((self.repo/'.tigerkit').exists())
        explicit=module.resolve(self.repo,'explanations','topic',explicit='report.html')
        self.assertEqual(explicit['source'],'explicit');self.assertEqual(explicit['path'],str(self.repo/'report.html'))

    def test_root_inside_worktree_rejected_and_no_creation(self):
        with self.assertRaises(ValueError):module.choose(str(self.repo/'output'),repo=self.repo)
        self.assertFalse((self.repo/'output').exists());self.assertFalse(self.config.exists())
    def test_existing_study_gets_new_suffix_without_modifying_old_home(self):
        module.choose(str(self.root/'durable'),repo=self.repo)
        old=Path(module.resolve(self.repo,'study','topic',create=True)['path']);(old/'lesson.html').write_text('original')
        new=Path(module.resolve(self.repo,'study','topic',create=True)['path'])
        self.assertEqual(new.name,'topic-2');self.assertEqual((old/'lesson.html').read_text(),'original')

if __name__=='__main__':unittest.main()
