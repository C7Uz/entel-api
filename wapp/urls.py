from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Viewset
from .router import urls


router = DefaultRouter()

urlpatterns = router.urls

# Para debug - ver todas las URLs
print("URLs disponibles:")
for url in urls:
    print(f"  {url.pattern}")

urlpatterns += [
    path('api/', include(urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
