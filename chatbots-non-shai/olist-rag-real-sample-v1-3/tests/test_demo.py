import unittest
from demo import compare, UNKNOWN
class DemoTests(unittest.TestCase):
    def test_15_rows(self):self.assertEqual(len(compare()),15)
    def test_unsupported(self):self.assertEqual(sum(r['answer']==UNKNOWN for r in compare()),6)
    def test_out_of_channel(self):
        self.assertEqual(next(r for r in compare() if r['question'].startswith('3일') and r['channel']=='B')['answer'],UNKNOWN)
    def test_reference_present(self):
        self.assertIn('[R06]',next(r for r in compare() if r['question'].startswith('3일') and r['channel']=='C')['answer'])
if __name__=='__main__':unittest.main()
