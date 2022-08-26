


class MessageError(Exception):
    def __init__(self, msg="Failed to send message to user"):
        self.msg = msg
        super().__init__(self.msg)
class InvalidMatchId(Exception):
    def __init__(self, msg="Invalid match_id entered"):
        self.msg = msg
        super().__init__(self.msg)
class TinderRatelimited(Exception):
    def __init__(self, msg="Ratelimit reached, consider adding some cooldown"):
        self.msg = msg
        super().__init__(self.msg)
class TinderMatchNotFound(Exception):
    def __init__(self, msg="Match not found"):
        self.msg = msg
        super().__init__(self.msg)
class UserNotFound(Exception):
    def __init__(self, msg="User not found"):
        self.msg = msg
        super().__init__(self.msg)
class FailedToUpdateProfile(Exception):
    def __init__(self, msg="Failed to upload new profile info"):
        self.msg = msg
        super().__init__(self.msg)
class InvalidContactType(Exception):
    def __init__(self, msg="Invalid contact type, must be one of: snapchat, instagram"):
        self.msg = msg
        super().__init__(self.msg)
class InvalidJSONResponse(Exception):
    def __init__(self, method, endpoint, msg="Invalid JSON response when JSON was expected to be returned at "):
        msg += f"{method.upper()} {endpoint}"
        self.msg = msg
        super().__init__(self.msg)
class InputStringTooLong(Exception):
    def __init__(self, string, msg="The string you input was too long for tinder to accept: "):
        msg += f"{string}"
        self.msg = msg
        super().__init__(self.msg)
class InvalidPhotoList(Exception):
    def __init__(self, msg="Invalid photo list passed, needs to be a list and have at least 1 photo path in it"):
        self.msg = msg
        super().__init__(self.msg)