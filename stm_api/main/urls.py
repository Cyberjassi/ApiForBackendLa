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

#Courses-
    path('course/',views.CourseList.as_view()),
    path('course/<int:pk>',views.CourseDetailView.as_view()),
    path('popular-courses/',views.CourseRatingList.as_view()),
    # path('search-courses/<str:searchString>',views.CourseList.as_view()),
    path('update-view/<int:course_id>',views.update_view),
    path('course-chapters/<int:course_id>',views.CourseChapterList.as_view()),
    path('chapter/',views.ChapterList.as_view()),
    path('fatch-recommended-courses/<int:studentId>',views.CourseList.as_view()),
    path('course-rating/',views.CourseRatingList.as_view()),
    path('student-testimonial/',views.CourseRatingList.as_view()),


# Students-
    path('student/',views.StudentList.as_view()),
    path('student/<int:pk>/',views.StudentDetail.as_view()),
    path('verify-student/<int:student_id>/',views.verify_student_via_otp.as_view()),
    path('student/dashboard/<int:pk>/',views.StudentDashboard.as_view()),
    path('student/change-password/<int:student_id>/',views.student_change_password),
    path('student-login/',views.student_login.as_view()),
    path('student-enroll-course/',views.StudentEnrollCourseList.as_view()),
    path('fatch-enroll-status/<int:student_id>/<int:course_id>',views.fatch_enroll_status.as_view()),
    path('fatch-all-enrolled-students/<int:teacher_id>',views.EnrolledStudentList.as_view()),
    path('fatch-enrolled-students/<int:course_id>',views.EnrolledStudentList.as_view()),
    path('fatch-enrolled-courses/<int:student_id>',views.EnrolledStudentList.as_view()),
    path('student-add-favorite-course/',views.StudentFavoriteCourseList.as_view()),
    path('student-remove-favorite-course/<int:course_id>/<int:student_id>',views.remove_favorite_course),
    path('fatch-favorite-status/<int:student_id>/<int:course_id>',views.fatch_favorite_status),
    path('fatch-favorite-courses/<int:student_id>',views.StudentFavoriteCourseList.as_view()),
    path('student/fetch-all-notification/<int:student_id>/',views.NotificationList.as_view()),
    path('student-forgot-password/',views.student_forgot_password.as_view()),
    path('student-change-password/<int:student_id>/',views.student_changne_password.as_view()),



# Assignments   
    path('student-assignment/<int:student_id>/<int:teacher_id>',views.AssignmentList.as_view()),
    path('my-assignments/<int:student_id>/',views.MyAssignmentList.as_view()),
    path('update-assignments/<int:pk>/',views.UpdateAssignmentList.as_view()),

# Study Material-
    path('study-materials/<int:course_id>',views.StudyMaterialList.as_view()),
    path('study-material/<int:pk>',views.StudyMaterialDetailView.as_view()),
    path('user/study-materials/<int:course_id>',views.StudyMaterialList.as_view()),

#down Navbar-
    path('faq/',views.FaqList.as_view()),
    path('pages/',views.FlatePageList.as_view()),
    path('pages/<int:pk>/<str:page_slug>',views.FlatePageDetail.as_view()),
    path('contact/',views.ContactList.as_view()),

#Quiz-
    path('quiz/',views.Quizlist.as_view()),
    path('teacher-quiz/<int:teacher_id>',views.TeacherQuizList.as_view()),
    path('teacher-quiz-detail/<int:pk>',views.TeacherQuizDetail.as_view()),
    path('quiz/<int:pk>',views.QuizDetailView.as_view()),
    path('quiz-questions/<int:quiz_id>/',views.QuizQuestionList.as_view()),
    path('quiz-questions/<int:quiz_id>/<int:limit>',views.QuizQuestionList.as_view()),
    path('fetch-quiz-assign-status/<int:quiz_id>/<int:course_id>',views.fetch_quiz_assign_status),
    path('quiz-assign-course/',views.CourseQuizList.as_view()),
    path('fetch-assigned-quiz/<int:course_id>',views.CourseQuizList.as_view()),
    path('attempt-quiz/',views.AttemptQuizList.as_view()),
    path('quiz-questions/<int:quiz_id>/next-question/<int:question_id>/',views.QuizQuestionList.as_view()),
    path('fetch-quiz-attempt-status/<int:quiz_id>/<int:student_id>',views.fetch_quiz_attempt_status),
    path('fetch-quiz-result/<int:quiz_id>/<int:student_id>',views.fetch_quiz_attempt_status),
    path('attempted-quiz/<int:quiz_id>',views.AttemptQuizList.as_view()),
    path('attempted-quiz/<int:quiz_id>',views.AttemptQuizList.as_view()),

# others-
    path('chapter/<int:pk>',views.ChapterDetailView.as_view()),
    path('fatch-rating-status/<int:student_id>/<int:course_id>',views.fatch_rating_status),
    path('save-notification/',views.NotificationList.as_view()),
    path('category/',views.CategoryList.as_view()),

#Messages-
    path('send-message/<int:teacher_id>/<int:student_id>',views.save_teacher_student_msg.as_view()),
    path('get-messages/<int:teacher_id>/<int:student_id>',views.MessageList.as_view()),
    path('send-group-message/<int:teacher_id>',views.save_teacher_student_group_msg.as_view()),


]