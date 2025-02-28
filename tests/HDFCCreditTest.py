import os
import unittest
from bank_statement_parser.banks.HdfcCredit import HsbcCredit


class TestHdfcCredit(unittest.TestCase):

    def setUp(self):
        self.kotak_debit = HsbcCredit()
        self.sample_csv_path = os.path.join(os.path.dirname(__file__),
                                            'resources/HDFC-Credit.csv')
        self.data = self.kotak_debit.getDataFrame(self.sample_csv_path)

    def test_numberOfRows(self):
        self.assertEqual(len(self.data), 8)

    def test_sumOfAmounts(self):
        print(self.data)
        total_amount = self.data['amount'].sum()
        expected_total = -2460.11  # Adjust for CR amounts
        self.assertAlmostEqual(total_amount, expected_total, places=2)


if __name__ == '__main__':
    unittest.main()
