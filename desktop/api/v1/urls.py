from django.urls import path, include


urlpatterns = [
    path('company/', include('api.v1.company.urls')),
    path('geo/', include('api.v1.geo.urls')),
    path('edu/', include('api.v1.education.urls')),

]




