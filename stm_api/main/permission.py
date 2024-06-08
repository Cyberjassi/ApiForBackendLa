from rest_framework.permissions import BasePermission
import jwt

class Teacher(BasePermission):
    message = "You are not a teacher."

    def has_permission(self, request, view):
        token_string = request.headers.get('Authorization').split(' ')[1]
        try:
            decoded_token = jwt.decode(token_string, options={"verify_signature": False})
            role = decoded_token.get('role')
            print("this is ",role)
            if role == 'teacher':
                return True
            else:
                return False
        except jwt.DecodeError as e:
            print("Error decoding token:", e)
            return False

class Student(BasePermission):
    message = "You are not a student."

    def has_permission(self, request, view):
        token_string = request.headers.get('Authorization').split(' ')[1]
        try:
            decoded_token = jwt.decode(token_string, options={"verify_signature": False})
            role = decoded_token.get('role')
            print("this is ",role)
            if role == 'student':
                return True
            else:
                return False
        except jwt.DecodeError as e:
            print("Error decoding token:", e)
            return False
