class Errors:
    def __init__(self,error_id,error_type,user_id,commit=None):
        self.error_id=error_id
        self.user_id=user_id
        self.commit=commit
        self.error_type=error_type
        if(commit==None): 
            commit = "unknown"
    

    