class IError:
    def __init__(self, error_id, error_type, user_id, commit = None):
        self.error_id = error_id
        self.error_type = error_type
        self.user_id = user_id
        self.commit = commit