import unittest
from types import SimpleNamespace
from utils.rag import answer_question, validate_answer,NOT_FOUND

class Store:
    def __init__(self,docs): self.docs=docs
    def similarity_search(self,q,k): return self.docs[:k]
class Chain:
    def __init__(self,value): self.value=value
    def invoke(self,params): return self.value

def doc(key):return SimpleNamespace(metadata={'id':key},page_content='시험용 근거')
class TestRAG(unittest.TestCase):
    def test_good(self):
        result=answer_question('배송?', 'A', Store([doc('F14')]),Chain('리뷰 2.57점 [F14]'))
        self.assertEqual(result['status'],'citations_in_retrieved_set')
    def test_fake_id_block(self):
        result=answer_question('배송?', 'A', Store([doc('F14')]),Chain('리뷰 2.57점 [F99]'))
        self.assertEqual(result['answer'],NOT_FOUND)
        self.assertTrue(result['status'].startswith('blocked_'))
    def test_no_citation_block(self):
        self.assertEqual(answer_question('문의', 'A', Store([doc('F14')]),Chain('리뷰 2.57점'))['answer'],NOT_FOUND)
    def test_malformed_id_block(self):
        self.assertFalse(validate_answer('사실 [F-14]',{'F14'},set('F'))['valid'])
    def test_beyond_channel(self):
        self.assertEqual(answer_question('모델', 'A',Store([doc('M09')]),Chain('특징 14개 [M09]'))['status'],'no_evidence')
        self.assertEqual(answer_question('모델', 'B',Store([doc('M09')]),Chain('특징 14개 [M09]'))['found_ids'],['M09'])
    def test_unknown(self):
        self.assertEqual(answer_question('2019 매출', 'C',Store([]),Chain('가짜'))['answer'],NOT_FOUND)
    def test_unsupported(self):
        with self.assertRaises(ValueError):answer_question('질문','D',Store([]),Chain('x'))
    def test_invalid_k(self):
        with self.assertRaises(ValueError):answer_question('질문','A',Store([]),Chain('x'),0)
    def test_not_found_explicit(self):
        self.assertEqual(answer_question('없는 질문','A',Store([doc('F14')]),Chain(NOT_FOUND))['answer'],NOT_FOUND)
    def test_fake_bracket(self):
        self.assertFalse(validate_answer('사실 [F14] [F99]',{'F14'},set('F'))['valid'])
    def test_disallowed(self):
        self.assertFalse(validate_answer('사실 [R06]',{'R06'},set('F'))['valid'])
    def test_missing_question(self):
        with self.assertRaises(ValueError):answer_question(' ','A',Store([]),Chain('x'))
if __name__ == '__main__': unittest.main()
