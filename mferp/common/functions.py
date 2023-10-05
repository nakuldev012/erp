from mferp.auth.user.tokens import get_access_token
from mferp.common.errors import ClientErrors
from datetime import datetime, timezone
from oauth2_provider.settings import oauth2_settings
import secrets
import string
import re
import pytz
from datetime import datetime
from mferp.common.constant import TZ
from mferp.common.errors import ClientErrors, UserErrors, ServerErrors


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
    

def conversion_24_time(str_time: str, column_name: str):
    """
    Converts the time from dataframe to 24 hr format
    :param str_time: s
    :return: str time in 24 hr format
    """
    try:
        values = str_time.split(":")
        if len(values) < 2:
            raise ServerErrors(
                "Time format should be correct in sheet column name :- "
                + str(column_name)
            )
        if values[-1][-2:] == "AM":
            if values[0] == "12":
                str_time_24 = ":".join(["00", values[1][:2]])
            else:
                str_time_24 = ":".join([values[0], values[1][:2]])
        else:
            if values[0] == "12":
                str_time_24 = ":".join([values[0], values[1][:2]])
            else:
                str_time_24 = ":".join([str(int(values[0]) + 12), values[1][:2]])
        return str_time_24
    except UserErrors:
        raise
    except:
        raise UserErrors(message="Sheet column " + column_name + " is not correct")


def convert_time_to_utc(time_string: str, date_string: str, column_name: str):
    """
    Converts the time and date string to UTC format
    :param time_string: str
    :param date_string: str
    :return: datetime object with value in UTC format
    """
    try:
        time_24 = conversion_24_time(time_string, column_name)
        datetime_str = datetime.strptime(
            date_string + " " + time_24.strip(), "%d-%b-%Y %H:%M"
        )
        riyadh_tz = pytz.timezone("Asia/Riyadh")
        riyadh_time = riyadh_tz.localize(datetime_str)
        utc_time = riyadh_time.astimezone(TZ)
    except UserErrors:
        raise
    except:
        raise UserErrors(message="Sheet column " + column_name + " is not correct")
    return utc_time


def get_string_datetime(date: datetime):
    """
    Convert DateTime to String Format

    Args:
        date (datetime): DateTime object

    Raises:
        ServerErrors: When error occured at conversion

    Returns:
        [str]: date_str: String of format "%Y-%m-%dT%H:%M:%SZ"
    """
    try:
        date_str = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return date_str
    except:
        raise ServerErrors("DateTime format is not correct")



def get_date_datetime(date_str: str):
    """
    Convert DateTime to String Format

    Args:
        date_str (str): DateTime object

    Raises:
        ServerErrors: When error occured at conversion

    Returns:
        [datetime]: date: String of format "%Y-%m-%dT%H:%M:%SZ"
    """
    try:
        try:
            date = TZ.localize(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ"))
        except:
            date = TZ.localize(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ"))
        return date
    except:
        raise ServerErrors("DateTime format is not correct")


def validate_email(email):
    """
    Validate email

    Args:
        email (str): Email address

    Returns:
        bool: True if validate
    """
    regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    if re.fullmatch(regex, email):
        return True
    return False

    


