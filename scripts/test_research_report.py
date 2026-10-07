from pathlib import Path
import subprocess
import unittest


class ResearchReportTest(unittest.TestCase):
    def test_current_section_uses_visible_content_across_navigation_breakpoint(self):
        template = Path(__file__).resolve().parents[1] / "skills/tk-research/assets/report.html"
        script = template.read_text().split("<script>", 1)[1].split("</script>", 1)[0]
        # The former 35%-height rule selected frontier below a largely visible hash target.
        for width in (390, 761):
            setup = """
const assert = (await import('node:assert/strict')).default;
const fakeLinks=['overview','unknowns','frontier','sources'].map(id=>({hash:'#'+id,
 setAttribute(){this.current=true},removeAttribute(){this.current=false}}));
const fakeSections=[{id:'overview',top:-300,bottom:-100},
 {id:'unknowns',top:90,bottom:290},{id:'frontier',top:310,bottom:500},
 {id:'sources',top:530,bottom:710}].map(s=>({...s,getBoundingClientRect(){return this}}));
globalThis.location={hash:'#unknowns'};globalThis.innerHeight=900;
globalThis.matchMedia=()=>({matches:WIDTH<=760});
globalThis.document={querySelectorAll:s=>s==='nav a'?fakeLinks:fakeSections,
 querySelector:()=>({getBoundingClientRect:()=>({bottom:80})})};
globalThis.addEventListener=()=>{};globalThis.requestAnimationFrame=f=>f();
""".replace("WIDTH", str(width))
            result = subprocess.run(["node", "--input-type=module", "-e",
                                     setup + script + "\ncurrent();assert.equal(links.find(a=>a.current).hash,'#unknowns');"],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
