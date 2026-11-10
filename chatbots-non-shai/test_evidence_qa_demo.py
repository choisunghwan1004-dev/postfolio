import unittest
from evidence_qa_demo import FALLBACK, answer, validate_citations


class GroundedChatbotTests(unittest.TestCase):
    def test_fact_access_all_channels(self):
        for channel in "ABC":
            response, ids = answer("늦게 도착한 주문의 리뷰 점수는?", channel)
            self.assertIn("[F14]", response)
            self.assertEqual(ids, ["F14"])

    def test_model_requires_b_or_c(self):
        self.assertEqual(answer("이탈 모델의 입력 특징은?", "A")[0], FALLBACK)
        for channel in "BC":
            self.assertIn("[M09]", answer("이탈 모델의 입력 특징은?", channel)[0])

    def test_policy_requires_c(self):
        self.assertEqual(answer("배송이 3일 지연되면 어떤 보상을 받아?", "A")[0], FALLBACK)
        self.assertEqual(answer("배송이 3일 지연되면 어떤 보상을 받아?", "B")[0], FALLBACK)
        self.assertIn("[R06]", answer("배송이 3일 지연되면 어떤 보상을 받아?", "C")[0])

    def test_unknown_question(self):
        for channel in "ABC":
            self.assertEqual(answer("2019년 매출은 얼마야?", channel)[0], FALLBACK)

    def test_fabricated_id_rejected(self):
        self.assertFalse(validate_citations("임의 사실 [F99]", ["F14"]))
        self.assertTrue(validate_citations("교재 예시 [F14]", ["F14"]))


if __name__ == "__main__":
    unittest.main()
