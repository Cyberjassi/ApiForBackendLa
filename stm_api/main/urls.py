from django.urls import path
from . import views

urlpatterns = [
    path('teacher/',views.TeacherList.as_view()),
    path('teacher/<int:pk>/',views.TeacherDetail.as_view()),
    path('teacher/dashboard/<int:pk>/',views.TeacherDashboard.as_view()),
    path('teacher/change-password/<int:teacher_id>/',views.teacher_change_password),
    path('teacher-login/',views.teacher_login),#
    path('category/',views.CategoryList.as_view()),
    path('course/',views.CourseList.as_view()),
    path('course-chapters/<int:course_id>',views.CourseChapterList.as_view()),
    # path('chapter/',views.ChapterList.as_view()),
    path('chapter/<int:pk>',views.ChapterDetailView.as_view()),
    path('teacher-courses/<int:teacher_id>',views.TeacherCourseList.as_view()),

    path('teacher-courses-detail/<int:pk>',views.TeacherCourseDetail.as_view()),
    path('student/',views.StudentList.as_view()),
    path('student/<int:pk>/',views.StudentDetail.as_view()),
    path('student/dashboard/<int:pk>/',views.StudentDashboard.as_view()),

    path('student/change-password/<int:student_id>/',views.student_change_password),
    path('student-login/',views.student_login),
    path('student-enroll-course/',views.StudentEnrollCourseList.as_view()),
    path('fatch-enroll-status/<int:student_id>/<int:course_id>',views.fatch_enroll_status),
    path('fatch-all-enrolled-students/<int:teacher_id>',views.EnrolledStudentList.as_view()),
 
    path('fatch-enrolled-students/<int:course_id>',views.EnrolledStudentList.as_view()),
    path('fatch-enrolled-courses/<int:student_id>',views.EnrolledStudentList.as_view()),
    path('fatch-recommended-courses/<int:studentId>',views.CourseList.as_view()),
    path('course-rating/',views.CourseRatingList.as_view()),

    path('fatch-rating-status/<int:student_id>/<int:course_id>',views.fatch_rating_status),

    path('fatch-rating-status/<int:student_id>/<int:course_id>',views.fatch_rating_status),
    path('student-add-favorite-course/',views.StudentFavoriteCourseList.as_view()),
    path('student-remove-favorite-course/<int:course_id>/<int:student_id>',views.remove_favorite_course),
    path('fatch-favorite-status/<int:student_id>/<int:course_id>',views.fatch_favorite_status),
    path('fatch-favorite-courses/<int:student_id>',views.StudentFavoriteCourseList.as_view()),
    path('student-assignment/<int:student_id>/<int:teacher_id>',views.AssignmentList.as_view()),
    path('my-assignments/<int:student_id>/',views.MyAssignmentList.as_view()),
    path('update-assignments/<int:pk>/',views.UpdateAssignmentList.as_view()),
    path('student/fetch-all-notification/<int:student_id>/',views.NotificationList.as_view()),
    path('save-notification/',views.NotificationList.as_view()),
 
]