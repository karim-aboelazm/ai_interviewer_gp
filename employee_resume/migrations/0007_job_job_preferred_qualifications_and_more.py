# Generated by Django 5.0.4 on 2024-05-06 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "employee_resume",
            "0006_interviewquestion_job_interviewquestionreview_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="job_preferred_qualifications",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="job",
            name="job_requirements",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="job",
            name="job_responsibilities",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="job",
            name="job_salary",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
