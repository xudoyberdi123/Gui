from django.urls import path
from api.v1.company.member.views import MemberView
from api.v1.company.position.views import PosView


urlpatterns = [
    path('member/', MemberView.as_view(), name="get_list_mem"),
    path('member/<int:pk>/', MemberView.as_view(), name="get_one_mem"),

    path('position/', PosView.as_view(), name="get_list_pos"),
    path('position/<int:pk>/', PosView.as_view(), name="get_one_pos")

]












