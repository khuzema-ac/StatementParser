
from typing import List
import pandas as pd
import bank_statement_parser.Bank as Bank
from bank_statement_parser.Transaction import Transaction


class HsbcCredit(Bank):
    __id_bank = "HSBC-CREDIT"

    def getTransactions(self, filename: str) -> List[Transaction]:
        transactions: List[Transaction] = []

        df = self.getData(filename)
        self.validateDataframe(df)

        for index, row in df.iterrows():
            _duplicate = ""

            if row["Seq"] > 1:
                _duplicate = " (" + str(row["Seq"]) + ") "

            created_date = row["Date"]
            remarks = row["Transaction Details"].strip() + _duplicate

            _multiplier = -1

            amount = row["Amount"] * _multiplier
            transaction = Transaction(
                bank=self.__id_bank,
                created_date=created_date,
                remarks=remarks,
                amount=amount
            )
            transactions.append(transaction)

        return transactions

    def getData(self, filename: str) -> pd.DataFrame:
        column_names = ["Date", "Transaction Details", "Amount"]
        df_full = self.load_bank_statement(filename,
                                           skip_rows=0,
                                           hasHeader=False)
        #  remane columns
        print(df_full)
        df_full.columns = column_names
        return df_full

    def validateDataframe(self, df):
        if "Date" not in df.columns:
            raise ValueError("Date not found")

        if "Transaction Details" not in df.columns:
            raise ValueError("Transaction Details not found")

        if "Amount" not in df.columns:
            raise ValueError("Amount(in Rs) not found")

        # Ensure "Amount(in Rs)" is a string before replacing commas
        if df["Amount"].dtype != 'object':
            df["Amount"] = df["Amount"].astype(str)
        df["Amount"] = df["Amount"].str.replace(",", "")
        df[["Amount"]] = df[["Amount"]].astype(float)
        df["Date"] = df["Date"].apply(self.parse_date)

        # to handle duplicate on same day
        df["Seq"] = (
            df.groupby(["Date", "Transaction Details", "Amount"])
            .cumcount()
            .add(1)
        )
