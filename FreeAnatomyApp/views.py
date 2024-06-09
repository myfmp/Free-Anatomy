from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime, timedelta
from .bot import RunBot
def main(request):
    cookie_1 = "email"
    cookie_2 = "password"
    cookie_3 = "link"
    if cookie_1 in request.COOKIES:
      cmail = request.COOKIES[cookie_1]
      cpassword = request.COOKIES[cookie_2]
      clink = request.COOKIES[cookie_3]
      return render(request, 'index.html', {'email': cmail, 'password': cpassword, 'link': clink})
    else:
        if request.method == 'POST':
          Is_submited = request.POST.get('submit_state')
          if Is_submited == 'True':
            account_info = RunBot()
            expiration_time = datetime.now() + timedelta(days=3)
            # Set cookies with appropriate attributes
            response = JsonResponse({'Account': account_info})
            response.set_cookie('email', account_info[0], expires=expiration_time, secure=settings.SESSION_COOKIE_SECURE, httponly=True)
            response.set_cookie('password', account_info[1], expires=expiration_time, secure=settings.SESSION_COOKIE_SECURE, httponly=True)
            response.set_cookie('link', account_info[2], expires=expiration_time, secure=settings.SESSION_COOKIE_SECURE, httponly=True)
            return response
        return render(request, "index.html")
