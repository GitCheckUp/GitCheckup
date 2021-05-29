class IError:
    # We may need to do None checks here.
    def __init__(self, error_id, error_type, user = None, commit = None, is_warning = False, extra_info = ""):
        self.error_id = error_id
        self.error_type = error_type
        self.user = user
        self.commit = commit
        self.extra_info = extra_info
        self.is_warning = is_warning
