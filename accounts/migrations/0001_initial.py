# Generated by Django 3.2.13 on 2022-07-28 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apps', '0001_initial'),
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('log', models.CharField(max_length=300)),
                ('amount', models.IntegerField(default=0)),
                ('code', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('a', 'admin'), ('c', 'customer')], default='c', max_length=20)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('utility_name', models.CharField(blank=True, max_length=200, null=True)),
                ('utility_short_name', models.CharField(blank=True, max_length=50, null=True)),
                ('utility_state', models.CharField(blank=True, max_length=50, null=True)),
                ('utility_district', models.CharField(blank=True, max_length=50, null=True)),
                ('utility_country', models.CharField(blank=True, max_length=50, null=True)),
                ('utility_postalcode', models.CharField(blank=True, max_length=20, null=True)),
                ('utility_address', models.TextField(blank=True, max_length=200, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=50, null=True)),
                ('contact_phnum', models.CharField(blank=True, max_length=15, null=True)),
                ('contact_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('contact_designation', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_landline', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_person', models.CharField(blank=True, max_length=200, null=True)),
                ('emergency_altperson', models.CharField(blank=True, max_length=200, null=True)),
                ('emergency_mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('emergency_altmobile', models.CharField(blank=True, max_length=200, null=True)),
                ('emergency_officeaddress', models.TextField(blank=True, max_length=200, null=True)),
                ('emergency_altofficeaddress', models.TextField(blank=True, max_length=200, null=True)),
                ('info_created_at', models.DateTimeField(auto_now_add=True)),
                ('info_updated_at', models.DateTimeField(auto_now=True)),
                ('se_coins', models.IntegerField(blank=True, default=999, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=200, null=True)),
                ('admin', models.BooleanField(default=False)),
                ('plan_active', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('apps', models.ManyToManyField(related_name='apps', to='apps.applists')),
                ('plans', models.ManyToManyField(to='plans.Plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='notifications')),
                ('body', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
                ('url_name', models.CharField(blank=True, default='View', max_length=255, null=True)),
                ('notified_time', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(editable=False, max_length=16, null=True, unique=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to='accounts.profile')),
            ],
        ),
    ]
