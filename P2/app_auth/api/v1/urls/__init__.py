from django.urls import path, include


app_name = 'app_auth_v1'

urlpatterns = [
    path('', include('app_auth.api.v1.urls.auth_urls')),
    path('', include('app_auth.api.v1.urls.password_urls')),
]
