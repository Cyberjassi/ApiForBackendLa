from django.urls import path
from . import views

urlpatterns = [
    path('teacher/',views.TeacherList.as_view()),
    path('teacher/<int:pk>/',views.TeacherDetail.as_view()),
    path('teacher-login',views.teacher_login),#
    path('category/',views.CategoryList.as_view()),
    path('course/',views.CourseList.as_view()),
    path('course-chapters/<int:course_id>',views.CourseChapterList.as_view()),
    # path('chapter/',views.ChapterList.as_view()),
    path('chapter/<int:pk>',views.ChapterDetailView.as_view()),
    path('teacher-courses/<int:teacher_id>',views.TeacherCourseList.as_view()),

    path('teacher-courses-detail/<int:pk>',views.TeacherCourseDetail.as_view()),
    path('student/',views.StudentList.as_view()),
    path('student-login/',views.student_login),
    path('student-enroll-course/',views.StudentEnrollCourseList.as_view()),
    path('fatch-enroll-status/<int:student_id>/<int:course_id>',views.fatch_enroll_status),
    path('fatch-all-enrolled-students/<int:teacher_id>',views.EnrollStudentList.as_view()),
    path('fatch-enrolled-students/<int:course_id>',views.EnrollStudentList.as_view()),
    path('course-rating/',views.CourseRatingList.as_view()),

    path('fatch-rating-status/<int:student_id>/<int:course_id>',views.fatch_rating_status),
 
]