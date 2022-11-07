from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from localflavor.br.models import BRCPFField, BRPostalCodeField, BRStateField

GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino')
]

STATE_CHOICES = [
    ('Acre', 'Acre'),
    ('Alagoas', 'Alagoas'),
    ('Amapá', 'Amapá'),
    ('Amazonas', 'Amazonas'),
    ('Bahia', 'Bahia'),
    ('Ceará', 'Ceará'),
    ('Distrito Federal', 'Distrito Federal'),
    ('Espírito Santo', 'Espírito Santo'),
    ('Goiás', 'Goiás'),
    ('Maranhão', 'Maranhão'),
    ('Mato Grosso', 'Mato Grosso'),
    ('Mato Grosso do Sul', 'Mato Grosso do Sul'),
    ('Minas Gerais', 'Minas Gerais'),
    ('Pará', 'Pará'),
    ('Paraíba', 'Paraíba'),
    ('Paraná', 'Paraná'),
    ('Pernambuco', 'Pernambuco'),
    ('Piauí', 'Piauí'),
    ('Rio de Janeiro', 'Rio de Janeiro'),
    ('Rio Grande do Norte', 'Rio Grande do Norte'),
    ('Rio Grande do Sul', 'Rio Grande do Sul'),
    ('Rondônia', 'Rondônia'),
    ('Roraima', 'Roraima'),
    ('Santa Catarina', 'Santa Catarina'),
    ('São Paulo', 'São Paulo'),
    ('Sergipe', 'Sergipe'),
    ('Tocantins', 'Tocantins'),

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
    # User details
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=255, verbose_name='Nome')
    cpf = BRCPFField(verbose_name='CPF')
    phone = models.CharField(max_length=11, verbose_name='Telefone')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name='Gênero')
    birth_date = models.DateField(verbose_name='Data de nascimento')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cpf', 'phone', 'gender', 'birth_date']

    def __str__(self):
        return self.email
        

class Address(models.Model):
    user = models.ForeignKey(MyUser, verbose_name='Cliente', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Nome do endereço', max_length=150, blank=True)
    CEP = BRPostalCodeField(verbose_name='CEP')
    address = models.CharField(verbose_name='Endereço', max_length=255)
    district = models.CharField(verbose_name='Bairro', max_length=255)
    city = models.CharField(verbose_name='Cidade', max_length=150)
    state = models.CharField(choices=STATE_CHOICES, max_length=25)
    created = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)
    default = models.BooleanField(verbose_name='Endereço Padrão', default=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return 'Endereço'