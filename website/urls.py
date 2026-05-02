from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('profile/', views.profile_view, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)