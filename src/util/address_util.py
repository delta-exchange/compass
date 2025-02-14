import re
import requests
from .logger import logger

class AddressUtil:

    @staticmethod
    def extract_pincode_state_city(address, city_list=[]):
        if not address:
            return None, None, None

        pincode_match = re.search(r'\b\d{6}\b', address)
        pincode = pincode_match.group(0) if pincode_match else None

        states = [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", 
            "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", 
            "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
            "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", 
            "Uttarakhand", "West Bengal"
        ]
        union_territories = [
            "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", 
            "Lakshadweep", "Delhi", "Puducherry", "Jammu and Kashmir", "Ladakh"
        ]
        state_pattern = r'\b(' + '|'.join(states + union_territories) + r')\b'
        state_match = re.search(state_pattern, address, re.IGNORECASE)
        state = state_match.group(0) if state_match else None

        city = None
        if not state:
            index = address.lower().find(state.lower())
            if index != -1:
                address_before_state = address[:index]
                splits = address_before_state.split(",")
                if len(splits) >= 2:
                    city = splits[-2].strip()
        if not city:
            city_pattern = r'\b(' + '|'.join(city_list) + r')\b'
            city_match = re.search(city_pattern, address, re.IGNORECASE)
            city = city_match.group(0) if city_match else None
        if (not city) and pincode:
            city = AddressUtil.get_city_by_pincode_using_postal_api(pincode)

        return pincode, state, city
    
    @staticmethod
    def get_city_state_country_by_login(login):
        if not login or not login.location: return (None,)*3
        return AddressUtil.get_city_state_country_by_location(login.location)
    
    @staticmethod
    def get_city_state_country_by_location(location):
        if not location: return (None,)*3
        splits = location.split(", ")
        if len(splits) < 3: return (None,)*3
        return (splits[0], splits[1], splits[2])
    
    @staticmethod
    def get_city_by_pincode_using_postal_api(pincode):
        try:
            url = f"https://api.postalpincode.in/pincode/{pincode}"
            response = requests.get(url)
            response_json = response.json()
            
            if not response_json:
                return None
            
            post_offices = response_json[0].get("PostOffice", [])
            return post_offices[0].get("Block") if post_offices else None

        except Exception as e:
            logger.error(f"Postal API failed for pin: {pincode} and error: {e}")
            return None
