from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.forms import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, password, **other_fields):
        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, first_name, password, **other_fields)


class User(AbstractUser, PermissionsMixin):
    def validate_phone_no(phone_no):
        if not (phone_no.isdigit() and len(phone_no) == 10):
            raise ValidationError('Phone number must be 10 digits')

    def validate_aadhar_no(aadhar_no):
        if not (aadhar_no.isdigit() and len(aadhar_no) == 12):
            raise ValidationError('Aadhar number must be a 12 digit number')

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    joined_date = models.DateField(blank=True, null=True)
    aadhar_no = models.CharField(
        unique=True, max_length=12, verbose_name='Aadhar Number', validators=[validate_aadhar_no], blank=True, null=True)
    phone_no = models.CharField(max_length=10, verbose_name='Phone number', validators=[
                                validate_phone_no], blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self) -> str:
        if self.last_name is None:
            return self.first_name
        return self.first_name + ' ' + self.last_name


class Certification(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    agency_name = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Participant')

    def __str__(self) -> str:
        return self.title


class Research(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    agency_name = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    users = models.ManyToManyField(
        User, verbose_name='Participants')
