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
    path('index/', views.IndexView.as_view(), name="IndexView")

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)