# Generated by Django 3.2 on 2022-11-02 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_address_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(choices=[('Acre', 'Acre'), ('Alagoas', 'Alagoas'), ('Amapá', 'Amapá'), ('Amazonas', 'Amazonas'), ('Bahia', 'Bahia'), ('Ceará', 'Ceará'), ('Distrito Federal', 'Distrito Federal'), ('Espírito Santo', 'Espírito Santo'), ('Goiás', 'Goiás'), ('Maranhão', 'Maranhão'), ('Mato Grosso', 'Mato Grosso'), ('Mato Grosso do Sul', 'Mato Grosso do Sul'), ('Minas Gerais', 'Minas Gerais'), ('Pará', 'Pará'), ('Paraíba', 'Paraíba'), ('Paraná', 'Paraná'), ('Pernambuco', 'Pernambuco'), ('Piauí', 'Piauí'), ('Rio de Janeiro', 'Rio de Janeiro'), ('Rio Grande do Norte', 'Rio Grande do Norte'), ('Rio Grande do Sul', 'Rio Grande do Sul'), ('Rondônia', 'Rondônia'), ('Roraima', 'Roraima'), ('Santa Catarina', 'Santa Catarina'), ('São Paulo', 'São Paulo'), ('Sergipe', 'Sergipe'), ('Tocantins', 'Tocantins')], max_length=25),
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]
