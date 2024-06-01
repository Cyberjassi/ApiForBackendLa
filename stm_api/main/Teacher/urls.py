from django.urls import path
from . import views
# from .views import TeacherLoginApiView


urlpatterns = [
#Teachers-
    path('teacher/',views.TeacherList.as_view()),
    path('teacher/<int:pk>/',views.TeacherDetail.as_view()),
    path('teacher/dashboard/<int:pk>/',views.TeacherDashboard.as_view()),
    path('teacher/change-password/<int:teacher_id>/',views.teacher_change_password.as_view()),
    path('teacher-login/',views.teacher_login.as_view()),#
    path('popular-teachers/',views.TeacherList.as_view()),
    path('verify-teacher/<int:teacher_id>/',views.verify_teacher_via_otp.as_view()),
    path('teacher-courses/<int:teacher_id>',views.TeacherCourseList.as_view()),
    path('teacher-courses-detail/<int:pk>',views.TeacherCourseDetail.as_view()),
    path('teacher-forgot-password/',views.teacher_forgot_password.as_view()),
    path('teacher-change-password/<int:teacher_id>/',views.teacher_change_password.as_view()),

]