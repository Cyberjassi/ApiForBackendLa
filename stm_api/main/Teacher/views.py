class TeacherList(APIView):
    pagination_class = MyPagination  # Assuming MyPagination is your custom pagination class

    def get(self, request):
        if 'popular' in request.GET:
            # Custom SQL query to get teachers ordered by the popularity of their courses
            # main is our app name in that query
            sql = "SELECT *, COUNT(c.id) as total_course FROM main_teacher as t INNER JOIN main_course as c ON c.teacher_id=t.id GROUP BY t.id ORDER BY total_course desc"
            queryset = models.Teacher.objects.raw(sql)
        else:
            queryset = models.Teacher.objects.all()

        # Pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        
        serializer = TecherSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TecherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # change-
# class TeacherList(generics.ListCreateAPIView):
#    queryset=models.Teacher.objects.all()
#    serializer_class=TecherSerializer
   #withour authenticate we can'nt able to see and do operations
   # permission_classes = [permissions.IsAuthenticated]
   
   #Will---
   # def get_queryset(self):
   #    if 'popular' in self.request.GET:
   #       sql="SELECT *,COUNT(c.id) as total_course FROM main_teacher as t INNER JOIN main_course as c ON c.teacher_id=t.id GROUP BY t.id ORDER BY total_course desc"
   #       return models.Teacher.objects.raw(sql)
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.Teacher.objects.all()
   serializer_class=TecherSerializer
   # permission_classes = [permissions.IsAuthenticated]

class TeacherDashboard(generics.RetrieveAPIView):
   queryset = models.Teacher.objects.all()
   serializer_class=TeacherDashboardSerializer

#mt
class TeacherCourseList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
   #  it is use for overide course so that we car retriewe specific course according to teacher id
    def get_queryset(self):
        # Retrieve teacher ID from URL kwargs
        teacher_id = self.kwargs['teacher_id']
        
        # Retrieve teacher object based on ID
        teacher = models.Teacher.objects.get(pk=teacher_id)
        
        # Filter courses by teacher
        return models.Course.objects.filter(teacher=teacher)

#through that teacher can do curd

class TeacherCourseDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Course.objects.get(pk=pk)
        except models.Course.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# will-
# class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Course.objects.all()
#     serializer_class = CourseSerializer

# it responsible for handle frontened request means if login information is match then it response True otherwise False

# @method_decorator(csrf_exempt, name='dispatch')

# change and will itself-
class teacher_login(APIView):
    def post(self, request):
     
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print("this is teacher data",request.body)
            # print(email, password)
            
            try:
                teacher_data = models.Teacher.objects.filter(email=email, password=password).first()
            except ObjectDoesNotExist:
                teacher_data = None

            if teacher_data:
                if not teacher_data.verify_status:
                    return JsonResponse({'bool': False, 'msg': 'Accuount is not verified'})
                else:
                    token = get_tokens_for_user(teacher_data)
                    return JsonResponse({'token':token,'bool': True, 'teacher_id': teacher_data.id})
            else:
                return JsonResponse({'bool': False,'msg':'Invalied Email or password'})
        except JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    def get(self, request):
        return JsonResponse({'error': 'GET method not allowed'}, status=405)
    
     
class verify_teacher_via_otp(APIView):
    def post(self, request, teacher_id):
        otp_digit = request.data.get('otp_digit')
        print(otp_digit)  # Using request.data for POST data
        verify = models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).first()
        if verify:
            models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).update(verify_status=True)
            return JsonResponse({'bool': True, 'teacher_id': verify.id})
        else:
            return JsonResponse({'bool': False})
        
class teacher_forgot_password(APIView):
    def post(self, request):
        email = request.data.get('email')
        print(email)  # Using request.data for POST data
        verify = models.Teacher.objects.filter(email=email).first()
        if verify:
            link=f"http://localhost:3000/teacher-change-password/{verify.id}/"
            send_mail(
                "Change Password",
                "Please Verify Your Account",
                "settings.EMAIL_HOST_USER",
                [email],  # Use 'email' instead of 'self.email'
                fail_silently=False,
                html_message=f"<p>Your OTP is </p><p>{link}</p>"  # Use 'otp_digit' instead of 'self.otp_digit'
        )
            return JsonResponse({'bool': True, 'msg': 'please check your email'})
        else:
            return JsonResponse({'bool': False,'msg':'Invalid Email!!'})
        
class teacher_change_password(APIView):
    def get(self, request, teacher_id):
            return JsonResponse({'bool': False, 'msg': 'Get Method not Allowed!'})

    def post(self, request, teacher_id):
        try:
            password = request.data.get('password')
            if password is None:
                return JsonResponse({'bool': False, 'msg': 'Password field is missing from the request!'}, status=status.HTTP_400_BAD_REQUEST)
            
            teacher_data = models.Teacher.objects.get(id=teacher_id)
            teacher_data.password = password
            teacher_data.save()
            return JsonResponse({'bool': True, 'msg': 'Password has been changed!'})
        
        except models.Teacher.DoesNotExist:
            return JsonResponse({'bool': False, 'msg': 'Teacher not found!'}, status=status.HTTP_404_NOT_FOUND)

