
import pandas as pd
import statement_parser.Bank as Bank
from statement_parser.Transaction import Transaction


class HdfcCredit(Bank):
    __id_bank = "HDFC-CREDIT"

    def getTransactions(self, filename: str) -> list[Transaction]:
        transactions: list[Transaction] = []

        df = self.getData(filename)
        self.validateDataframe(df)

        for index, row in df.iterrows():
            _duplicate = ""

            if row["Seq"] > 1:
                _duplicate = " (" + str(row["Seq"]) + ") "

            created_date = row["DATE"]
            remarks = row["Description"].strip() + _duplicate

            if row["Debit / Credit"] == "CR":
                _multiplier = 1
            else:
                _multiplier = -1

            amount = row["AMT"] * _multiplier
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
                                               ["transaction type"])
        df_full = self.load_bank_statement(filename,
                                           skip_rows=skip_rows,
                                           delimiter='~',
                                           usecols=["DATE",
                                                    "Description",
                                                    "AMT",
                                                    "Debit / Credit "])
        # filter out empty rows

        df_filtered = df_full[df_full.iloc[:, 1].notna()]
        df_filtered.columns = df_filtered.columns.str.strip()
        df_filtered.loc[:, "DATE"] = df_filtered["DATE"].apply(self.parse_date)
        # Filter out rows where "DATE" is NaT
        df_filtered = df_filtered[df_filtered["DATE"].notna()]
        df = df_filtered.copy()
        return df

    def validateDataframe(self, df):
        if "DATE" not in df.columns:
            raise ValueError("Date not found")

        if "AMT" not in df.columns:
            raise ValueError("AMT not found")

        if "Description" not in df.columns:
            raise ValueError("Description not found")

        if "Debit / Credit" not in df.columns:
            raise ValueError("Debit / Credit not found")

        # Ensure "Amount(in Rs)" is a string before replacing commas
        if df["AMT"].dtype != 'object':
            df["AMT"] = df["AMT"].astype(str)
        df["AMT"] = df["AMT"].str.replace(",", "")
        df[["AMT"]] = df[["AMT"]].astype(float)
        # Change Cr to upper case and remove spaces
        df["Debit / Credit"] = df["Debit / Credit"].str.upper().str.strip()
        # df["DATE"] = df["DATE"].apply(self.parse_date)
        print(df)
        df["Seq"] = (
            df.groupby(["DATE", "Description", "AMT", "Debit / Credit"])
            .cumcount()
            .add(1)
        )
