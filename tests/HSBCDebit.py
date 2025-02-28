import os
import unittest
from bank_statement_parser.banks.HsbcDebit import HsbcDebit


class TestHsbcDebit(unittest.TestCase):

    def setUp(self):
        self.kotak_debit = HsbcDebit()
        self.sample_csv_path = os.path.join(os.path.dirname(__file__),
                                            'resources/HSBC-Debit.xls')
        self.data = self.kotak_debit.getDataFrame(self.sample_csv_path)

    def test_numberOfRows(self):
        self.assertEqual(len(self.data), 3)

    def test_sumOfAmounts(self):
        print(self.data)
        total_amount = self.data['amount'].sum()
        expected_total = 121526.09  # Adjust for CR amounts
        self.assertAlmostEqual(total_amount, expected_total, places=2)


if __name__ == '__main__':
    unittest.main()
