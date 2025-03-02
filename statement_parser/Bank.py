from abc import ABC, abstractmethod
from statement_parser.Transaction import Transaction
import pandas as pd
from dateutil import parser
import logging


class Bank(ABC):
    @abstractmethod
    def getTransactions(self, filename: str) -> list[Transaction]:
        pass

    def getDataFrame(self, filename: str) -> pd.DataFrame:
        trans = self.getTransactions(filename)
        return pd.DataFrame([t.to_dict() for t in trans])

    def get_transaction_start(self,
                              filename: str,
                              headers: list) -> int:
        """
        Find the row where transaction data starts.

        Parameters:
            file_path (str): Path to the file.

        Returns:
            int: Row index where transactions start.
        """
        if filename.endswith('.csv'):
            with open(filename, 'r') as file:
                lines = file.readlines()
        elif filename.endswith('.xls') or filename.endswith('.xlsx'):
            df = pd.read_excel(filename, header=None)
            lines = df.astype(str).values.tolist()
        else:
            raise ValueError("Unsupported file format. Use CSV or \
                             Excel files.")

        for i, line in enumerate(lines):
            if any(keyword in str(line).lower() for keyword in headers):
                return i

        raise ValueError("Could not find the start of transaction data.")

    def load_bank_statement(self,
                            file_path,
                            skip_rows=0,
                            delimiter=",",
                            usecols=None,
                            hasHeader=True) -> pd.DataFrame:
        """
        Load a bank statement file (CSV or Excel) into a DataFrame.

        Parameters:
            file_path (str): Path to the file.
            skip_rows (int): Number of initial rows to skip.

        Returns:
            pd.DataFrame: DataFrame containing transaction data.
        """
        logging.info(f"Loading bank statement \
                     file: {file_path} skip: {skip_rows}")

        if file_path.endswith('.csv'):
            if hasHeader:
                df = pd.read_csv(file_path,
                                 skiprows=skip_rows,
                                 delimiter=delimiter,
                                 usecols=usecols)
            else:
                df = pd.read_csv(file_path,
                                 skiprows=skip_rows,
                                 delimiter=delimiter,
                                 usecols=usecols,
                                 header=None)

        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, skiprows=skip_rows)
        else:
            raise ValueError("Unsupported file format. Use CSV or \
                             Excel files.")

        return df

    def parse_date(self, date_str):
        try:
            # Adjust for your date format
            return parser.parse(date_str, dayfirst=True)
        except ValueError:
            return None  # Handle invalid dates
