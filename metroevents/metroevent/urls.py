from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

#paths arranged alphabetically by name
app_name = 'metroevent'
urlpatterns = [ 
    # path('api/data', views.get_data, name='api-data'),

    #TEST URL
    path('login/', views.LoginView.as_view(), name="LoginView"),
    path('index/', views.IndexView.as_view(), name="IndexView"),
    path('signup/', views.SignUpView, name="SignUpView"),
    path('logout/', views.LogoutView, name="LogoutView"),
    path('homepage/', views.HomePageView.as_view(), name="HomePageView"),
    path('profile/', views.ProfileView.as_view(), name="ProfileView"),
    path('org_profile/', views.OrgProfileView.as_view(), name="OrgProfileView"),
    path('admin_dashboard/', views.AdminView.as_view(), name="AdminView"),
    path('users_admin/', views.UsersAdminView.as_view(), name="UsersAdminView"),
    path('events_admin/', views.EventsAdminView.as_view(), name="EventsAdminView"),
    path('organizers_admin/', views.OrgAdminView.as_view(), name="OrgAdminView"),
    path('requests/', views.RequestView.as_view(), name="RequestView"),
    path('addevent/', views.AddEventView.as_view(), name="AddEventView"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)