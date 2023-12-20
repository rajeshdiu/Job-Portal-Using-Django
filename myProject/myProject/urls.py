
from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signupPage,name='signupPage'),
    path('logoutPage/',logoutPage,name='logoutPage'),
    path('mySigninPage/',mySigninPage,name='mySigninPage'),
    path('dashboardPage/',dashboardPage,name='dashboardPage'),
    path('viewjobPage/',viewjobPage,name='viewjobPage'),
    path('add_job/',add_job,name='add_job'),
    path('deleteJob/<str:myid>',deleteJob,name='deleteJob'),
    path('editJobPage/<str:myid>',editJobPage,name='editJobPage'),
    path('updateJob/',updateJob,name='updateJob'),
    path('ApplyList/<str:myid>',ApplyList,name='ApplyList'),
    path('apply_for_job/<str:jobid>',apply_for_job,name='apply_for_job'),
    path('jobApplicationPage/',jobApplicationPage,name='jobApplicationPage'),
    path('jobSeekerAppliedJob/',jobSeekerAppliedJob,name='jobSeekerAppliedJob'),
    path('userProfilePage/',userProfilePage,name='userProfilePage'),
]

