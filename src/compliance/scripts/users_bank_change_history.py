import traceback
import csv
import os

from src.util import DateTimeUtil, logger
from src.database.service import UserBankAccountService, UserDetailsService, KycDocumentsService

COMPLIANCE_DATA_DIR = os.path.join(os.getcwd(), 'reports', 'compliance_data')
BANK_ACCOUNT_CHANGES_FILE = "bank_account_changes.csv"

def generate_users_bank_change_history(from_date, to_date = None):
    try:
        from_date = DateTimeUtil.get_date_from_string(from_date)
        if to_date:
            to_date = DateTimeUtil.get_date_from_string(to_date)
        else:
            to_date = DateTimeUtil.get_today_date()
        logger.info(f"Generating users bank change history from {from_date} to {to_date}")

        create_csv_file(['User ID', 'Name', 'Account Activation Date', 'Old Bank Account Number', 'Old Bank IFSC', 'New Bank Account Number', 'New Bank IFSC', 'Change Date', 'Individual/Non-Individual Account'])

        while True:
            logger.info(f"To Date: {to_date}")

            user_bank_account_status_logs = UserBankAccountService.get_user_bank_change_status_logs_by_status_and_between("completed", from_date, to_date)
            user_bank_account_status_logs_count = len(user_bank_account_status_logs)
            if user_bank_account_status_logs_count == 0:
                break
    
            user_ids = list({user_bank_account_status_log.user_id for user_bank_account_status_log in user_bank_account_status_logs})
            
            users_mapping = get_users_mapping(user_ids)
            approved_kyc_mapping = get_kyc_status_mapping(user_ids)
            user_bank_map = get_user_banks_mapping(user_ids)

            user_bank_changes_data = get_user_bank_changes_data(user_bank_account_status_logs, users_mapping, approved_kyc_mapping, user_bank_map)
            logger.info(f"bank changes count: {len(user_bank_changes_data)}")
            if len(user_bank_changes_data) == 0:
                break

            add_to_csv_file(user_bank_changes_data)
    
            to_date = user_bank_account_status_logs[-1].created_at      
    except Exception as e:
        logger.error(f"Error generating users bank change history: {e}")
        traceback.print_exc()

def create_csv_file(csv_columns):
    dirname = os.path.join(COMPLIANCE_DATA_DIR, DateTimeUtil.get_current_date())
    os.makedirs(dirname, exist_ok=True)
    file_path = os.path.join(COMPLIANCE_DATA_DIR, DateTimeUtil.get_current_date(), BANK_ACCOUNT_CHANGES_FILE)
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_columns)

def add_to_csv_file(data):
    file_path = os.path.join(COMPLIANCE_DATA_DIR, DateTimeUtil.get_current_date(), BANK_ACCOUNT_CHANGES_FILE)
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def get_users_mapping(user_ids):
    users = UserDetailsService.get_by_user_ids(user_ids)
    return {user.id: user for user in users}

def get_kyc_status_mapping(user_ids):
    approved_kyc_status_logs = KycDocumentsService.get_approved_kyc_status_by_user_ids(user_ids)
    return {log.user_id: log for log in approved_kyc_status_logs}

def get_user_banks_mapping(user_ids):
    user_banks = UserBankAccountService.get_user_banks_by_user_ids_and_status(user_ids, "completed")
    user_bank_map = {user_id: [] for user_id in user_ids}
    for bank in user_banks:
        user_bank_map[bank.user_id].append(bank)
    return user_bank_map

def get_user_bank_changes_data(user_bank_account_status_logs, users_mapping, approved_kyc_mapping, user_bank_map):
    user_bank_changes = []
    for user_bank_account_status_log in user_bank_account_status_logs:
        user_id = user_bank_account_status_log.user_id
        user = users_mapping.get(user_id)
        if not user:
            logger.error(f"User with ID {user_id} not found for bank change history log.")
            continue
        
        user_banks = user_bank_map.get(user_id, [])[::-1]

        if len(user_banks) < 3:
            continue

        last_bank = next((bank for bank in user_banks if bank.created_at <= user_bank_account_status_log.created_at ), None)
        last_to_last_bank = next((bank for bank in user_banks if last_bank and bank.created_at < last_bank.created_at ), None)
        if not last_to_last_bank:
            continue

        kyc_approval_log = approved_kyc_mapping.get(user_id)

        user_bank_changes.append([
            user_id,
            (user.first_name or "") + " " + (user.last_name or ""),
            kyc_approval_log.created_at.strftime("%Y-%m-%d %H:%M:%S") if kyc_approval_log else "N/A",
            last_to_last_bank.account_number if len(user_banks) > 0 else "N/A",
            last_to_last_bank.ifsc_code if len(user_banks) > 0 else "N/A",
            last_bank.account_number,
            last_bank.ifsc_code,
            user_bank_account_status_log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Individual" if user.corporate_account_id else "Non-Individual"
        ])

    return user_bank_changes
    
