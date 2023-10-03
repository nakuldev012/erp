from mferp.auth.user.tokens import get_access_token
from mferp.common.errors import ClientErrors
from datetime import datetime, timezone
from oauth2_provider.settings import oauth2_settings
import secrets
import string


def generate_password(length=12):
    # Define the characters to use for the password
    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        # Generate a random password using secrets.choice
        password = ''.join(secrets.choice(characters) for _ in range(length))

        # Check if the password meets the requirements
        if (
            any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in string.punctuation for char in password) and
            not any(char in "<>~`^;|\/'" for char in password)
        ):
            return password



def check_password(pwd: str):
    """
    Check password is valid or not with (Upper,Lower,Digit,Special)

    param:
        pwd (str): password of user
    return:
        bool: True when password is valid, else False
    """
    not_special = ["~", "`", "<", ">", "^", ";", "|", "'"]
    special = [
        "$",
        "@",
        "#",
        "&",
        "*",
        "!",
        "(",
        ")",
        "+",
        "%",
        ",",
        "-",
        "_",
        ".",
        "/",
        ":",
        "=",
        "?",
        "[",
        "]",
        "{",
        "}",
    ]
    if len(pwd) < 8:
        raise ClientErrors("length should be at least 8")
    if not any(char.isdigit() for char in pwd):
        raise ClientErrors("Password should have at least one numeral")
    if not any(char.isupper() for char in pwd):
        raise ClientErrors("Password should have at least one uppercase letter")
    if not any(char.islower() for char in pwd):
        raise ClientErrors("Password should have at least one lowercase letter")
    if any(char in not_special for char in pwd):
        raise ClientErrors("< > ~ ` ^ ; | ' is not allowed")
    if not any(char in special for char in pwd):
        raise ClientErrors(
            "Password should have at least one of the symbols '$','@','#','&','*','!','(',')','+','%',',','-','_','.','/',':','=','?','[',']','{','}'"
        )
    else:
        return True
    


