from django.urls import path
from api.v1.education.course.views import CourseView
from api.v1.education.group.views import GroupView
from api.v1.education.group_student.views import GrView

urlpatterns = [
    path('course/', CourseView.as_view(), name='course_get_list'),
    path('course/<int:pk>/', CourseView.as_view(), name='course_get_one'),

    path('group/', GroupView.as_view(), name='course_get_list'),
    path('group/<int:pk>/', GroupView.as_view(), name='course_get_one'),

    path('gr/', GrView.as_view(), name='course_get_list'),
    path('gr/<int:pk>/', GrView.as_view(), name='course_get_one'),


]