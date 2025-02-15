# Bank Statement Parser

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PyPI Version](https://img.shields.io/pypi/v/bank-statement-parser)

**Bank Statement Parser** is a Python library designed to parse and normalize transaction data from various bank statement formats ( CSV, Excel, etc.) into a consistent and easy-to-use Pandas DataFrame. It supports multiple banks and file formats, making it a versatile tool for financial data analysis.

---

## Features

- **Multi-Format Support**: Parse bank statements from  CSV, Excel, and more.
- **Bank-Specific Parsing**: Customizable parsers for different banks.
- **Consistent Output**: Normalized transaction data with standardized columns (`Date`, `Description`, `Amount`, `Transaction Type`, etc.).
- **Easy Integration**: Simple API for quick integration into your Python projects.
- **Extensible**: Add support for new banks or formats with minimal effort.

---

## Installation

You can install the library via pip:

```bash
pip install BankStatementParser
```


# Usage
### Basic Example

```python
from parser import HSBC

# Initialize the parser
parser = BankStatementParser()

# Parse a bank statement
df = parser.parse("path/to/statement.pdf", format="pdf", bank="Chase")

# Display the parsed transactions
print(df.head())
```
