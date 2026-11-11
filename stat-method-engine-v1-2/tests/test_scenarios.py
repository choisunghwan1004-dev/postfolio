import csv,hashlib,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scenario_engine import Scenario,run_scenario,compare_scenarios,recommend_methods

class Scenarios(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)/'sample.csv'
  self.p.write_text('location,day,pm10,pm25\nA,2022-01-01,10,2\nA,2022-01-02,20,4\nA,2022-01-03,30,6\nB,2022-01-01,40,8\nB,2022-01-02,50,10\n',encoding='utf8')
 def tearDown(self):self.tmp.cleanup()
 def test_summary_changes_with_range(self):
  a=run_scenario(self.p,Scenario())['result']['mean']
  b=run_scenario(self.p,Scenario(min_value=30))['result']['mean']
  self.assertEqual(a,30);self.assertEqual(b,40)
 def test_group(self):
  r=run_scenario(self.p,Scenario(method='group_compare',group_col='location'))['result']['groups']
  self.assertEqual(len(r),2);self.assertEqual(r[0]['mean'],20);self.assertEqual(r[1]['mean'],45)
 def test_date_and_filter(self):
  r=run_scenario(self.p,Scenario(filter_col='location',filter_equals='A',date_col='day',start_date='2022-01-02'))
  self.assertEqual(r['result']['mean'],25)
 def test_timeseries_change_window(self):
  a=run_scenario(self.p,Scenario(method='timeseries',date_col='day',window=2))['result']['series']
  b=run_scenario(self.p,Scenario(method='timeseries',date_col='day',window=3))['result']['series']
  self.assertIsNotNone(a[1]['moving_average']);self.assertIsNone(b[1]['moving_average'])
 def test_correlation(self):
  r=run_scenario(self.p,Scenario(method='correlation',second_col='pm25'))['result'];self.assertAlmostEqual(r['pearson'],1)
 def test_reject_same_columns(self):
  with self.assertRaisesRegex(ValueError,'서로 다른'):run_scenario(self.p,Scenario(method='correlation',second_col='pm10'))
 def test_reject_no_variation(self):
  const=Path(self.tmp.name)/'constant.csv'
  const.write_text('location,day,pm10,pm25\nA,2022-01-01,10,5\nA,2022-01-02,20,5\nA,2022-01-03,30,5\n')
  with self.assertRaisesRegex(ValueError,'변화'):run_scenario(const,Scenario(method='correlation',second_col='pm25'))
 def test_reject_date_required(self):
  with self.assertRaisesRegex(ValueError,'열 없음'):run_scenario(self.p,Scenario(method='timeseries'))
 def test_reject_bad_dates(self):
  with self.assertRaisesRegex(ValueError,'늦음'):run_scenario(self.p,Scenario(start_date='2023-01-01',end_date='2022-01-01',date_col='day'))
 def test_compare_fail_and_success(self):
  result=compare_scenarios(self.p,[Scenario(),Scenario(method='correlation')])
  self.assertEqual(result['scenarios'][0]['status'],'executed_locally');self.assertEqual(result['scenarios'][1]['status'],'blocked')
 def test_original_unchanged(self):
  x=hashlib.sha256(self.p.read_bytes()).digest();run_scenario(self.p,Scenario());self.assertEqual(hashlib.sha256(self.p.read_bytes()).digest(),x)
 def test_candidate_conditions(self):
  opts=recommend_methods([{'column':'pm10','inferred_type':'numeric','date_name_hint':False}],goal='relationship')
  corr=[x for x in opts if x['id']=='correlation'][0];self.assertEqual(corr['status'],'needs_conditions')
 def test_empty_group_error(self):
  with self.assertRaisesRegex(ValueError,'관측이 없음'):run_scenario(self.p,Scenario(method='group_compare',group_col='location',filter_col='location',filter_equals='Z'))
 def test_large_guard(self):
  with self.assertRaisesRegex(ValueError,'64MiB'):run_scenario(self.p,Scenario(),max_csv_bytes=1)

if __name__=='__main__':unittest.main()
