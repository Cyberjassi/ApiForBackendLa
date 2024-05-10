from rest_framework.permissions import BasePermission

class TeacherStudent(BasePermission):
    def has_permission(self, request, view):
        if request.GET.get('role') == 'teacher':
            return True
        elif request.GET.get('role') == 'student':
            return True
        else:
            return False