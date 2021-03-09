from django.http  import HttpResponse
from django.shortcuts import redirect 

def isUserauthenticated(view_func):
    def wrapper_func(request, *args,**kwargs):
        print('celal sengör', request.user.is_authenticated)
        if request.user.is_authenticated:
            return view_func(request,*args,**kwargs)
        else:
            return HttpResponse("You are taller not allowed ")
    return wrapper_func
def isUserauthenticatedorAdmin(view_func):
    def wrapper_func(request, *args,**kwargs):
        print('celal sengör', request.user.is_authenticated)
        if request.user.is_authenticated or request.user.is_superuser:
            return view_func(request,*args,**kwargs)
        else:
            return HttpResponse("You are taller not allowed ")
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):
            group=None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("You are  not allowed ")
        return wrapper_func

    return decorator
