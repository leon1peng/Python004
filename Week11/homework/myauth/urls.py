from django.conf.urls import url
from .views import login_f, login, home, logout, reg

urlpatterns = [
    url(r'form', login_f),
    url(r'login', login),
    url(r'home', home),
    url(r'logout', logout),
    url(r'reg', reg),
    url(r'', login_f),
]
