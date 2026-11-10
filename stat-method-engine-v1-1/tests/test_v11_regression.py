import csv
import json
import math
import os
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import inspect_csv, choose_backend, advise
from run_group import execute

class RegressionV11(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.base=Path(self.tmp.name)
        self.csv=self.base/'missing.csv'
        self.csv.write_text('site,pm10\nA,10\nA,abc\nA,\nB,20\n,30\n,\n',encoding='utf-8')
    def tearDown(self): self.tmp.cleanup()
    def test_null_and_non_numeric(self):
        out=execute(self.csv,'site','pm10')
        data={x['site']:x for x in out}
        self.assertEqual(data['A']['count'],1)
        self.assertEqual(data['A']['mean'],10)
        self.assertEqual(data['B']['count'],1)
        self.assertEqual(data[None]['count'],1)
        self.assertEqual(data[None]['mean'],30)
        json.dumps(out,allow_nan=False)
    def test_max_groups(self):
        with self.assertRaisesRegex(ValueError,'상한'):
            execute(self.csv,'site','pm10',max_groups=2)
    def test_bad_column(self):
        with self.assertRaisesRegex(ValueError,'열을 찾을 수 없습니다'):
            execute(self.csv,'city','pm10')
    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            execute(self.base/'nonexistent.csv','site','pm10')
    def test_cp949_read_and_no_mutation(self):
        cp=self.base/'korean.csv'
        cp.write_bytes('지역,미세먼지\n서울,12\n부산,24\n'.encode('cp949'))
        raw=cp.read_bytes()
        p=inspect_csv(cp,encoding='cp949')
        self.assertEqual(p['sampled_rows'],2)
        result=execute(cp,'지역','미세먼지',encoding='cp949')
        self.assertEqual({x['지역']:x['mean'] for x in result},{'서울':12,'부산':24})
        self.assertEqual(cp.read_bytes(),raw)
    def test_bad_csv_shape(self):
        path=self.base/'bad.csv'
        path.write_text('a,b\n1,2,3\n')
        with self.assertRaisesRegex(ValueError,'열 수 초과'):
            inspect_csv(path)
    def test_duplicate_header(self):
        path=self.base/'dupes.csv'
        path.write_text('a,a\n1,2\n')
        with self.assertRaisesRegex(ValueError,'중복'):
            inspect_csv(path)
    def test_invalid_ram_nan(self):
        with self.assertRaises(ValueError):choose_backend(100,math.nan,'summary')
        with self.assertRaises(ValueError):choose_backend(100,math.inf,'summary')
    def test_unknown_goal(self):
        with self.assertRaises(ValueError): choose_backend(100,8,'bogus')
    def test_optional_backend_not_installed(self):
        import importlib.util
        if importlib.util.find_spec('polars') is None:
            with self.assertRaises(ModuleNotFoundError):execute(self.csv,'site','pm10',backend='Polars')
        if importlib.util.find_spec('dask') is None:
            with self.assertRaises(ModuleNotFoundError):execute(self.csv,'site','pm10',backend='Dask')
    def test_reject_lossy_conversion(self):
        with self.assertRaisesRegex(ValueError,'UTF-8'):
            execute(self.csv,'site','pm10',backend='Polars',encoding='cp949')
    def test_actual_air_csv_profile(self):
        real=Path(os.environ.get('STAT_ENGINE_REAL_AIR_CSV', '/mnt/data/data_air_2022.csv'))
        if not real.exists():self.skipTest('실측 파일이 없음')
        p=inspect_csv(real,encoding='cp949')
        self.assertEqual(p['sampled_rows'],500)
        self.assertIn('day',[c['column'] for c in p['columns']])
        self.assertTrue(any(c['column']=='pm10' for c in p['columns']))
        self.assertEqual(p['inspection'],'sample_only; no full-file materialization')

if __name__=='__main__':unittest.main()
