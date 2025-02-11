import re

class AddressUtil:

    @staticmethod
    def extract_pincode_state(address):
        if not address:
            return None, None

        pincode_match = re.search(r'\b\d{6}\b', address)
        states = [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
            "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
            "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
            "West Bengal", "Jammu and Kashmir", "Ladakh"
        ]
        state_pattern = r'\b(' + '|'.join(states) + r')\b'
        state_match = re.search(state_pattern, address, re.IGNORECASE)

        pincode = pincode_match.group(0) if pincode_match else None
        state = state_match.group(0) if state_match else None

        return pincode, state