class Validators(object):
    
    @staticmethod
    def validate_username(username):
        if len(username) < 3 or username == "" or username == None:
            return False
        return True