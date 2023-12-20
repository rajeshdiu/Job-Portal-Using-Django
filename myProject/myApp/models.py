from django.db import models

from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
    USER=[
        ('recruiter','Recruiter'),('jobseeker','JobSeeker')
    ]
    display_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    user_type=models.CharField(choices=USER,max_length=120)
    def __str__(self):
        return self.display_name
    

class Job_Model(models.Model):
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(Custom_User, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title


class ApplyModel(models.Model):
    job = models.ForeignKey(Job_Model, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.applicant.display_name} applied for {self.job.job_title}"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    company_info = models.TextField(max_length=128)
    profile_pic = models.ImageField(upload_to='media/Recruiter/profile_pic')

    def __str__(self):
        return f"Recruiter Profile for {self.user.username}"

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    skills_set = models.TextField(max_length=128)
    resume = models.FileField(upload_to='resumes/')
    profile_pic = models.ImageField(upload_to='media/Jobseeker/profile_pic')

    def __str__(self):
        return f"Job Seeker Profile for {self.user.username}"
