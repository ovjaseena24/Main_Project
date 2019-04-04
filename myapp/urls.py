from django.conf import settings
from django.urls import path,include
from . import views
from django.conf.urls.static import static





urlpatterns = [
    #path('login/',views.login,name='login'),
    path('login/', views.user_login, name="login"),
    path('register/',views.register,name='register'),
    path('upload/',views.upload,name='upload'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)