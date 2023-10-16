from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,LoginSerializer,LogoutSerializer
from .leaveManagement import add_leave_with_calculation
from django.http import JsonResponse
from django.core.cache import cache
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import *
import json

# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        username = serializer.validated_data['username']
        userId = User.objects.get(username = username).id
        return JsonResponse({
            "message":"User registered successfully",
            "data":user_data,
            "id":userId
        },
        status=  status.HTTP_201_CREATED
        )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        userId = User.objects.get(username = username).id
        return JsonResponse({
            "message":"User logged in successfully",
            "id":userId,
            "data":serializer.data,
        },
        status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def send_otp(request):
    email = request.data.get('email')
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User not found with this email"}, status=status.HTTP_404_NOT_FOUND)
    
    otp = get_random_string(length=4, allowed_chars='1234567890')
    cache.set(email, otp, timeout=300)
    
    subject = 'Password Reset OTP'
    message = f'Your OTP for password reset is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
    except : 
        return Response({"message":"Faild to send OTP"}, status=status.HTTP_408_REQUEST_TIMEOUT)


@api_view(['POST'])
def confirm_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    cached_otp = cache.get(email)
    if cached_otp is None or cached_otp != otp:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    
    if password != confirm_password:
        return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
    
    cached_otp = cache.get(email)
    if cached_otp is None:
        return Response({"message": "OTP expired or not requested"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User not found with this email"}, status=status.HTTP_404_NOT_FOUND)
    
    user.set_password(password)
    user.save()
    
    cache.delete(email)
    
    subject = 'Password changed'
    message = f'Your password has been changed successfully,your new password is {password}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
    except:
        return Response({"message":"Password reset successfull,but failed to send notification mail due to timeout"}, status=status.HTTP_408_REQUEST_TIMEOUT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_employee_view(request):
    if request.method == 'POST' and request.user.isAdmin == True:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_200_OK)
    else:
        return JsonResponse({
            "status":"failed",
            "message":"User not authorised"
        },
        status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def getAllEmployees(request):
    user_fields = User.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).order_by('id').values(
    'id',
    'username',
    'full_name',
    'emplyeeIdentficationCode',
    'joining_date',
    'phone',
    'department',
    'designation'
)

    user_data = [
        {
            'id': user['id'],
            'username': user['username'],
            'full_name': user['full_name'],
            'emplyeeIdentficationCode': user['emplyeeIdentficationCode'],
            'joining_date': user['joining_date'],
            'phone': user['phone'],
            'department': user['department'],
            'designation': user['designation']
        }
        for user in user_fields
    ]

    return JsonResponse({'data': user_data})

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user(request):
    try:
        if request.user.isAdmin == False:
            raise Exception("user not authorised")
        
        else:
            data = json.loads(request.body)
            if data['email']:
                user = User.objects.get(email = data['email'])
                userId = user.id
                email = data['email']
                username = data['username']
                password = data['password']
                confirmPassword = data['confirmPassword']
                first_name = data['first_name']
                last_name = data['last_name']
                empId = data['emplyeeIdentficationCode']
                joining_date =  data['joining_date']
                phone = data['phone']
                department = data['department']
                designation = data['designation']

                if password != "" and password == confirmPassword:
                    user.set_password(password)
                    user.save()

                User.objects.filter(id = userId).update(
                    email=email,
                    username = username if username else "",
                    first_name=first_name if first_name else "",
                    last_name=last_name if last_name else "",
                    emplyeeIdentficationCode=empId if empId else "",
                    joining_date=joining_date if joining_date else "",
                    phone=phone if phone else "",
                    department=department if department else "",
                    designation=designation if designation else ""
                )

            return JsonResponse({
                "message":"User updated successfully"
            },
            status = status.HTTP_200_OK)


    except Exception as ex:
        return JsonResponse({
            "message":str(ex)
        },
        status = status.HTTP_401_UNAUTHORIZED)

    

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    try:
        if request.user.isAdmin == False:
            raise Exception("user not authorised")
        
        data = json.loads(request.body)
        user = User.objects.get(email=data['email'])
        user.delete()
        return JsonResponse({
            "message": f"User {user.username} with employee ID - {user.emplyeeIdentficationCode} deleted from the employee list successfully",
            "status":"success"
        },
        status = status.HTTP_200_OK)

        
    except Exception as ex:
        return JsonResponse({
            "message": str(ex),
            "status":"failed"
        },
        status = status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def user_detail_view(request):
#     userData = json.loads(request.body)
#     if userData['searchId'] == 'username':
#         user = get_object_or_404(User, username=userData['username'])
#     elif userData['searchId'] == 'email':
#         user = get_object_or_404(User, email=userData['email'])
#     elif userData['searchId'] == 'emplyeeIdentficationCode':
#         user = get_object_or_404(User, emplyeeIdentficationCode=userData['emplyeeIdentficationCode'])
#     if userData['searchId'] == 'designation':
#         designation = userData['designation']
#         users = User.objects.filter(designation=designation)
        
#         user_list = []
#         for user in users:
#             user_data = {
#                 'id': user.id,
#                 'username': user.username,
#                 'fullName': user.first_name + " " + user.last_name,
#                 'email': user.email,
#                 'emplyeeIdentficationCode': user.emplyeeIdentficationCode,
#                 'joining_date': user.joining_date,
#                 'phone': user.phone,
#                 'department': user.department, 
#                 'designation': user.designation,
#             }
#             user_list.append(user_data)

#         return Response(user_list)

#     user = {
#         'id': user.id,
#         'username': user.username,
#         'fullName':user.first_name+" "+user.last_name,
#         'email': user.email,
#         'emplyeeIdentficationCode': user.emplyeeIdentficationCode,
#         'joining_date': user.joining_date,
#         'phone': user.phone,
#         'department': user.department,
#         'designation': user.designation,
#     }

#     return JsonResponse(user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_leave(request):
    user = request.user
    data = request.data

    leave_type = data.get('leave_type')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    return add_leave_with_calculation(user, leave_type, start_date_str, end_date_str)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leave_history(request):
    user = request.user
    leave_history = Leave.objects.filter(user=user)
    leave_data = [
        {
            'leave_type': leave.leave_type,
            'start_date': leave.start_date,
            'end_date': leave.end_date
        }
        for leave in leave_history
    ]
    return Response(leave_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_holiday(request):
    if request.method == 'POST' and request.isAdmin == True:
        data = json.loads(request.body)
        date_str = data['date']
        name = data['name']

        if not date_str:
            return JsonResponse({"message": "Date is required"}, status=400)
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({"message": "Invalid date format"}, status=400)

        if Holiday.objects.filter(date=date).exists():
            return JsonResponse({"message": "Holiday with this date already exists"}, status=400)

        Holiday.objects.create(date=date, name=name)

        return JsonResponse({"message": "Holiday added successfully"}, status=201)
    
    return JsonResponse({"message": "Method not allowed"}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_holidays(request):
    holidays = Holiday.objects.all()
    holidays_list = [{"date": holiday.date.strftime('%Y-%m-%d'), "name": holiday.name} for holiday in holidays]
    return JsonResponse({"holidays": holidays_list})