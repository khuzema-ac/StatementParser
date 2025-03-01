import os
import unittest
from bank_statement_parser.banks.KotakDebit import KotakDebit


class TestKotakDebit(unittest.TestCase):

    def setUp(self):
        self.bank = KotakDebit()
        self.sample_csv_path = os.path.join(os.path.dirname(__file__),
                                            'resources/Kotak-Debit.csv')
        self.data = self.bank.getDataFrame(self.sample_csv_path)

    def test_numberOfRows(self):
        self.assertEqual(len(self.data), 9)

    def test_sumOfAmounts(self):
        print(self.data)
        total_amount = self.data['amount'].sum()
        expected_total = -34609.46  # Adjust for CR amounts
        self.assertAlmostEqual(total_amount, expected_total, places=2)


if __name__ == '__main__':
    unittest.main()
