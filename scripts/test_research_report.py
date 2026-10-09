from pathlib import Path
import subprocess
import unittest


class ResearchReportTest(unittest.TestCase):
    def test_current_section_uses_visible_content_across_navigation_breakpoint(self):
        root = Path(__file__).resolve().parents[1]
        script = (root / 'skills/tk-explain/assets/html-theme.js').read_text()
        # Shared navigation must respect the sticky bar and select a nested section
        # at the reading edge rather than its larger enclosing parent.
        setup = r'''
const assert = require('node:assert/strict');
const listeners = {};
const fakeLinks=['overview','unknowns','conditions','frontier','sources'].map(id=>({hash:'#'+id,
 setAttribute(){this.current=true},removeAttribute(){this.current=false}}));
const fakeSections=[{id:'overview',top:-300,bottom:-100},
 {id:'unknowns',top:90,bottom:490},{id:'conditions',top:120,bottom:450},
 {id:'frontier',top:510,bottom:700},{id:'sources',top:730,bottom:890}]
 .map(s=>({...s,getBoundingClientRect(){return this},contains(other){return this.id==='unknowns'&&other.id==='conditions'}}));
let mobile=false;
const nav={querySelector:()=>null,querySelectorAll:()=>fakeLinks,addEventListener(){},contains(){return true}};
const bar={getBoundingClientRect:()=>({height:80,bottom:80})};
globalThis.location={hash:'#unknowns'};globalThis.innerHeight=900;
globalThis.getComputedStyle=()=>({position:mobile?'static':'sticky'});
globalThis.document={querySelector:s=>s==='.ht-doc-nav'?nav:s==='.ht-topbar'?bar:null,
 getElementById:id=>fakeSections.find(s=>s.id===id),documentElement:{style:{setProperty(){}}},addEventListener(){}};
globalThis.addEventListener=(event,fn)=>{listeners[event]=fn};globalThis.requestAnimationFrame=f=>f();
'''
        checks = r'''
listeners.scroll();assert.equal(fakeLinks.find(a=>a.current).hash,'#conditions');
mobile=true;listeners.resize();assert.equal(fakeLinks.find(a=>a.current).hash,'#unknowns');
// Moving the child to the mobile reading edge must activate it there too.
fakeSections.find(s=>s.id==='unknowns').top=-20;
fakeSections.find(s=>s.id==='conditions').top=20;
listeners.scroll();assert.equal(fakeLinks.find(a=>a.current).hash,'#conditions');
'''
        result = subprocess.run(['node', '-e', setup + script + checks],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
