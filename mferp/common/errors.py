from rest_framework import serializers


class CustomValidationErrorMixin:
    def is_valid(self, raise_exception=False):
        valid = super().is_valid(raise_exception=False)
        if not valid and raise_exception:
            # Customize the response for validation errors
            response_data = {
                "message": "All Fields are required",
                "success": False,
            }
            raise serializers.ValidationError(response_data)
        return valid


class UserErrors(Exception):
    """
    Error Exception
    """

    def __init__(self, message=None, error_message=None, response_code=None):
        self.message = message if message else "Could Not Validate Credentials"
        self.error_message = error_message if error_message else ""
        self.response_code = response_code if response_code else 400
        self.type = "User Errors"

class ForbiddenErrors(UserErrors):
    """
    Error Exception
    """

    def __init__(self, message=None, error_message=None, response_code=None):
        self.message = message if message else "You do not have permission to perform this action."
        self.error_message = error_message if error_message else ""
        self.response_code = response_code if response_code else 403
        self.type = "Forbidden Errors"


class ClientErrors(UserErrors):
    """
    When error occured because of user's response
    """

    def __init__(self, message=None, error_message=None, response_code=None):
        self.message = message if message else "All fields are required"
        self.error_message = error_message if error_message else ""
        self.response_code = response_code if response_code else 400
        self.type = "Client Errors"


class DatabaseErrors(UserErrors):
    """
    When error occured because of database issue
    """

    def __init__(self, message=None, error_message=None, response_code=None):
        self.message = message if message else "Some Database Issue. Try Again"
        self.error_message = error_message if error_message else ""
        self.response_code = response_code if response_code else 503
        self.type = "Database Errors"


class ServerErrors(UserErrors):
    """
    When error occured because of server error
    """

    def __init__(self, message=None, error_message=None, response_code=None):
        self.message = message if message else "Internal Server Error"
        self.error_message = error_message if error_message else ""
        self.response_code = response_code if response_code else 500
        self.type = "Server Errors"
