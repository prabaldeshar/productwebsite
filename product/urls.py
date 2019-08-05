from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('add/', views.add, name='add'),
    path('<int:product_id>', views.detail, name='detail'),
    path('predict/<int:product_id>', views.post, name='post'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
