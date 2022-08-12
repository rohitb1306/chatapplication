from django.urls import path
from . import views
urlpatterns = [
    path('profile/',views.Profile.as_view(),name='profile'),
    path('signout',views.Signout.as_view(),name="signout"),
    path('signup',views.Signup.as_view(),name="signup")
]