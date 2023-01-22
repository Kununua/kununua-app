class Validators(object):
    
    @staticmethod
    def validate_username(username):
        if len(username) < 3 or not username:
            return False
        return True