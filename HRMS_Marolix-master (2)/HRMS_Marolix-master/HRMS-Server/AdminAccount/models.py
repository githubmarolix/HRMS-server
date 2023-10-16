from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    emplyeeIdentficationCode = models.CharField(max_length=50,default='')
    joining_date = models.DateField(default='')
    phone = models.CharField(max_length=15,default='')
    isAdmin = models.BooleanField(default=False)
    casual_leave_days = models.PositiveIntegerField(default=0)
    medical_leave_days = models.PositiveIntegerField(default=0)
    lop_leave_days = models.PositiveIntegerField(default=0)
    department = models.CharField(max_length=255,default='')
    DESIGNATION_CHOICES = [
        ('des1', 'Designation 1'),
        ('des2', 'Designation 2'),
        ('des3', 'Designation 3'),
        ('des3', 'Designation 4'),
        ('des3', 'Designation 5'),
        ('des3', 'Designation 6'),
        ('des3', 'Designation 7'),
        ('des3', 'Designation 8'),
        ('des3', 'Designation 9'),
        ('des10', 'Designation 10'),
    ]

    designation = models.CharField(
        max_length=255,
        choices=DESIGNATION_CHOICES,
        default='des1'
    )

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    

class Leave(models.Model):
    LEAVE_TYPES = [
        ('casual', 'Casual'),
        ('medical', 'Medical'),
        ('lop', 'Loss of Pay'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} Leave"
    
class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.name