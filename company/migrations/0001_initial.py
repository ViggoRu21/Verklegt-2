# Generated by Django 5.0.4 on 2024-05-07 14:37

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utilities_static', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='utilities_static.user')),
                ('company_ssn', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('salary_low', models.IntegerField()),
                ('salary_high', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilities_static.category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilities_static.company')),
                ('employment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilities_static.employmenttype')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.recruiter')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('status', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='utilities_static.status')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='utilities_static.user')),
                ('listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='company.joblisting')),
            ],
        ),
    ]
