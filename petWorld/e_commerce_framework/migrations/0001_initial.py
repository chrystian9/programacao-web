# Generated by Django 4.2 on 2023-05-13 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=200)),
                ('complement', models.CharField(blank=True, max_length=200, null=True)),
                ('number', models.IntegerField()),
                ('reference', models.CharField(blank=True, max_length=255)),
                ('neighborhood', models.CharField(max_length=45)),
                ('city', models.CharField(max_length=45)),
                ('state_acronym', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranão'), ('MG', 'Minas Gerais'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PE', 'Pernanbuco'), ('PI', 'Piauí'), ('PR', 'Paraná'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('RS', 'Rio Grande do Sul'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('SP', 'São Paulo'), ('TO', 'Tocantins')], max_length=2)),
                ('zip_code', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('sex', models.IntegerField(choices=[(1, 'F'), (2, 'M'), (3, 'N')])),
                ('phone_number', models.CharField(max_length=12)),
                ('date_birth', models.DateField(verbose_name='date of birth')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_commerce_framework.address')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_number', models.IntegerField(unique=True)),
                ('value', models.FloatField()),
                ('freight_rate', models.FloatField()),
                ('discount', models.FloatField()),
                ('total_value', models.FloatField()),
                ('payment_method', models.IntegerField(choices=[(1, 'CASH'), (2, 'CREDIT'), (3, 'DEBT')])),
                ('number_installments', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.FloatField()),
                ('categories', models.ManyToManyField(related_name='products', to='e_commerce_framework.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(unique=True)),
                ('date_time', models.DateTimeField(verbose_name='date of order')),
                ('status', models.IntegerField(choices=[(1, 'DONE'), (2, 'PROCESS'), (3, 'TRANSIT'), (4, 'DELIVERED'), (5, 'LATE'), (6, 'CANCELED')])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='e_commerce_framework.customer')),
                ('delivery_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_commerce_framework.address')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_commerce_framework.payment')),
                ('products', models.ManyToManyField(related_name='orders', to='e_commerce_framework.product')),
            ],
        ),
    ]