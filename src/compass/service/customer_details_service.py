from src.database.service import UserDetailsService, KycDocumentsService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class CustomerDetailsService:

    @staticmethod
    def generate_customer_details_details(from_time):
        report_name = f"CST{DateTimeUtil.get_current_date()}01"
        try:
            batch, users_count = 1, 0
            while True:
                logger.info(f'generating customer details for batch {batch}')

                users = UserDetailsService.get_batch_by_since(batch, from_time)
                if len(users) == 0: break

                users_mapping = CustomerDetailsService.get_users_mapping(users)

                user_kyc_details_mapping = KycDocumentsService.get_by_user_ids(list({user.id for user in users_mapping.values()}))

                ReportService.write_report(report_name, CustomerDetailsService.convert_to_compass_format(users, users_mapping, user_kyc_details_mapping))
                batch += 1
                users_count += len(users)
            logger.info(f'generated customer details for {users_count} users')
        except Exception as exception:
            logger.error(f'failed to generate customer details: {exception}')
            traceback.print_exc()

    @staticmethod
    def get_users_mapping(users):
        users_mapping = {user.id: user for user in users}

        subaccount_users_parent_id_mapping = {user.id: user.parent_user_id for user in users if user.parent_user_id}
        parent_user_ids = list(subaccount_users_parent_id_mapping.values())
        parent_users = UserDetailsService.get_by_user_ids(parent_user_ids)
        parent_users_mapping = {user.id: user for user in parent_users}
        
        for user_id, parent_user_id in subaccount_users_parent_id_mapping.items():
            parent = parent_users_mapping.get(parent_user_id)
            if parent:
                users_mapping[user_id] = parent
        return users_mapping
    

    @staticmethod
    def convert_to_compass_format(users, users_mapping, user_kyc_details_mapping):
        users_compass = []
        for user in users:
            main_user = users_mapping.get(user.id)
            if not main_user:
                logger.debug(f"user with id: {user.id} not found")
            kyc = user_kyc_details_mapping.get(main_user.id, {}) if main_user else {}
        
            users_compass.append({
                'Customer ID': user.id,
                'Constitution Type': 'Individual',
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
                'Annual Income': main_user.income if main_user else None,
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
                'Phone Details': f'{main_user.country_calling_code} {main_user.phone_number}' if (main_user and main_user.country_calling_code and main_user.phone_number) else None,
                'PEP Flag': None,
                'NPO Flag': None,
                'HNI Flag': None,
                'Communication Address Line1': kyc.get("address"),
                'Communication Address Line2': None,
                'Communication City': None,
                'Communication State': main_user.region if main_user else None,
                'Communication Country': main_user.country if main_user else None,
                'Communication PO Box': None,
                'Communication  AddressDistrict': None,
                'Communication AddressLocality': None,
                'Communication AddressNon-Indian Pincode': None,
                'Communication Phone No': main_user.phone_number if main_user else None,
                'Communication Fax No': None,
                'Communication EmailId': main_user.email if main_user else None,
                'PermanentAddress Line 1': kyc.get("address"),
                'PermanentAddress Line 2': None,
                'Permanent City': None,
                'Permanent State': main_user.region if main_user else None,
                'Permanent PO Box': None,
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
                'REKYC_Status': main_user.is_kyc_done if main_user else None,
                'REKYC_Date': None,
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
                'Registered AddressLine1': None,
                'Registered AddressLine2': None,
                'Registered AddressCity': None,
                'Registered AddressState': None,
                'Registered AddressCountry': None,
                'Registered AddressPinCode': None,
                'Registered AddressPhoneNo': None,
                'Registered AddressFaxNo': None,
                'Registered AddressDistrict': None,
                'Registered AddressLocality': None,
                'Registered AddressNon-Indian Pincode': None,
                'Residence AddressLine1': None,
                'Residence AddressLine2': None,
                'Residence AddressCity': None,
                'Residence AddressState': None,
                'Residence AddressCountry': None,
                'Residence AddressPinCode': None,
                'Residence AddressPhoneNo': None,
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
                'CUSTOMERONBOARDING_CITY': None,
                'CUSTOMERONBOARDING_PROVINCE_OR_STATE': main_user.region if main_user else None,
                'CUSTOMERONBOARDING_PINCODE': None,
                'CUSTOMERONBOARDING_COUNTRY': main_user.country if main_user else None,
                'CUSTOMERONBOARDING_GEOLOCATION': None,
                'CUSTOMER_FAMILYCODE/CUSTOMER_GROUPCODE': None,
            })
        return users_compass