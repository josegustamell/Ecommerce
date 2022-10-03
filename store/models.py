from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino')
]

SIZE_CHOICES = [
    ('PP', 'PP'),
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG')
]

class MyAccountManager(BaseUserManager):
    def create_superuser(self, email, name, password, cpf, gender, birth_date, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, name, password, cpf, gender, birth_date, **other_fields)


    def create_user(self, email, name, password, cpf, gender, birth_date, **other_fields):
        if not email:
            raise ValueError('You must provide an email address.')
        if not cpf:
            raise ValueError('You must provide your cpf.')
        if not birth_date:
            raise ValueError('You must provide your birth date.')

        user = self.model(email=self.normalize_email(email), name=name, cpf=cpf, gender=gender, birth_date=birth_date, **other_fields)
        user.set_password(password)
        user.save()
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    phone = models.CharField(max_length=11)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cpf', 'phone', 'gender', 'birth_date']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Categoria')
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    slug = models.SlugField(max_length=255)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, blank=True, null=True)
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)
    sold = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')