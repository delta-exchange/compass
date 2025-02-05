from src.database.service import UserDetailsService, KycDocumentsService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class CustomerDetailsService:

    @staticmethod
    def generate_customer_details_details():
        report_name = f"CST{DateTimeUtil.get_current_date()}01"
        try:
            batch, users_count = 1, 0
            while True:
                logger.info(f'generating customer details for batch {batch}')
                users = UserDetailsService.get_batch_by_created_at(batch)
                if len(users) == 0:
                    break

                user_ids = [user.id for user in users] + [user.parent_user_id for user in users]
                valid_user_ids = [id for id in user_ids if id]
                user_kyc_details = KycDocumentsService.get_by_user_ids(valid_user_ids)
                ReportService.write_report(report_name, CustomerDetailsService.__convert_to_compass_format(users, user_kyc_details))
                batch += 1
                users_count += len(users)
            logger.info(f'generated customer details for {users_count} login histories')
        except Exception as exception:
            logger.error(f'failed to generate customer details: {exception}')
            traceback.print_exc()

    @staticmethod
    def __convert_to_compass_format(users, user_kyc_details):
        users_compass = []
        for user in users:
            kyc = user_kyc_details.get(user.id, {})
            if (not kyc) and user.parent_user_id:
                kyc = user_kyc_details.get(user.parent_user_id, {})

            users_compass.append({
                'Customer ID': user.id,
                'Constitutiopn Type': None,
                'Customer Type': None,
                'PRIMARY_SEGMENT': None,
                'Customer Name': f"{user.first_name if user.first_name else ''} {user.last_name if user.last_name else ''}",
                'FirstName': user.first_name,
                'MiddleName': None,
                'LastName': user.last_name,
                'Spouse/Partner Name': None,
                'Created Date Time': user.created_at,
                'Date of Birth / Incorporation': user.dob,
                'Age': DateTimeUtil.get_age_by_dob(user.dob),
                'Place of Birth / Incorporation': None,
                'Nationality': user.country,
                'Residential Status': None, 
                'Salutation': None,
                'Father Name': None,
                'Mother Name': None,
                'Gender': None,
                'OccupationCode': user.occupation,
                'Nature of Business': user.occupation,
                'Credit Rating': None,
                'PAN No': kyc.get("pan_number"),
                'Passport No': None,
                'Driving License No': None,
                'VoterIdentityCardNo': None,
                'IdentityNo': kyc.get("aadhaar_number"),
                'TAX ID': None,
                'Annual Income': user.income,
                'Income From Business': None,
                'Other Income': None,
                'Net Worth': None,
                'Investments Val': None,
                'Marital Status': None,
                'Mobile No': user.phone_number,
                'WebSite': None,
                'Remarks': None,
                'Education': None,
                'CBS_RiskRating': None,
                'RM Code': None,
                'RM Name': None,
                'RM Mobile': None,
                'Authorized  Capital': None,
                'Phone Details': f"{user.country_calling_code if user.country_calling_code else ''} {user.phone_number if user.phone_number else ''}",
                'PEP Flag': None,
                'NPO Flag': None,
                'HNI Flag': None,
                'Communication Address Line1': kyc.get("address"),
                'Communication Address Line2': None,
                'Communication City': None,
                'Communication State': user.region,
                'Communication Country': user.country,
                'Communication PO Box': None,
                'Communication  AddressDistrict': None,
                'Communication AddressLocality': None,
                'Communication AddressNon-Indian Pincode': None,
                'Communication Phone No': user.phone_number,
                'Communication Fax No': None,
                'Communication EmailId': user.email,
                'PermanentAddress Line 1': kyc.get("address"),
                'PermanentAddress Line 2': None,
                'Permanent City': None,
                'Permanent State': user.region,
                'Permanent PO Box': None,
                'Permanent Country': user.country,
                'Permanent AddressDistrict': None,
                'Permanent AddressLocality': None,
                'Permanent AddressNon-Indian Pincode': None,
                'Permanent Phone No': user.phone_number,
                'Permanent Fax No': None,
                'Permanent EMailId': user.email,
                'PASSPORT_ISSUEDATE': None,
                'PASSPORT_EXPIRYDATE': None,
                'PASSPORT_ISSUEDPLACE': None,
                'PASSPORT_COUNTRYOFISSUE': None,
                'PASSPORT_COUNTRYOF RESIDENCE': None,
                'NPR': None,
                'DIN / DPIN': None,
                'REKYC_Status': user.is_kyc_done,
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
                'Country of Nationality': user.country,
                'Country of Incorporation': user.country,
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
                'CUSTOMERONBOARDING_PROVINCE_OR_STATE': user.region,
                'CUSTOMERONBOARDING_PINCODE': None,
                'CUSTOMERONBOARDING_COUNTRY': user.country,
                'CUSTOMERONBOARDING_GEOLOCATION': None,
                'CUSTOMER_FAMILYCODE/CUSTOMER_GROUPCODE': None,
            })
        return users_compass