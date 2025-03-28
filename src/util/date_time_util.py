from datetime import datetime, timedelta, timezone

class DateTimeUtil:
    
    @staticmethod
    def get_last_date():
        utc_24hrs_ago = datetime.now(timezone.utc) - timedelta(hours=24)
        last_date = utc_24hrs_ago.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return last_date
    
    @staticmethod
    def get_today_date():
        now = datetime.now(timezone.utc)
        today_date = now.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return today_date
        
    @staticmethod
    def get_date_from_string(date_string):
        return datetime.strptime(date_string, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00.000000Z")
    
    @staticmethod
    def get_age_by_dob(dob):
        if dob is None:
            return None
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    
    @staticmethod
    def get_current_date():
        return datetime.now(timezone.utc).strftime('%d%m%Y')
    
    @staticmethod
    def get_master_date():
        utc_24hrs_ago = datetime.now(timezone.utc) - timedelta(days = 1000)
        updated_since = utc_24hrs_ago.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return updated_since
    
    @staticmethod
    def get_txn_master_date():
        utc_24hrs_ago = datetime.now(timezone.utc) - timedelta(days = 90)
        updated_since = utc_24hrs_ago.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return updated_since