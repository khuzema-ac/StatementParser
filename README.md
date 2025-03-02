# Bank Statement Parser

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PyPI Version](https://img.shields.io/pypi/v/bank-statement-parser)

**Bank Statement Parser** is a Python library designed to parse and normalize transaction data from various bank statement formats ( CSV, Excel, etc.) into a consistent and easy-to-use Pandas DataFrame. It supports multiple banks and file formats, making it a versatile tool for financial data analysis.

---

## Features

- **Multi-Format Support**: Parse bank statements from  CSV, Excel, and more.
- **Bank-Specific Parsing**: Customizable parsers for different banks.
- **Consistent Output**: Normalized transaction data with standardized columns (`Date`, `Description`, `Amount`,  etc.).
- **Easy Integration**: Simple API for quick integration into your Python projects.
- **Extensible**: Add support for new banks or formats with minimal effort.

---

## Installation

You can install the library via pip:

```bash
pip install statement_parser
```


# Usage
### Basic Example

```python
from statement_parser.banks.HdfcCredit import HdfcCredit

parser = HsbcCredit()
df = parser.getDataFrame("path/to/statement.csv")
# Display the parsed transactions
print(df.head())
```
