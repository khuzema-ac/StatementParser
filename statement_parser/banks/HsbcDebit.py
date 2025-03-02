
import pandas as pd
import statement_parser.Bank as Bank
from statement_parser.Transaction import Transaction


class HsbcDebit(Bank):
    __id_bank = "HSBC-DEBIT"

    def getTransactions(self, filename: str) -> list[Transaction]:
        transactions: list[Transaction] = []

        df = self.getData(filename)
        self.validateDataframe(df)

        for index, row in df.iterrows():
            _duplicate = ""

            if row["Seq"] > 1:
                _duplicate = " (" + str(row["Seq"]) + ") "

            created_date = row["Date"]
            remarks = row["Transaction Details"].strip() + _duplicate
            amount = (row["Deposits"] -
                      row["Withdrawals"])

            transaction = Transaction(
                bank=self.__id_bank,
                created_date=created_date,
                remarks=remarks,
                amount=amount
            )
            transactions.append(transaction)

        return transactions

    def getData(self, filename: str) -> pd.DataFrame:
        skip_rows = self.get_transaction_start(filename,
                                               ["date", "transaction details"])
        df_full = self.load_bank_statement(filename, skip_rows=skip_rows)
        # filter out empty rows
        df_filtered = df_full[df_full.iloc[:, 2].notna()]
        df_filtered.columns = df_filtered.columns.str.strip()
        df = df_filtered.copy()
        return df

    def validateDataframe(self, df):
        if "Date" not in df.columns:
            raise ValueError("Date not found")

        if "Transaction Details" not in df.columns:
            raise ValueError("Transaction Details not found")

        if "Deposits" not in df.columns:
            raise ValueError("Deposits not found")

        if "Withdrawals" not in df.columns:
            raise ValueError("Withdrawals not found")

        df[["Deposits"]] = df[["Deposits"]].fillna(0).astype(float)
        df[["Withdrawals"]] = df[["Withdrawals"]].fillna(0).astype(float)
        df["Date"] = df["Date"].apply(self.parse_date)

        # to handle duplicate on same day
        df["Seq"] = (
            df.groupby(["Date",
                        "Transaction Details",
                        "Deposits",
                        "Withdrawals"])
            .cumcount()
            .add(1)
        )
