import os
import unittest
from datetime import datetime
import pandas as pd
from bank_statement_parser.banks.IciciCredit import IciciCredit
from bank_statement_parser.Transaction import Transaction

class TestIciciCredit(unittest.TestCase):

    def setUp(self):
        self.icici_credit = IciciCredit()
        self.sample_csv_path = os.path.join(os.path.dirname(__file__), 'resources/ICICI-Credit.csv')
        self.data = self.icici_credit.getDataFrame(self.sample_csv_path)

    def test_numberOfRows(self):
        self.assertEqual(len(self.data),10)

    def test_sumOfAmounts(self):
        print(self.data)
        total_amount = self.data['amount'].sum()
        expected_total = -8542.88  # Adjust for CR amounts
        self.assertAlmostEqual(total_amount, expected_total, places=2)


if __name__ == '__main__':
    unittest.main()