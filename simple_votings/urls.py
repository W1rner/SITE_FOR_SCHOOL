"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from main import views
# from django.contrib.auth import views as auth_views
# from main.views import get_menu_context

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page),
    path('login/', views.login_page),
    path('votings/', views.votings_page),
    path('votings/vote/participants', views.vote_users_page),
    path('registration/', views.registration_page),
    path('logout/', views.logout_user),
    path('votings/vote/', views.vote_page),
    path('votings/vote/user_voted', views.user_voted_page),
    path('user/', views.user_profile_page),
    path('user/edit_profile/', views.user_edit_profile_page),
    path('user/create_voting', views.create_voting_page),
    path('error/', views.error_page),
    path('user/history', views.user_history_page),
    path('complaints_&_suggestions/', views.complaints),
    path('complaints_&_suggestions/create', views.create_cas_page),
    # path('', views.index_page, name='index'),
    # path('time/', views.time_page, name='time'),
    # path(
    #     'login/',
    #     auth_views.LoginView.as_view(
    #         extra_context={
    #             'menu': get_menu_context(),
    #             'pagename': 'Авторизация'
    #         }
    #     ),
    #     name='login'
    # ),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'main.views.custom_404_page'
handler403 = 'main.views.custom_403_page'
