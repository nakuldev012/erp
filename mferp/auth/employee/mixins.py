# from django.contrib.auth.decorators import user_passes_test
# from django.utils.decorators import method_decorator
# from mferp.auth.user.models import Account


# def is_hradmin(user):
#     import ipdb;
#     ipdb.set_trace()
#     return user.groups.filter(name='hr_configuration').exists()

# class HRAdminRequiredMixin:
#     @method_decorator(user_passes_test(is_hradmin))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


# from django.core.exceptions import PermissionDenied
# from rest_framework.views import APIView
# class HRAdminRequiredMixin(APIView):
#     def dispatch(self, request, *args, **kwargs):

#         import ipdb;
#         ipdb.set_trace()
#         if request.user.groups.filter(name = "hr_configuration").exists():
#             #return True
#             return super().dispatch(request, *args, **kwargs)

#         else:
#             raise PermissionDenied(" You do not have permissions to access this")


# from functools import wraps
# from django.contrib.auth.decorators import user_passes_test
# from django.http import HttpResponseForbidden

# def group_required(hr_configuration):
#     """
#     Custom decorator to check if a user belongs to the specified group.
#     """
#     def decorator(view_func):
#         import ipdb;
#         ipdb.set_trace()
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if request.user.groups.filter(name=hr_configuration).exists():
#                 return view_func(request, *args, **kwargs)
#             else:
#                 # You can customize the response for unauthorized users here
#                 return HttpResponseForbidden("You do not have permission to access this view.")
#         return _wrapped_view
#     return decorator


from functools import wraps
from django.core.exceptions import PermissionDenied
from requests import Response

from mferp.common.errors import ForbiddenErrors, UserErrors
from rest_framework import status


def group_required(mater_Config):
    """
    Custom decorator to restrict access to views based on user group membership.
    :param hr_configuration: List of group names that are allowed to access the view.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            # try:
            user = request.user
            if user.groups.filter(name=mater_Config).exists():
                return view_func(self, request, *args, **kwargs)
            else:
                error_response = {
                "message": "You do not have permission to perform this action."
            }
                return Response(error_response, status=status.HTTP_403_FORBIDDEN)
                raise PermissionDenied
            #         raise ForbiddenErrors("You do not have permission to perform this action.")
            # except UserErrors as error:
            #     return Response(
            #         {
            #             "message": error.message,
            #             "success": False,
            #         },
            #         status=error.response_code,
            #     )
            # except Exception as error:
            #     return Response(
            #         {
            #             "message": "Something Went Wrong",
            #             "success": False,
            #         },
            #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     )
        return _wrapped_view

    return decorator
