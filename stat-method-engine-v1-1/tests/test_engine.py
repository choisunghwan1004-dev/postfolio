import sys, csv, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import inspect_csv, choose_backend, advise, METHODS
from run_group import execute

class EngineTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/'sample.csv'
        self.path.write_text('day,site,pm10\n2022-01-01,A,10\n2022-01-02,A,20\n2022-01-03,B,30\n',encoding='utf-8')
    def tearDown(self):self.tmp.cleanup()
    def test_inspect_and_advice(self):
        a=inspect_csv(self.path); self.assertEqual(a['sampled_rows'],3);self.assertEqual(a['total_rows'],'not_counted')
        x=advise(a,'trend',8);self.assertIn('day',x['date_name_hints']);self.assertEqual(x['backend']['recommended'],'pandas')
    def test_backend_big(self):
        a=choose_backend(50*1024**3,8,'summary');self.assertEqual(a['recommended'],'Dask')
        b=choose_backend(50*1024**3,8,'summary',pandas_familiar=False);self.assertEqual(b['recommended'],'Polars')
    def test_distributed(self):
        self.assertEqual(choose_backend(1000,8,'deep_learning',distributed=True,gpu=True)['recommended'],'Ray')
        self.assertEqual(choose_backend(1000,8,'classification',distributed=True)['recommended'],'PySpark')
    def test_invalid(self):
        with self.assertRaises(ValueError):choose_backend(1000,0,'trend')
    def test_pandas_result(self):
        result=execute(self.path,'site','pm10')
        got={x['site']:x for x in result};self.assertEqual(got['A']['mean'],15);self.assertEqual(got['B']['count'],1)
    def test_catalog(self):self.assertGreaterEqual(len(METHODS),10)

if __name__=='__main__':unittest.main()
