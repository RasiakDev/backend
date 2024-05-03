from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return f"Post: {self.title}"

cities = (
    ("Durres", "Durres"),
    ("Tirane", "Tirane")
)
units = (
    ("gr","gr"),
    ("Kg", "Kg"),
    ("ml", "ml"),
    ("Lt", "Lt"),
    ("Cope", "Cope")
)

class Category(models.Model):
    category=models.CharField(max_length=50, primary_key=True)

    def __str__(self) -> str:
        return self.category

class Product(models.Model):
    name=models.CharField(max_length=255, null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description=models.TextField(max_length=255, null=True, blank=True)
    # barcode=models.CharField(max_length=13)
    unit=models.CharField(max_length=10, choices=units, null=True)
    quantity=models.IntegerField( null=True)
    # size=models.IntegerField()
    price=models.FloatField( null=True)
    total=models.FloatField( null=True)
    reviews=models.FloatField( null=True)
    reviewCount=models.IntegerField( null=True)
    image=models.ImageField(upload_to=f'products', null=True)

    def __str__(self) -> str:
        return self.name

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Formati email nuk eshte i sakte")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email=None, password=None,**extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self,email=None, password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    # phone = models.CharField(max_length=14)
    name = models.CharField(max_length=100, null=True)
    # last_name = models.CharField(max_length=100)
    # city=models.CharField(max_length=15,choices = cities, default='Durres')
    # adress=models.CharField(max_length=255)
    date_joined=models.DateField(default=timezone.now,null=True)
    last_login=models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self) -> str:
        return self.first_name
    def get_short_name(self) -> str:
        return self.first_name or self.email.split('@')[0]
    def __str__(self) -> str:
        return self.username or self.email