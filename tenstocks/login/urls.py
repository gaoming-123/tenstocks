from django.urls import path,include
from . import views

app_name='login'
urlpatterns = [
    path('login/', views.Login.as_view(),name='login'),
    path('register/', views.Register.as_view(),name='register'),
    path('logout/', views.Logout.as_view(),name='logout'),
    path('info/', views.InfoView.as_view(),name='info'),
    path('confirm/', views.user_confirm,name='confirm'),
    path('email/',views.send_my_email,name='send_email' ),
    # path('captcha/', include('captcha.urls')),
]
