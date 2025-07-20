import pandas as pd
import statement_parser.Bank as Bank
from statement_parser.Transaction import Transaction


class Wallet(Bank):
    __id_bank = "WALLET"

    def getTransactions(self, filename: str) -> list[Transaction]:
        transactions: list[Transaction] = []
        df = self.getData(filename)
        self.validateDataframe(df)

        for index, row in df.iterrows():
            _category = ""
            _duplicate = ""

            if row["category"].strip() != "":
                _category = row["category"].strip() + ": "

            if row["Seq"] > 1:
                _duplicate = " (" + str(row["Seq"]) + ") "

            timestamp = pd.Timestamp(row["date"])
            created_date = timestamp.to_pydatetime()
            remarks = _category + row["note"].strip() + _duplicate
            amount = row["amount"]
            transaction = Transaction(
                bank=self.__id_bank,
                created_date=created_date,
                remarks=remarks,
                amount=amount,
            )
            transactions.append(transaction)

        return transactions

    def getData(self, filename: str) -> pd.DataFrame:
        skip_rows = self.get_transaction_start(filename, ["date", "note"])
        df_full = self.load_bank_statement(filename, skip_rows=skip_rows)
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

        df["Seq"] = (
            df.groupby(["date", "note", "category", "amount"])
            .cumcount()
            .add(1)
            )
