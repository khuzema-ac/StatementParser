import os
import unittest
from statement_parser.banks.IciciDebit import IciciDebit


class TestIciciDebit(unittest.TestCase):

    def setUp(self):
        self.bank = IciciDebit()
        self.sample_csv_path = os.path.join(os.path.dirname(__file__),
                                            'resources/ICICI-Debit.xls')
        self.data = self.bank.getDataFrame(self.sample_csv_path)

    def test_numberOfRows(self):
        self.assertEqual(len(self.data), 9)

    def test_sumOfAmounts(self):
        print(self.data)
        total_amount = self.data['amount'].sum()
        expected_total = 12293.21  # Adjust for CR amounts
        self.assertAlmostEqual(total_amount, expected_total, places=2)


if __name__ == '__main__':
    unittest.main()
