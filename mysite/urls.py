"""
"""
from django.contrib import admin
from django.urls import include, path
from MarketBot import views
from django.conf import settings  # new
from django.conf.urls.static import static  # new
from venipbot import urls

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('venipbot/', include('venipbot.urls')),
    path('payment/', views.payment),
    path('bitrix/', views.bitrix),
]
if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
