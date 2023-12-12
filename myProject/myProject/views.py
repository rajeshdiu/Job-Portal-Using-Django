from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from myApp.models import *


def signupPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        displayname= request.POST.get('display_name')
        mail= request.POST.get('email')
        pass_word= request.POST.get('password')
        usertype= request.POST.get('user_type')
        user = Custom_User.objects.create_user(username=user_name,password=pass_word)
        user.display_name=displayname
        user.email=mail
        user.user_type=usertype
        user.save()
        return redirect("signinPage")

    return render(request,'signup.html')

def logoutPage(request):

    logout(request)

    return redirect('signinPage')

def signinPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=user_name, password=password)

        print(user)

        if user:
            login(request,user)
            return redirect("dashboardPage")


    return render(request,'login.html')

@login_required
def dashboardPage(request):

    user=request.user

    if user.is_authenticated:

        if user.user_type == 'recruiter':

            context={
                'myUser':"Hi I am recruiter"
            }

            Template_name = 'Recruiter/dashboard.html'
        
        elif user.user_type == 'jobseeker':

            context={
                'myUser':"Hi I am jobseeker"
            }

            Template_name = 'JobSeeker/dashboard.html'
        else:
            return HttpResponse("Invalid User")
    else:
        return HttpResponse(" User is not authenticated ")
    
    return render(request,Template_name,context)

@login_required
def viewjobPage(request):
    
    job=Job_Model.objects.all()
    
    context={
        'job':job
    }


    return render(request,"viewjob.html",context)


@login_required
def add_job(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        description = request.POST.get('description')
        
        print(job_title,company,location,description)

        # Assuming the user is stored in request.user
        user = request.user

        # Create a new Job instance
        new_job = Job_Model(
            job_title=job_title,
            company=company,
            location=location,
            description=description,
            created_by=user  # Assign the job to the current user
        )

        # Save the job to the database
        new_job.save()

        return redirect('viewjobPage')  # Redirect to the dashboard or another page

    return render(request, 'Recruiter/add_job.html')


def deleteJob(request,myid):
    
    job=Job_Model.objects.filter(id=myid).delete()
    
    return redirect("viewjobPage")



def editJobPage(request,myid):
    
    job=Job_Model.objects.filter(id=myid)
    
    context={
        'job':job
    }
    
    return render(request, 'Recruiter/edit_job.html',context)



def updateJob(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job_title = request.POST.get('job_title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        description = request.POST.get('description')
        
        print(job_id,job_title,company,location,description)

        # Assuming the user is stored in request.user
        user = request.user

        # Create a new Job instance
        new_job = Job_Model(
            id=job_id,
            job_title=job_title,
            company=company,
            location=location,
            description=description,
            created_by=user,  # Assign the job to the current user
        )

        # Save the job to the database
        new_job.save()

        return redirect('viewjobPage')
    
def ApplyList(request,myid):
    
    
    return render(request,'Recruiter/ApplyList.html')



def apply_for_job(request, jobid):
    
    job = Job_Model.objects.filter(id=jobid)
    
    context={
        'job':job
    }
  

    return render(request, 'JobSeeker/apply_job.html',context)
    
