import unittest

from prepare_reader_eval import reader_packet


class ReaderIsolationTests(unittest.TestCase):
    def test_hidden_context_and_answer_never_enter_packet(self):
        case = {
            "id": "missing-actor",
            "source_context": "The author knows the actor is Alice.",
            "expected": {"answer": "unknown"},
            "reader_input": {
                "document": "The owner deploys.",
                "purpose": "Operator instructions",
                "questions": ["Who deploys?"],
                "reasoning": "Alice is the owner.",
                "expected_answer": "Alice",
            },
        }
        self.assertEqual(reader_packet(case), {
            "document": "The owner deploys.",
            "purpose": "Operator instructions",
            "questions": ["Who deploys?"],
        })

    def test_missing_final_document_does_not_fall_back_to_source(self):
        with self.assertRaises(KeyError):
            reader_packet({"source": "Hidden source", "reader_input": {
                "purpose": "Guide", "questions": ["Who?"]}})
