import os
import unittest
from datetime import datetime
import pandas as pd
from bank_statement_parser.banks.IciciDebit import IciciDebit
from bank_statement_parser.Transaction import Transaction

class TestIciciDebit(unittest.TestCase):

    def setUp(self):
        self.icici_debit = IciciDebit()
        self.sample_csv_path = os.path.join(os.path.dirname(__file__), 'resources/ICICI-Debit.xls')
        self.data = self.icici_debit.getDataFrame(self.sample_csv_path)

    def test_numberOfRows(self):
        self.assertEqual(len(self.data),9)

    def test_sumOfAmounts(self):
        print(self.data)
        total_amount = self.data['amount'].sum()
        expected_total = 12293.21  # Adjust for CR amounts
        self.assertAlmostEqual(total_amount, expected_total, places=2)


if __name__ == '__main__':
    unittest.main()