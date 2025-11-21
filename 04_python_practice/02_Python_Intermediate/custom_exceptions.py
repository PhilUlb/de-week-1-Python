import string

DIGITS = "123456789"
SPECIAL_CHARS = "!@#$%^&*()"

class InvalidUserNameError(Exception):
    def __init__(self, username):
        self.user_name = username
        self.msg = f"Invalid user name '{username}'. User name needs to be at least 5 characters long and must not contain spaces."
        super().__init__(self.msg)


class InvalidPasswordError(Exception):
    def __init__(self, password):
        self.password = password
        self.msg = f"Invalid password '{password}'. Password needs to be at least 8 characters long and must contain at least one digit and one special character ('{SPECIAL_CHARS}')."
        super().__init__(self.msg)


def _validate_username(username: str) -> None:
    if " " in username or len(username) < 5:
        raise InvalidUserNameError(username)


def _validate_password(password: str) -> None:
    if len(password) < 8:
        raise InvalidPasswordError(password)
    if not any(e in DIGITS for e in password):
        raise InvalidPasswordError(password)
    if not any(e in SPECIAL_CHARS for e in password):
        raise InvalidPasswordError(password)
    

def register_user(username: str, password: str) -> bool:
    had_error = False
    try:
        _validate_username(username)
    except InvalidUserNameError as e:
        print(e)
        had_error = True
    except Exception as e:
        print(e)
        had_error = True
    try:
        _validate_password(password)
    except InvalidPasswordError as e:
        print(e)
        had_error = True
    except Exception as e:
        print(e)
        had_error = True
    
    return not had_error


if __name__=="__main__":
    print(register_user("Heno", "12345!!!!"))