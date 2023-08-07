from django.urls import path
from.views import *

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('', home, name='home'),
    path('success/', success, name='success'),
    path('success1/', success1, name='success1'),
    path('error/', error, name='error'),
    path('reset_pass/', reset_pass, name='reset_pass'),
    path('new_pass/', new_pass, name='new_pass'),
    path('verify/<auth_token>', verify, name='verify'),
    path('reset_user_pass/<auth_token>', reset_user_pass, name='reset_user_pass'),
    path('create/', create, name='create'),
    path('see_profile/<int:id>/', see_profile, name='see_profile'),
    path('update_profile/<int:id>/', update_profile, name='update_profile'),
    path('delete/<int:id>', delete, name='delete'),
]
