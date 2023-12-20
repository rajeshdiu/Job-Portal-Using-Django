from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        return redirect("mySigninPage")

    return render(request,'signup.html')

def logoutPage(request):

    logout(request)

    return redirect('mySigninPage')

def mySigninPage(request):

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


@login_required
def deleteJob(request,myid):
    
    job=Job_Model.objects.filter(id=myid).delete()
    
    return redirect("viewjobPage")



@login_required
def editJobPage(request,myid):
    
    job=Job_Model.objects.filter(id=myid)
    
    context={
        'job':job
    }
    
    return render(request, 'Recruiter/edit_job.html',context)



@login_required
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
  
@login_required  
def ApplyList(request,myid):
    
    
    return render(request,'Recruiter/ApplyList.html')



@login_required
def apply_for_job(request, jobid):
    
    
    job = get_object_or_404(Job_Model, id=jobid)
    
    if request.method == 'POST':
        skills = request.POST.get('skills')
        resume = request.FILES.get('resume')
        
        
        if skills and resume:
            applicant = request.user

            application = ApplyModel.objects.create(
                job=job,
                applicant=applicant,
                skills=skills,
                resume=resume
            )
            application.save()
            return redirect('jobSeekerAppliedJob')
            messages.success(request, 'Application submitted successfully!')
        else:
            messages.error(request, 'Error in the application form. Please check the fields.')

    
    context={
        'job':job
    }
  

    return render(request, 'JobSeeker/apply_job.html',context)


def jobApplicationPage(request):
    
    applicants = ApplyModel.objects.all()

    context = {
        'applicants': applicants,
    }
    
    return render(request,'Recruiter/jobApplicationPage.html',context)


def ApplyList(request, myid):
    myJob = get_object_or_404(Job_Model, id=myid)
    applicants = ApplyModel.objects.filter(job=myJob)
    
    context = {
        'job': myJob,
        'applicants': applicants,
    }

    return render(request, 'Recruiter/ApplyList.html', context)


def jobSeekerAppliedJob(request):
    
    job_seeker=request.user
    
    applied_job=ApplyModel.objects.filter(applicant=job_seeker)
    
    context={
        'applied_job':applied_job,
        
    }
    
    
    return render(request, 'JobSeeker/appliedjob.html', context)


    
def userProfilePage(request):
    

    current_user = request.user

    if current_user.user_type == 'recruiter':
        jobs_created = Job_Model.objects.filter(created_by=current_user)
        
        context = {
            'user': current_user,
            'jobs_created': jobs_created,
        }
    elif current_user.user_type == 'jobseeker':
        applied_jobs = ApplyModel.objects.filter(applicant=current_user)
        seeker=JobSeekerProfile.objects.all()
        
        context = {
            'user': current_user,
            'applied_jobs': applied_jobs,
            'seeker':seeker,
        }
    else:
        # Handle other user types if needed
        context = {}

    return render(request, 'JobSeeker/profile.html', context)

