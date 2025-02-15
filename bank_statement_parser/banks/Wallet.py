from datetime import date
from typing import List
import numpy as np
import pandas as pd
import bank_statement_parser.Bank as Bank
from bank_statement_parser.Transaction import Transaction

class Wallet(Bank):
    __id_ledger = 300

    def getTransactions(self, filename: str) -> List[Transaction]:
        transactions: List[Transaction] = []
        df = self.getDataFrame(filename)
        self.validateDataframe(df)

        for index, row in df.iterrows():
            _category = ""
            _duplicate = ""

            if row["category"].strip() != "":
                _category = row["category"].strip() + ": "

            if row["Seq"] > 1:
                _duplicate = " (" + str(row["Seq"]) + ") "

            created_date = row["date"]
            remarks = _category + row["note"].strip() + _duplicate
            amount = row["amount"]
            transaction = Transaction(
                id_ledger=self.__id_ledger,
                created_date=created_date,
                remarks=remarks,
                amount=amount,
            )
            transactions.append(transaction)

        return transactions

    def getDataFrame(self, filename: str) -> pd.DataFrame:
        xls = pd.ExcelFile(filename)
        df_full = xls.parse()
        #   remove last columns since not used
        del df_full[df_full.columns[-9]]
        df = df_full.copy()
        return df

    def validateDataframe(self, df):
        if "date" not in df.columns:
            raise ValueError("Date not found")

        if "note" not in df.columns:
            raise ValueError("note not found")

        if "category" not in df.columns:
            raise ValueError("category not found")

        if "amount" not in df.columns:
            raise ValueError("amount not found")

        df[["amount"]] = df[["amount"]].astype(float)
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")

        df["Seq"] = df.groupby(["date", "note", "category", "amount"]).cumcount().add(1)
