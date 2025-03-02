
import pandas as pd
import statement_parser.Bank as Bank
from statement_parser.Transaction import Transaction


class IciciCredit(Bank):
    __id_bank = "ICICI-CREDIT"

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

            if row["BillingAmountSign"] == "CR":
                _multiplier = 1
            else:
                _multiplier = -1

            amount = row["Amount(in Rs)"] * _multiplier
            transaction = Transaction(
                bank=self.__id_bank,
                created_date=created_date,
                remarks=remarks,
                amount=amount
            )
            transactions.append(transaction)

        return transactions

    def getData(self, filename: str) -> pd.DataFrame:
        skip_rows = self.get_transaction_start(filename, ["date", "sr.no"])
        df_full = self.load_bank_statement(filename, skip_rows=skip_rows)
        # filter out empty rows
        df_filtered = df_full[df_full.iloc[:, 3].notna()]
        df = df_filtered.copy()
        return df

    def validateDataframe(self, df):
        if "Date" not in df.columns:
            raise ValueError("Date not found")

        if "Sr.No." not in df.columns:
            raise ValueError("Sr.No. not found")

        if "Transaction Details" not in df.columns:
            raise ValueError("Transaction Details not found")

        if "Amount(in Rs)" not in df.columns:
            raise ValueError("Amount(in Rs) not found")

        df[["Sr.No."]] = df[["Sr.No."]].astype(int)
        # Ensure "Amount(in Rs)" is a string before replacing commas
        if df["Amount(in Rs)"].dtype != 'object':
            df["Amount(in Rs)"] = df["Amount(in Rs)"].astype(str)
        df["Amount(in Rs)"] = df["Amount(in Rs)"].str.replace(",", "")
        df[["Amount(in Rs)"]] = df[["Amount(in Rs)"]].astype(float)
        df["Date"] = df["Date"].apply(self.parse_date)

        # if df["Sr.No."].max() != len(df):
        #     raise ValueError("No. of rows does not match {} != {}"
        #                      .format(len(df), df["Sr.No."].max()))
        # to handle duplicate on same day
        df["Seq"] = (
            df.groupby(["Date", "Transaction Details", "Amount(in Rs)"])
            .cumcount()
            .add(1)
        )
