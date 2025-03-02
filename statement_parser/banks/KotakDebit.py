import pandas as pd
import statement_parser.Bank as Bank
from statement_parser.Transaction import Transaction


class KotakDebit(Bank):
    __id_bank = "KOTAK-DEBIT"

    def getTransactions(self, filename: str) -> list[Transaction]:
        transactions: list[Transaction] = []
        df = self.getData(filename)
        self.validateDataframe(df)

        for index, row in df.iterrows():
            _duplicate = ""
            _multiplier = 1
            _checkNo = ""

            if row["Seq"] > 1:
                _duplicate = " (" + str(row["Seq"]) + ") "

            if row["Dr / Cr"].upper() == "DR":
                _multiplier = -1

            if str(row["Chq / Ref No."]).strip() != "nan":
                _checkNo = "Ref: " + str(row["Chq / Ref No."]).strip() + " "

            created_date = row["Transaction Date"]
            remarks = _checkNo + row["Description"].strip() + _duplicate
            amount = row["Amount"] * _multiplier
            transaction = Transaction(
                bank=self.__id_bank,
                created_date=created_date,
                remarks=remarks,
                amount=amount,
            )
            transactions.append(transaction)

        return transactions

    def getData(self, filename: str) -> pd.DataFrame:
        skip_rows = self.get_transaction_start(filename, ["date", "sr.no"])
        df_full = self.load_bank_statement(filename, skip_rows=skip_rows)
        # filter out empty rows
        df_filtered = df_full[df_full.iloc[:, 8].notna()]
        # remove last column since it has same header has
        # CR/DR which is causing issues later
        del df_filtered[df_filtered.columns[-1]]
        df = df_filtered.copy()
        return df

    def validateDataframe(self, df):
        if "Transaction Date" not in df.columns:
            raise ValueError("Transaction Date not found")

        if "Sl. No." not in df.columns:
            raise ValueError("Sl. No. not found")

        if "Description" not in df.columns:
            raise ValueError("Description not found")

        if "Chq / Ref No." not in df.columns:
            raise ValueError("Chq / Ref No. not found")

        if "Amount" not in df.columns:
            raise ValueError("Amount not found")

        if "Dr / Cr" not in df.columns:
            raise ValueError("Dr / Cr not found")

        df[["Sl. No."]] = df[["Sl. No."]].astype(int)
        df["Amount"] = df["Amount"].str.replace(",", "")
        df[["Amount"]] = df[["Amount"]].astype(float)
        df["Transaction Date"] = pd.to_datetime(
            df["Transaction Date"], format="%d-%m-%Y"
        )

        if df["Sl. No."].max() != len(df):
            raise ValueError("No. of rows does not match")
        # to handle duplicate on same day
        df["Seq"] = (
            df.groupby(
                [
                    "Transaction Date",
                    "Description",
                    "Chq / Ref No.",
                    "Amount",
                    "Dr / Cr",
                ]
            )
            .cumcount()
            .add(1)
        )
