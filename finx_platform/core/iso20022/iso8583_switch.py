"""ISO 8583 Financial Transaction Card Originated Message Switch Parser."""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import struct


class ISO8583Message:
    """Standard ISO 8583 Bitmap & Field Parser for ATM & POS Card Transactions."""
    
    FIELD_NAMES = {
        0: "MTI",
        2: "Primary Account Number (PAN)",
        3: "Processing Code",
        4: "Transaction Amount",
        7: "Transmission Date and Time",
        11: "System Trace Audit Number (STAN)",
        12: "Local Transaction Time",
        13: "Local Transaction Date",
        14: "Expiration Date",
        18: "Merchant Category Code (MCC)",
        22: "Point of Service Entry Mode",
        25: "Point of Service Condition Code",
        32: "Acquiring Institution Identification Code",
        37: "Retrieval Reference Number (RRN)",
        38: "Authorization Identification Response",
        39: "Response Code",
        41: "Card Acceptor Terminal Identification",
        42: "Card Acceptor Identification Code",
        43: "Card Acceptor Name/Location",
        48: "Private Additional Data",
        49: "Currency Code",
        52: "Personal Identification Number (PIN) Block",
        54: "Additional Amounts",
        55: "EMV ICC System Related Data",
        62: "Custom Private Field",
        102: "Account Identification 1 (Source)",
        103: "Account Identification 2 (Dest)",
        128: "Message Authentication Code (MAC)"
    }

    RESPONSE_CODES = {
        "00": "Approved or completed successfully",
        "01": "Refer to card issuer",
        "04": "Pick-up card (stolen/lost)",
        "05": "Do not honor",
        "12": "Invalid transaction",
        "13": "Invalid amount",
        "14": "Invalid card number (no such number)",
        "51": "Insufficient funds",
        "54": "Expired card",
        "55": "Incorrect personal identification number (PIN)",
        "57": "Transaction not permitted to cardholder",
        "58": "Transaction not permitted to terminal",
        "61": "Exceeds withdrawal amount limit",
        "65": "Exceeds withdrawal frequency limit",
        "75": "Allowable number of PIN tries exceeded",
        "91": "Issuer or switch is inoperative",
        "96": "System malfunction"
    }

    def __init__(self, mti: str = "0200"):
        self.mti = mti
        self.fields: Dict[int, str] = {}

    def set_field(self, field_num: int, value: str) -> None:
        self.fields[field_num] = str(value)

    def get_field(self, field_num: int) -> Optional[str]:
        return self.fields.get(field_num)

    def generate_stan(self) -> str:
        now = datetime.now(timezone.utc)
        return now.strftime("%H%M%S")

    def generate_rrn(self, stan: str) -> str:
        now = datetime.now(timezone.utc)
        return f"{now.strftime('%y%j%H')}{stan[:4]}"

    def pack(self) -> Dict[str, Any]:
        """Encodes ISO 8583 message dictionary representation."""
        return {
            "mti": self.mti,
            "fields": {
                f"field_{k}_{self.FIELD_NAMES.get(k, 'Unknown').replace(' ', '_')}": v
                for k, v in sorted(self.fields.items())
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    @classmethod
    def create_auth_request(cls, pan: str, amount: float, exp: str, mcc: str = "5411", terminal_id: str = "TERM0001") -> "ISO8583Message":
        msg = cls("0200")
        msg.set_field(2, pan)
        msg.set_field(3, "000000")  # Goods and Services Purchase
        msg.set_field(4, f"{int(amount * 100):012d}")
        now = datetime.now(timezone.utc)
        msg.set_field(7, now.strftime("%m%d%H%M%S"))
        stan = msg.generate_stan()
        msg.set_field(11, stan)
        msg.set_field(12, now.strftime("%H%M%S"))
        msg.set_field(13, now.strftime("%m%d"))
        msg.set_field(14, exp)
        msg.set_field(18, mcc)
        msg.set_field(22, "051")  # Chip read with PIN
        msg.set_field(37, msg.generate_rrn(stan))
        msg.set_field(41, terminal_id)
        msg.set_field(49, "356")  # INR Currency ISO Code
        return msg

    def create_auth_response(self, response_code: str = "00", auth_id: str = "AUTH99") -> "ISO8583Message":
        resp = ISO8583Message("0210")
        for k, v in self.fields.items():
            resp.set_field(k, v)
        resp.set_field(38, auth_id if response_code == "00" else "")
        resp.set_field(39, response_code)
        return resp
