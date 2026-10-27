"""Verify source-bound change model failures, not semantic correctness."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'skills/tk-explain-diff'
spec = importlib.util.spec_from_file_location('change_model', PACKAGE / 'scripts/change_model.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

class ChangeModelTest(unittest.TestCase):
    def setUp(self):
        self.model=json.loads((PACKAGE/'assets/change-example.json').read_text())
        self.sources=json.loads((PACKAGE/'assets/change-example.sources.json').read_text())
    def errors(self, model=None, sources=None):
        return module.validate_model(self.model if model is None else model, self.sources if sources is None else sources)
    def assertCode(self, code):
        errors=self.errors(); self.assertIn(code, [e['code'] for e in errors], errors)
        self.assertTrue(all(e['path'] and e['message'] for e in errors))
    def test_example_is_valid_and_not_mutated(self):
        before=copy.deepcopy((self.model,self.sources));self.assertEqual(self.errors(),[]);self.assertEqual((self.model,self.sources),before)
    def test_primary_coverage_and_secondary_reason(self):
        self.model['groups'][0]['unit_ids'].remove('u-banner');self.assertCode('ORPHAN_UNIT')
        self.model['units'][1]['disposition']='secondary';self.assertCode('REASON')
        self.model['units'][1]['reason']='not needed in this view';self.assertEqual(self.errors(),[])
    def test_incomplete_inventory_requires_limitation(self):
        self.model['inventory_complete']=False;self.assertCode('LIMITATION')
        self.model['inventory_limit']='one file unavailable';self.assertEqual(self.errors(),[])
    def test_duplicate_unknown_and_order_are_rejected(self):
        self.model['evidence'].append(copy.deepcopy(self.model['evidence'][0]));self.assertCode('DUPLICATE_ID')
        self.model['groups'][0]['depends_on']=['expiry-boundary'];self.assertCode('DEPENDENCY_ORDER')
        self.model['groups'][0]['evidence_ids'].append('missing');self.assertCode('UNKNOWN_EVIDENCE')
        self.model['groups'][0]['extra']=1;self.assertCode('UNKNOWN_KEY')
    def test_digest_range_and_endpoint_mismatch(self):
        self.model['evidence'][0]['sha256']='bad';self.assertCode('DIGEST')
        self.model['evidence'][0]['start']=0;self.assertCode('RANGE')
        self.model['units'][0]['before']=['e-policy-head'];self.assertCode('ENDPOINT')
    def test_missing_source_and_unsafe_path(self):
        self.sources['files'].pop(0);self.assertCode('MISSING_SOURCE')
        self.model['evidence'][0]['path']='../escape';self.assertCode('PATH')
    def test_empty_and_unavailable_source(self):
        source=self.sources['files'][0];e=self.model['evidence'][0];source['text']='';e.update(start=None,end=None,sha256=hashlib.sha256(b'').hexdigest());self.assertEqual(self.errors(),[])
        e.update(availability='unavailable',sha256=None,reason='not accessible');self.model['groups'][0]['before']['basis']='inference';self.model['groups'][0]['before']['limitation']='source unavailable';self.model['groups'][1]['before']['basis']='inference';self.model['groups'][1]['before']['limitation']='source unavailable';self.assertEqual(self.errors(),[])
        e['reason']=None;self.assertCode('REASON')
    def test_source_inference_and_invalid_structure(self):
        c=self.model['groups'][0]['before'];c['basis']='inference';self.assertCode('LIMITATION')
        c['limitation']='inferred';self.assertEqual(self.errors(),[])
        self.assertTrue(self.errors(model=[]));self.assertTrue(self.errors(sources=[]))
    def test_graph_reference_and_presence(self):
        self.model['graph']={'nodes':[{'id':'a','label':'A','delta':'unchanged','versions':['base','head'],'evidence_ids':[]},{'id':'b','label':'B','delta':'added','versions':['head'],'evidence_ids':[]}],
          'edges':[{'id':'ab','from':'a','to':'b','label':'uses','delta':'added','versions':['head'],'basis':'inference','evidence_ids':[],'limitation':'inferred'}],
          'flows':[{'id':'f','title':'Flow','group_id':'ttl-duration','version':'head','steps':[{'id':'s','edge_id':'ab','explanation':'A to B'}]}]}
        self.assertEqual(self.errors(),[])
        self.model['graph']['edges'][0]['evidence_ids']=['e-policy-base'];self.assertCode('PRESENCE')
        self.model['graph']['edges'][0]['evidence_ids']=[]
        self.model['graph']['flows'][0]['version']='base';self.assertCode('PRESENCE')
        self.model['graph']['edges'][0]['to']='missing';self.assertCode('UNKNOWN_NODE')
    def test_metadata_changes_and_workspace_snapshots(self):
        self.model['snapshot'].update(comparison='workspace', from_='ignored')
        del self.model['snapshot']['from_']
        self.model['snapshot']['versions']['head']={'kind':'worktree','id':'a'*64}
        for f in self.sources['files']:
            if f['path']=='src/banner.ts': f['kind']='metadata'; f['text']='rename metadata\n'
        for e in self.model['evidence']:
            if e['path']=='src/banner.ts':
                e.update(kind='metadata',start=1,end=1,sha256=hashlib.sha256(b'rename metadata\n').hexdigest())
        self.model['units'][1]['kind']='rename'
        self.assertEqual(self.errors(),[])
        self.model['snapshot']['versions']['head']['id']='not-a-hash';self.assertCode('FINGERPRINT')
    def test_nontext_changes_and_deletion_use_metadata_or_limitations(self):
        for kind in ('binary','mode','submodule','rename'):
            with self.subTest(kind=kind):
                model=copy.deepcopy(self.model); sources=copy.deepcopy(self.sources)
                model['units'][1]['kind']=kind
                for f in sources['files']:
                    if f['path']=='src/banner.ts': f.update(kind='metadata',text=kind+' change\n')
                for e in model['evidence']:
                    if e['path']=='src/banner.ts': e.update(kind='metadata',start=1,end=1,sha256=hashlib.sha256((kind+' change\n').encode()).hexdigest())
                self.assertEqual(self.errors(model,sources),[])
        model=copy.deepcopy(self.model)
        model['units'][1]['after']=[]
        after=model['groups'][0]['after'];after.update(basis='inference',evidence=['e-policy-head'],limitation='deleted source is unavailable')
        self.assertEqual(self.errors(model),[])

    def test_real_commit_ids_and_distinct_workspace_versions(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            def git(*args):
                return subprocess.run(['git','-C',str(root),*args],check=True,text=True,capture_output=True).stdout.strip()
            git('init','-q');git('config','user.name','Test');git('config','user.email','test@example.invalid')
            f=root/'sample';f.write_text('before\n');git('add','sample');git('commit','-qm','before');before=git('rev-parse','HEAD')
            f.write_text('after\n');git('commit','-qam','after');after=git('rev-parse','HEAD')
            self.model['snapshot'].update(comparison='range',versions={'base':{'kind':'commit','id':before},'head':{'kind':'commit','id':after}})
            self.assertEqual(self.errors(),[])
            self.model['snapshot']['versions']['index']={'kind':'index','id':'a'*64}
            self.model['snapshot']['versions']['worktree']={'kind':'worktree','id':'b'*64}
            self.assertEqual(self.errors(),[])
            self.model['snapshot']['versions']['head']['id']='short';self.assertCode('FINGERPRINT')

    def test_same_path_remains_distinct_across_index_and_worktree(self):
        for name,text in (('index','staged\n'),('worktree','unstaged\n')):
            self.model['snapshot']['versions'][name]={'kind':name,'id':('a' if name=='index' else 'b')*64}
            self.sources['files'].append({'kind':'text','version':name,'path':'src/policy.ts','text':text})
            self.model['evidence'].append({'id':'e-'+name,'kind':'text','version':name,'path':'src/policy.ts',
                'start':1,'end':1,'availability':'available','sha256':hashlib.sha256(text.encode()).hexdigest(),'reason':None})
        self.assertEqual(self.errors(),[])
        self.sources['files'][-1]['text']='different\n';self.assertCode('DIGEST')

    def test_non_text_values_do_not_crash_or_execute(self):
        self.model['groups'][0]['depends_on']=[{'untrusted':'rm -rf /'}]
        self.assertCode('ID')
        self.model['evidence'][0]['path']='https:host/path';self.assertCode('PATH')

    def test_cli_reports_scope_and_does_not_execute_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); sentinel=root/'executed'; model=root/'model.json'; sources=root/'sources.json'
            payload=f"__import__('pathlib').Path({str(sentinel)!r}).write_text('executed')\n</script> 한글 %\n"
            self.sources['files'][0]['text']=payload
            self.model['evidence'][0].update(sha256=hashlib.sha256(payload.encode()).hexdigest(),start=1,end=2)
            model.write_text(json.dumps(self.model,ensure_ascii=False)); sources.write_text(json.dumps(self.sources,ensure_ascii=False))
            cmd=[sys.executable,str(PACKAGE/'scripts/change_model.py'),'--model',str(model),'--sources',str(sources)]
            result=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('Git, completeness and interpretation were not verified',result.stdout)
            self.assertFalse(sentinel.exists())
            self.assertEqual(json.loads(sources.read_text())['files'][0]['text'],payload)

if __name__=='__main__': unittest.main()
