from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from authentication.models import User


class VacancyCreatePermission(permissions.BasePermission):
    message = 'Adding vacancies for non hr user not allowed.'

    def has_permission(self, request, view):
        # if isinstance(request.user, AnonymousUser):
        #     return False

        if request.user.role != User.HR:
            return False
        return True
