// Execute the generated entry/lesson scripts; browser file-origin policy is a separate check.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict'),{pathToFileURL}=require('node:url');
const entry=process.argv[2],root=path.dirname(entry),html=fs.readFileSync(entry,'utf8');
const map=JSON.parse(html.match(/id="course-pages"[^>]*>(.*?)<\/script>/s)[1]);
const script=[...html.matchAll(/<script>(.*?)<\/script>/gs)].at(-1)[1],listeners={},frameListeners={},posts=[],loaded=[];
const frame={contentWindow:{postMessage:(...args)=>posts.push(args)},addEventListener:(kind,fn)=>frameListeners[kind]=fn};
let context;
const document={getElementById:id=>id==='course-frame'?frame:{textContent:JSON.stringify(map)},
 createElement:tag=>tag==='base'?{set href(value){this.outerHTML='<base href="'+value+'">';}}:{remove(){this.removed=true;}},
 head:{appendChild(node){loaded.push(node.src);vm.runInContext(fs.readFileSync(path.join(root,node.src),'utf8'),context);node.onload();}}};
const window={addEventListener:(kind,fn)=>listeners[kind]=fn};
context=vm.createContext({document,window,URL,location:{href:pathToFileURL(entry).href}});
vm.runInContext(script,context);
const ids=Object.keys(map),first=frame.srcdoc;
assert.equal(loaded.length,1);assert.match(first,/<base href="file:/);
assert(first.includes(new URL('lessons/',pathToFileURL(entry)).href));assert(!first.includes('data:audio/'));
listeners.message({source:{},data:{type:'course-lesson',id:ids[1]}});assert.equal(loaded.length,1);
listeners.message({source:frame.contentWindow,data:{type:'course-lesson',id:'../invalid'}});assert.equal(loaded.length,1);
listeners.message({source:frame.contentWindow,data:{type:'course-lesson',id:ids[1],ui:{tocTop:42}}});
assert.equal(loaded.length,2);assert.notEqual(frame.srcdoc,first);frameListeners.load();
assert.equal(posts.at(-1)[0].type,'course-enter');assert.equal(posts.at(-1)[0].ui.tocTop,42);
const current=frame.srcdoc;window.CourseLessonLoader(ids[0],'<head>stale');assert.equal(frame.srcdoc,current);
console.log('Generated classic-script loading, relative base, source-bound navigation and lesson entry: Pass');
