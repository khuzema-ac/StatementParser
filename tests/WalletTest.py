import os
import unittest
from bank_statement_parser.banks.Wallet import Wallet


class TestWallet(unittest.TestCase):

    def setUp(self):
        self.bank = Wallet()
        self.sample_csv_path = os.path.join(os.path.dirname(__file__),
                                            'resources/wallet.xls')
        self.data = self.bank.getDataFrame(self.sample_csv_path)

    def test_numberOfRows(self):
        self.assertEqual(len(self.data), 37)

    def test_sumOfAmounts(self):
        print(self.data)
        total_amount = self.data['amount'].sum()
        expected_total = -2989  # Adjust for CR amounts
        self.assertAlmostEqual(total_amount, expected_total, places=2)


if __name__ == '__main__':
    unittest.main()
