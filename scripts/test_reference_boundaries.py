from pathlib import Path
import tempfile,unittest,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
import shared_references as s
import check_token_budget as b

def captured_blocks():
 t=(ROOT/'skills/tk-prep/SKILL.md').read_text(); a=t.index('## Shared References'); z=t.index('\n<!--',a); consumer=t[a:z].strip()+'\n'
 t=(ROOT/'skills/tk-questioning/SKILL.md').read_text(); a=t.index('Use this reference-only skill'); z=t.index('## Conditional references',a); reference=t[a:z].rstrip()+'\n'
 return consumer,reference

class BoundaryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name).resolve(); self.skills=self.root/'skills'
  for target in s.SHARED_REFERENCES:
   p=self.root/target; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('# Reference\n')
  self.consumer,self.reference=captured_blocks()
  self.operation=self.skills/'tk-example/SKILL.md'; self.operation.parent.mkdir(parents=True); self.operation.write_text('---\nname: tk-example\nmetadata:\n  tigerkit:\n    kind: hybrid\n---\n\n'+self.consumer)
  self.library=self.skills/'tk-questioning/SKILL.md'; self.library.write_text('---\nname: tk-questioning\nmetadata:\n  tigerkit:\n    kind: hybrid\n    role: reference\n---\n\n'+self.reference)
 def tearDown(self): self.tmp.cleanup()
 def test_intact_reference_and_operation_guards_accepted(self):
  self.assertEqual(s.validate_shared_references(self.skills),[])
 def test_consumer_availability_stop_cannot_disappear(self):
  self.operation.write_text(self.operation.read_text().replace('no memory or unapproved installs','cached memory or automatic installs'))
  self.assertTrue(any('boundary' in x and 'tk-example' in x for x in s.validate_shared_references(self.skills)))
 def test_reference_invocation_cannot_acquire_authority(self):
  original=self.library.read_text(); changed=original.replace('not start that workflow or grant','start that workflow and grant'); self.assertNotEqual(original,changed); self.library.write_text(changed)
  self.assertTrue(any('boundary' in x and 'tk-questioning' in x for x in s.validate_shared_references(self.skills)))
 def test_duplicate_boundary_not_accepted(self):
  self.operation.write_text(self.operation.read_text()+'\n'+self.consumer)
  self.assertTrue(any('boundary' in x and 'tk-example' in x for x in s.validate_shared_references(self.skills)))
 def test_exact_inline_guards_count_toward_shared_load(self):
  self.assertGreater(b._shared_block_bytes(self.operation),0)
  self.assertGreater(b._shared_block_bytes(self.library),0)
 def test_only_canonical_guards_are_excluded_from_duplicate_detector(self):
  self.assertEqual(b._normalized_sentences(self.root),{})
  novel='Always require this distinct executable implementation decision before touching a selected deployment target.'
  for p in [self.operation,self.library]: p.write_text(p.read_text()+'\n'+novel+'\n')
  self.assertIn(novel[:-1].casefold(),b._normalized_sentences(self.root))

if __name__=='__main__': unittest.main()
