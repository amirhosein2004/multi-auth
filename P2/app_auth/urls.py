from django.urls import path, include


urlpatterns = [
    path('v1/', include('app_auth.api.v1.urls')),
]
