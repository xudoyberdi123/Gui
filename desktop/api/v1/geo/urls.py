from django.urls import path

from .district.views import DistrictView
from .region.views import RegionView
from .views import RegionListView, DistrictListView

urlpatterns = [
    path('region/list/', RegionListView.as_view(), name='geo_region_list'),
    path('district/<int:region>/list/', DistrictListView.as_view(), name='geo_district_list'),
    path("regions/", RegionView.as_view(), name="region_list"),
    path("regions/<int:pk>/", RegionView.as_view(), name="region_one"),
    path("districts/", DistrictView.as_view(), name="region_list"),
    path("districts/<int:pk>/", DistrictView.as_view(), name="region_one"),
]
