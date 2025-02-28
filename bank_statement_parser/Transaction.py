from datetime import datetime
import hashlib


class Transaction:
    created_date: datetime
    bank: str
    remarks: str
    amount: float

    def __init__(self, bank: str,
                 created_date: datetime,
                 remarks: str,
                 amount: float):
        self.bank = bank
        self.created_date = created_date
        self.remarks = remarks
        self.amount = amount

    def hash(self):
        strObj = (str(self.bank) +
                  str(self.created_date) +
                  str(self.remarks) +
                  str(self.amount))
        hash_obj = hashlib.sha1(strObj.encode("utf-8"))
        hex_hash = hash_obj.hexdigest()
        return hex_hash

    def to_dict(self):
        return {
            "bank": self.bank,
            "created_date": self.created_date,
            "remarks": self.remarks,
            "amount": self.amount,
            "hash": self.hash(),
        }
