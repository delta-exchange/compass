from datetime import datetime, timedelta, timezone

class DateTimeUtil:
    
    @staticmethod
    def get_24hrs_ago():
        utc_24hrs_ago = datetime.now(timezone.utc) - timedelta(hours=24)
        updated_since = utc_24hrs_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
        return updated_since
    
    @staticmethod
    def get_date_from_string(date_string):
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    
    @staticmethod
    def get_age_by_dob(dob):
        if dob is None:
            return None
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    
    @staticmethod
    def get_current_date():
        return datetime.now(timezone.utc).strftime('%Y-%m-%d')