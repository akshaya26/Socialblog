from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name='accounts'
urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    #template name is provided becuase by default django will look into 'registration/login.html'.So either proceed
    # above way or below commented and place login.html inside a registration directory prsent within templates directory of
    # accounts app
    # path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),#logout view has a default view
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('groups/',include('groups.urls')),

]