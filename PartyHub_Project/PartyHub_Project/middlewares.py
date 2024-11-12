from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class CustomErrorHandlingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, HttpResponseForbidden) or isinstance(exception, PermissionDenied):
            return render(request, '403.html', status=403)

        else:
            return None

