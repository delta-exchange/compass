from src.database.service import UserDetailsService, KycDocumentsService, LoginHistoryService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, AddressUtil, get_report_index

import traceback

class CustomerDetailsService:

    @staticmethod
    def generate_customer_details_details(from_time, to):
        try:
            login_city_list = CustomerDetailsService.get_login_city_list()
            current_date = DateTimeUtil.get_current_date()
            logger.info(f'generating customer details')
            total_count = 0
            while True:
                logger.info(f"From: {from_time}")
                report_name = f"CST{current_date}" + get_report_index(total_count, 100000)
                users = UserDetailsService.get_between(from_time, to, batch_size=2000)
                users_count = len(users)
                if users_count == 0: 
                    break
                else:
                    from_time = users[-1].updated_at
                    total_count += len(users)

                    users_mapping = CustomerDetailsService.get_users_mapping(users)
                    user_kyc_details_mapping = KycDocumentsService.get_by_user_ids(list({user.id for user in users_mapping.values() if user.is_kyc_done}))
                    ReportService.write_report(report_name, CustomerDetailsService.convert_to_compass_format(users, users_mapping, user_kyc_details_mapping, login_city_list))
                
            logger.info(f'generated customer details for {total_count} users')
        except Exception as exception:
            logger.error(f'failed to generate customer details: {exception}')
            traceback.print_exc()

    @staticmethod
    def get_login_city_list():
        locations = LoginHistoryService.get_unique_locations()
        city_state_country_list = [AddressUtil.get_city_state_country_by_location(location) for location in locations if location]
        login_city_list = [city_state_country[0] for city_state_country in city_state_country_list if city_state_country[0]]
        return login_city_list

    @staticmethod
    def get_users_mapping(users):
        users_mapping = {user.id: user for user in users}

        subaccount_users_parent_id_mapping = {user.id: user.parent_user_id for user in users if user.parent_user_id}
        parent_user_ids = list(subaccount_users_parent_id_mapping.values())
        if len(parent_user_ids) == 0: 
            return users_mapping
        parent_users = UserDetailsService.get_by_user_ids(parent_user_ids)
        parent_users_mapping = {user.id: user for user in parent_users}
        
        for user_id, parent_user_id in subaccount_users_parent_id_mapping.items():
            parent = parent_users_mapping.get(parent_user_id)
            if parent:
                users_mapping[user_id] = parent
        return users_mapping
    

    @staticmethod
    def convert_to_compass_format(users, users_mapping, user_kyc_details_mapping, login_city_list):
        users_compass = []
        for user in users:
            main_user = users_mapping.get(user.id)
            if not main_user:
                logger.debug(f"user with id: {user.id} not found")
            kyc = user_kyc_details_mapping.get(main_user.id, {}) if main_user else {}
            pincode, state, city = AddressUtil.extract_pincode_state_city(kyc.get("address"), login_city_list)
            if not state:
                state = main_user.region if main_user else None
        
            users_compass.append({
                'Customer ID': user.id,
                'Constitutiopn Type': 'Individual',
                'Customer Type': 'Individual',
                'PRIMARY_SEGMENT': 'Futures & Options',
                'Customer Name': f'{main_user.first_name} {main_user.last_name}' if (main_user and main_user.first_name and main_user.last_name) else None,
                'FirstName': main_user.first_name if main_user else None,
                'MiddleName': None,
                'LastName': main_user.last_name if main_user else None,
                'Spouse/Partner Name': None,
                'Created Date Time': user.created_at,
                'Date of Birth / Incorporation': main_user.dob if main_user else None,
                'Age': DateTimeUtil.get_age_by_dob(main_user.dob) if main_user else None,
                'Place of Birth / Incorporation': None,
                'Nationality': main_user.country if main_user else None,
                'Residential Status': None, 
                'Salutation': None,
                'Father Name': None,
                'Mother Name': None,
                'Gender': None,
                'OccupationCode': main_user.occupation if main_user else None,
                'Nature of Business': main_user.occupation if main_user else None,
                'Credit Rating': None,
                'PAN No': kyc.get('pan_number'),
                'Passport No': None,
                'Driving License No': None,
                'VoterIdentityCardNo': None,
                'IdentityNo': kyc.get('aadhaar_number'),
                'TAX ID': None,
                'Annual Income': None,
                'Income From Business': None,
                'Other Income': None,
                'Net Worth': None,
                'Investments Val': None,
                'Marital Status': None,
                'Mobile No': main_user.phone_number if main_user else None,
                'WebSite': None,
                'Remarks': None,
                'Education': None,
                'CBS_RiskRating': None,
                'RM Code': None,
                'RM Name': None,
                'RM Mobile': None,
                'Authorized  Capital': None,
                'Phone Details': main_user.phone_number if main_user else None,
                'PEP Flag': None,
                'NPO Flag': None,
                'HNI Flag': None,
                'Communication Address Line1': kyc.get("address"),
                'Communication Address Line2': None,
                'Communication City': city,
                'Communication State': state,
                'Communication Country': main_user.country if main_user else None,
                'Communication PO Box': pincode,
                'Communication  AddressDistrict': None,
                'Communication AddressLocality': None,
                'Communication AddressNon-Indian Pincode': None,
                'Communication Phone No': main_user.phone_number if main_user else None,
                'Communication Fax No': None,
                'Communication EmailId': main_user.email if main_user else None,
                'PermanentAddress Line 1': kyc.get("address"),
                'PermanentAddress Line 2': None,
                'Permanent City': city,
                'Permanent State': state,
                'Permanent PO Box': pincode,
                'Permanent Country': main_user.country if main_user else None,
                'Permanent AddressDistrict': None,
                'Permanent AddressLocality': None,
                'Permanent AddressNon-Indian Pincode': None,
                'Permanent Phone No': main_user.phone_number if main_user else None,
                'Permanent Fax No': None,
                'Permanent EMailId': user.email,
                'PASSPORT_ISSUEDATE': None,
                'PASSPORT_EXPIRYDATE': None,
                'PASSPORT_ISSUEDPLACE': None,
                'PASSPORT_COUNTRYOFISSUE': None,
                'PASSPORT_COUNTRYOF RESIDENCE': None,
                'NPR': None,
                'DIN / DPIN': None,
                'REKYC_Status': main_user.is_kyc_refresh_required if main_user else None,
                'REKYC_Date': main_user.kyc_expiry_date if main_user else None,
                'FCRA status': None,
                'FCRA Registration State': None,
                'FCRA Registration Number': None,
                'Line oF Business': None,
                'FCRN': None,
                'LLPIN': None,
                'FLLPIN': None,
                'TAN': None,
                'GSTIN': None,
                'IEC Code': None,
                'Office AddressLine1': None,
                'Office AddressLine2': None,
                'Office AddressCity': None,
                'Office AddressState': None,
                'Office AddressCountry': None,
                'Office AddressPinCode': None,
                'Office AddressPhoneNo': None,
                'Office AddressFaxNo': None,
                'Office AddressDistrict': None,
                'Office AddressLocality': None,
                'Office AddressNon-Indian Pincode': None,
                'Non-face to Face flag': None,
                'CUSTOMER_STATUS': None,
                'ANNUAL_SALES': None,
                'Country of Nationality': main_user.country if main_user else None,
                'Country of Incorporation': main_user.country if main_user else None,
                'Registered AddressLine1': kyc.get("address"),
                'Registered AddressLine2': None,
                'Registered AddressCity': city,
                'Registered AddressState': state,
                'Registered AddressCountry': main_user.country if main_user else None,
                'Registered AddressPinCode': pincode,
                'Registered AddressPhoneNo': main_user.phone_number if main_user else None,
                'Registered AddressFaxNo': None,
                'Registered AddressDistrict': None,
                'Registered AddressLocality': None,
                'Registered AddressNon-Indian Pincode': None,
                'Residence AddressLine1': kyc.get("address"),
                'Residence AddressLine2': None,
                'Residence AddressCity': city,
                'Residence AddressState': state,
                'Residence AddressCountry': main_user.country if main_user else None,
                'Residence AddressPinCode': pincode,
                'Residence AddressPhoneNo': main_user.phone_number if main_user else None,
                'Residence AddressFaxNo': None,
                'Residence AddressDistrict': None,
                'Residence AddressLocality': None,
                'Residence AddressNon-Indian Pincode': None,
                'Alternate AddressLine1': None,
                'Alternate AddressLine2': None, 
                'Alternate AddressCity': None,
                'Alternate AddressState': None,
                'Alternate AddressCountry': None,
                'Alternate AddressPinCode': None,
                'Alternate AddressPhoneNo': None,
                'Alternate AddressFaxNo': None,
                'Alternate AddressDistrict': None,
                'Alternate AddressLocality': None,
                'Alternate AddressNon-Indian Pincode': None,
                'Alternate AddressCity / Village / Town': None, 
                'DATA_SOURCE': None,
                'UPDATE_TIMESTAMP': user.updated_at,
                'CUSTOMERONBOARDING_IPADDRESS': None,
                'CUSTOMERONBOARDING_ADDRESS': kyc.get("address"),
                'CUSTOMERONBOARDING_CITY': city,
                'CUSTOMERONBOARDING_PROVINCE_OR_STATE': state,
                'CUSTOMERONBOARDING_PINCODE': pincode,
                'CUSTOMERONBOARDING_COUNTRY': main_user.country if main_user else None,
                'CUSTOMERONBOARDING_GEOLOCATION': None,
                'CUSTOMER_FAMILYCODE/CUSTOMER_GROUPCODE': main_user.id if main_user else None,
                'Annual Income Range': main_user.income if main_user else None,
            })
        return users_compass