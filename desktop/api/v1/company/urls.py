from django.urls import path
from api.v1.company.member.views import MemberView

urlpatterns = [
    path('member/', MemberView.as_view(), name="get_list"),
    path('member/<int:pk>/', MemberView.as_view(), name="get_one")

]













