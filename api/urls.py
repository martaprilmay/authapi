from django.urls import path

from .views import reg, login, status

app_name = 'ai'

urlpatterns = [
    path('reg/', reg, name='registration'),
    path('login/', login, name='login'),
    path('status/', status, name='status'),
]