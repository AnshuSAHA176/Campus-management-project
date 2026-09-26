
from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.account.urls')),
     path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path('api/',include('apps.academics.urls')),
    path('room/',include('apps.rooms.urls')),
    path('scheduling/',include('apps.scheduling.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
]
