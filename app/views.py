from cmd import IDENTCHARS
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserLoginForm, JobCreationForm, JobFilterForm, NannyAvailableForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import usersext, jobs, nanny, appliednanny
from django.contrib.auth.decorators import login_required
from collections import namedtuple
from datetime import datetime

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

# Create your views here.
def index(request):
    return render(request,'app/landing.html')
def nanny_application(request):
    return render(request,'app/Nanny Application.html')
def nanny_page(request):
    return render(request,'app/Nanny Page.html')
def nanny_bookings(request):
    return render(request,'app/Nanny Bookings.html')
def nanny_opportunities(request):
    return render(request,'app/Nanny Opportunities.html')

def nanny_requests(request):
    return render(request,'app/Nanny Requests.html')

def parents_browse_sitters(request):
    return render(request,'app/Parent browse sitter.html')
def parent_make_offer(request):
    return render(request,'app/Parent make offers.html')
def parent_offers(request):
    return render(request,'app/Parent offers.html')
def parent_page(request):
    return render(request,'app/Parent page.html')
def parent_profile(request):
    return render(request,'app/Parent profile.html')
def parent_bookings(request):
    return render(request,'app/Parent Bookings.html')
def view_applicants(request):
    return render(request,'app/Parent view offer applicants.html')
def elements(request):
    return render(request,'app/elements.html')
def index(request):
    return render(request,'app/index.html')
def index2(request):
    return render(request,'app/index 2.html')

def parentloginregister(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        userregister_form = UserRegistrationForm(request.POST)
        userlogin_form = UserLoginForm(request.POST)
        # Check if the form is valid:
        if userregister_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            user = User.objects.create_user(username=userregister_form.cleaned_data['email'], password=userregister_form.cleaned_data['password'], first_name=userregister_form.cleaned_data['first_name'], last_name=userregister_form.cleaned_data['last_name'])
            ue = usersext(user=user, nric=userregister_form.cleaned_data['nric'], dob=userregister_form.cleaned_data['date_of_birth'], role='parent')
            ue.save()
            messages.info(request, 'Your registration is successful! Login with your credentials below to continue.')
            return redirect('/parent#login')
        if userlogin_form.is_valid():
            user = authenticate(username=userlogin_form.cleaned_data['email'], password=userlogin_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.info(request, 'Login Successful')
                return redirect('/parent#login')
            else:
                messages.info(request, 'Login fail')
                return redirect('/parent#login')

    # If this is a GET (or any other method) create the default form.
    else:
        
        userregister_form = UserRegistrationForm
        userlogin_form = UserLoginForm

    return render(request, 'app/parentloginregister.html',{'userregister_form': userregister_form, 'userlogin_form':userlogin_form})

def nannyloginregister(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        userregister_form = UserRegistrationForm(request.POST)
        userlogin_form = UserLoginForm(request.POST)
        # Check if the form is valid:
        if userregister_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            user = User.objects.create_user(username=userregister_form.cleaned_data['email'], password=userregister_form.cleaned_data['password'], first_name=userregister_form.cleaned_data['first_name'], last_name=userregister_form.cleaned_data['last_name'])
            ue = usersext(user=user, nric=userregister_form.cleaned_data['nric'], dob=userregister_form.cleaned_data['date_of_birth'], role='nanny')
            ue.save()
            messages.info(request, 'Your registration is successful! Login with your credentials below to continue.')
            return redirect('/parent#login')
        if userlogin_form.is_valid():
            user = authenticate(username=userlogin_form.cleaned_data['email'], password=userlogin_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.info(request, 'Login Successful')
                return redirect('/nanny#login')
            else:
                messages.info(request, 'Login fail')
                return redirect('/nanny#login')
            
    # If this is a GET (or any other method) create the default form.
    else:
        
        userregister_form = UserRegistrationForm
        userlogin_form = UserLoginForm

    return render(request, 'app/nannyloginregister.html',{'userregister_form': userregister_form, 'userlogin_form':userlogin_form})

@login_required
def parentcreatejob(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        createjob_form = JobCreationForm(request.POST)
        # Check if the form is valid:
        if createjob_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            current_user = request.user
            print(current_user.id)        
            new_job = jobs(user=current_user, 
                        start_date=createjob_form.cleaned_data['start_date'], 
                        start_time=createjob_form.cleaned_data['start_time'],
                        end_date=createjob_form.cleaned_data['end_date'],
                        end_time=createjob_form.cleaned_data['end_time'],
                        rate=createjob_form.cleaned_data['rate'],
                        experience_req=createjob_form.cleaned_data['experience_req'],
                        job_requirement=createjob_form.cleaned_data['job_requirement'])
            new_job.save()
            messages.info(request, 'Your job creation is successful! Eligible nannies can now see the job you created')
            return redirect('/parentcreatejob')
    # If this is a GET (or any other method) create the default form.
    else:
        createjob_form = JobCreationForm
        
    return render(request, 'app/parentcreatejob.html',{'createjob_form': createjob_form})

@login_required
def nannyscheduleview(request):
    print(request.user)
    """Shows the main page"""
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT u.first_name, u.last_name, n.start_date, n.end_date, n.start_time, n.end_time, n.rate, n.experience, n.about_me FROM auth_user u, app_nanny n WHERE n.user_id=u.id") 
        #results = namedtuplefetchall(cursor)
        nanny_schedule = cursor.fetchone()
    nanny_dict = {'results': nanny_schedule}
    return render(request, 'app/nannyscheduleview.html',nanny_dict)

@login_required
def nannyedit(request):

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM auth_user u, app_nanny n WHERE n.user_id = u.id")
        obj = cursor.fetchone()

    status = ''
    # save the data from the form
    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE app_nanny SET start_date = %s, end_date = %s, start_time = %s, end_time = %s, rate = %s, experience = %s, about_me = %s FROM auth_user u, app_nanny n WHERE n.user_id = u.id"
                        , [request.POST['start_date'], request.POST['end_date'], request.POST['start_time'],
                            request.POST['end_time'] , request.POST['rate'], request.POST['experience'], request.POST['about_me']])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM auth_user u, app_nanny n WHERE n.user_id = u.id")
            obj = cursor.fetchone()
            print(obj)

        context["obj"] = obj
        context["status"] = status
 
    return render(request, "app/nannyedit.html", context)




#-----------------------------------------------------------------------------------------------------------------------------------------#
@login_required
def nannybrowsejob(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        JobFilter_form = JobFilterForm(request.POST)
        # Check if the form is valid:
        print(JobFilter_form.is_valid())
        print(JobFilter_form.cleaned_data)
        if JobFilter_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            
            # min_start_date=JobFilter_form.cleaned_data['min_start_date'].strftime("%Y-%m-%d")
            # min_start_time=JobFilter_form.cleaned_data['min_start_time'].strftime("%H:%M:%S")
            # max_end_date=JobFilter_form.cleaned_data['max_end_date'].strftime("%Y %m %d")
            min_start_date=JobFilter_form.cleaned_data['min_start_date']
            min_start_time=JobFilter_form.cleaned_data['min_start_time']
            max_end_date=JobFilter_form.cleaned_data['max_end_date']
            
            max_end_time=JobFilter_form.cleaned_data['max_end_time']
            min_rate=JobFilter_form.cleaned_data['min_rate']
            max_experience_req=JobFilter_form.cleaned_data['max_experience_req']
            print(min_start_date.strftime("%Y-%m-%d"))
            print(max_end_date.strftime("%Y-%m-%d"))
            print(str(min_rate))
            print(str(max_experience_req))
            print(min_start_time.strftime("%H"))
            print(min_start_time.strftime("%H"))
            print(min_start_time.strftime("%M"))
            print(max_end_time.strftime("%H"))
            print(max_end_time.strftime("%H"))
            print(max_end_time.strftime("%M"))
            # print("%s %s %s %s %s %s %s %s %s %s %s",min_start_date.strftime("%Y-%m-%d"), max_end_date.strftime("%Y-%m-%d"), str(min_rate), str(min_experience_req), min_start_time.strftime("%-H"),min_start_time.strftime("%-H"),min_start_time.strftime("%-M"), max_end_time.strftime("%-H"),max_end_time.strftime("%-H"),max_end_time.strftime("%-M"))
            with connection.cursor() as cursor:
                cursor.execute("SELECT u.first_name, u.last_name, j.start_date, j.end_date, j.start_time, j.end_time, j.rate, j.experience_req, j.job_requirement FROM auth_user u, app_jobs j WHERE (j.user_id=u.id AND j.start_date >= %s AND j.end_date <= %s AND j.rate>=%s AND j.experience_req<=%s) AND ((date_part('hour',j.start_time) > %s) OR ((date_part('hour',j.start_time) = %s AND (date_part('minute',j.start_time) > %s)))) AND ((date_part('hour',j.end_time) < %s) OR ((date_part('hour',j.end_time) = %s AND (date_part('minute',j.end_time) < %s))))",
                [min_start_date.strftime("%Y-%m-%d"), max_end_date.strftime("%Y-%m-%d"), str(min_rate), str(max_experience_req), min_start_time.strftime("%H"),min_start_time.strftime("%H"),min_start_time.strftime("%M"), max_end_time.strftime("%H"),max_end_time.strftime("%H"),max_end_time.strftime("%M")]) 
                results = namedtuplefetchall(cursor)
            return render(request, 'app/nannybrowsejobs.html',{'filterjob_form': JobFilter_form, 'results': results})
    # If this is a GET (or any other method) create the default form.
    else:
        JobFilter_form = JobFilterForm
        with connection.cursor() as cursor:
            cursor.execute("SELECT u.first_name, u.last_name, j.start_date, j.end_date, j.start_time, j.end_time, j.rate, j.experience_req, j.job_requirement FROM auth_user u, app_jobs j WHERE j.user_id=u.id") 
            results = namedtuplefetchall(cursor)   
        
    return render(request, 'app/nannybrowsejobs.html',{'filterjob_form': JobFilter_form, 'results': results})


# @login_required
# def parentsbrowsenannies(request):
#     if request.method == 'POST':
#         # Create a form instance and populate it with data from the request (binding):
#         JobFilter_form = JobFilterForm(request.POST)
#         # Check if the form is valid:
#         print(JobFilter_form.is_valid())
#         print(JobFilter_form.cleaned_data)
#         if JobFilter_form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            
#             # min_start_date=JobFilter_form.cleaned_data['min_start_date'].strftime("%Y-%m-%d")
#             # min_start_time=JobFilter_form.cleaned_data['min_start_time'].strftime("%H:%M:%S")
#             # max_end_date=JobFilter_form.cleaned_data['max_end_date'].strftime("%Y %m %d")
#             min_start_date=JobFilter_form.cleaned_data['min_start_date']
#             min_start_time=JobFilter_form.cleaned_data['min_start_time']
#             max_end_date=JobFilter_form.cleaned_data['max_end_date']
            
#             max_end_time=JobFilter_form.cleaned_data['max_end_time']
#             min_rate=JobFilter_form.cleaned_data['min_rate']
#             max_experience_req=JobFilter_form.cleaned_data['max_experience_req']
#             print(min_start_date.strftime("%Y-%m-%d"))
#             print(max_end_date.strftime("%Y-%m-%d"))
#             print(str(min_rate))
#             print(str(max_experience_req))
#             print(min_start_time.strftime("%H"))
#             print(min_start_time.strftime("%H"))
#             print(min_start_time.strftime("%M"))
#             print(max_end_time.strftime("%H"))
#             print(max_end_time.strftime("%H"))
#             print(max_end_time.strftime("%M"))
#             # print("%s %s %s %s %s %s %s %s %s %s %s",min_start_date.strftime("%Y-%m-%d"), max_end_date.strftime("%Y-%m-%d"), str(min_rate), str(min_experience_req), min_start_time.strftime("%-H"),min_start_time.strftime("%-H"),min_start_time.strftime("%-M"), max_end_time.strftime("%-H"),max_end_time.strftime("%-H"),max_end_time.strftime("%-M"))
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT u.first_name, u.last_name, j.start_date, j.end_date, j.start_time, j.end_time, j.rate, j.experience_req, j.job_requirement FROM auth_user u, app_jobs j WHERE (j.user_id=u.id AND j.start_date >= %s AND j.end_date <= %s AND j.rate>=%s AND j.experience_req<=%s) AND ((date_part('hour',j.start_time) > %s) OR ((date_part('hour',j.start_time) = %s AND (date_part('minute',j.start_time) > %s)))) AND ((date_part('hour',j.end_time) < %s) OR ((date_part('hour',j.end_time) = %s AND (date_part('minute',j.end_time) < %s))))",
#                 [min_start_date.strftime("%Y-%m-%d"), max_end_date.strftime("%Y-%m-%d"), str(min_rate), str(max_experience_req), min_start_time.strftime("%H"),min_start_time.strftime("%H"),min_start_time.strftime("%M"), max_end_time.strftime("%H"),max_end_time.strftime("%H"),max_end_time.strftime("%M")]) 
#                 results = namedtuplefetchall(cursor)
#             return render(request, 'app/nannybrowsejobs.html',{'filterjob_form': JobFilter_form, 'results': results})
#     # If this is a GET (or any other method) create the default form.
#     else:
#         JobFilter_form = JobFilterForm
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT u.first_name, u.last_name, j.start_date, j.end_date, j.start_time, j.end_time, j.rate, j.experience_req, j.job_requirement FROM auth_user u, app_jobs j WHERE j.user_id=u.id") 
#             results = namedtuplefetchall(cursor)    
#     return render(request, 'app/nannybrowsejobs.html',{'filterjob_form': JobFilter_form, 'results': results})

# def index(request):
#     """Shows the main page""" 

#     ## Delete customer
#     if request.POST:
#         if request.POST['action'] == 'delete':
#             with connection.cursor() as cursor:
#                 cursor.execute("DELETE FROM customers WHERE customerid = %s", [request.POST['id']])

#     ## Use raw query to get all objects
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM customers ORDER BY customerid")
#         customers = cursor.fetchall()

#     result_dict = {'records': customers}

#     return render(request,'app/index.html',result_dict)

# Create your views here.
#def jobview(request, id):
#    """Shows the main page"""
#    ## Use raw query to get the job
#    with connection.cursor() as cursor:
#        cursor.execute("SELECT * FROM app_jobs WHERE jobid = %s", [id])
#        view_job = cursor.fetchone()
#    result_dict = {'jobv': view_job}
#    return render(request,'app/jobview.html',result_dict)

def jobview(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    """Shows the main page"""
    ## Use raw query to get the job
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_jobs WHERE jobid = %s", [id])
        view_job = cursor.fetchone()    
    jobv_dict = {'jobv': view_job}
    status = ''
    # save the data from the form
    if request.POST:
        with connection.cursor() as cursor:
            #check if nanny already applied
            cursor.execute("SELECT * FROM app_appliednanny WHERE nannyid_id = %s", request.user.id)
            curr_nannyid = cursor.fetchone()
            ## No nanny with same id
            if curr_nannyid == None:
                cursor.execute("INSERT INTO app_appliednanny(%s, %s)", id, request.user)
                status = 'Applied successfully!'
                return redirect(request,'app/nanny_opportunities.html')
            else:
                status = 'You have already applied!'
    
    context['status'] = status
    return render(request,'app/jobview.html',{'jobv': view_job, 'status': status })

@login_required
def nannyalljobview(request):
    # dictionary for initial data with field names as keys
    result_dict ={}
    with connection.cursor() as cursor:
        cursor.execute("SELECT j.jobid, j.start_date, j.end_date, j.start_time, j.end_time, j.rate, j.job_requirement p.status FROM app_jobs j, app_appliednanny p WHERE j.user_id = p.nannyid_id ORDER BY p.applyid")
        results = cursor.fetchone()
    result_dict['record']=results
    return render(request, "app/nannyalljobview.html", result_dict)

@login_required
def nanny_profile_page(request):
    current_user = request.user
    result_dict = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT e.nric, u.first_name, u.last_name, u.email, e.dob, u.password, n.start_date, n.end_date, n.start_time, n.end_time, n.rate, n.experience, n.about_me FROM app_nanny n, auth_user u, app_usersext e WHERE u.id = %s and e.role = 'nanny'"
                        , [current_user.id] )
        results = cursor.fetchall()
    result_dict = {'records': results}
    return render(request,'app/Nanny Profile Page.html',result_dict)















#---------------

def view(request, id):
    """Shows the main page"""
    ## Use raw query to get the job
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM jobs WHERE jobid = %s", [id])
        view_job = cursor.fetchone()
    result_dict = {'jobv': view_job}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
                return redirect('index')    
            else:
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE user = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)

#OLD NANNY AVAIL ADD
@login_required
def nannyscheduleadd(request):
    # Create a form instance and populate it with data from the request (binding):
    nannyavail_form = NannyAvailableForm(request.POST)
    # Check if the form is valid:
    if nannyavail_form.is_valid():
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
        current_user = request.user
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM app_nanny WHERE user = current_user")
        availability = nanny(user=current_user, 
                                start_date=nannyavail_form.cleaned_data['start_date'], 
                                start_time=nannyavail_form.cleaned_data['start_time'],
                                end_date=nannyavail_form.cleaned_data['end_date'],
                                end_time=nannyavail_form.cleaned_data['end_time'],
                                rate=nannyavail_form.cleaned_data['rate'],
                                experience=nannyavail_form.cleaned_data['experience'],
                                about_me = nannyavail_form.cleaned_data['about_me'])
        availability.save()
        messages.info(request, 'Your available schedule creation is successful! Parents looking for nannies can now see your availability.')
        return redirect('/nannyscheduleadd')

    else:
        nannyavail_form = NannyAvailableForm # If this is a GET (or any other method) create the default form.

    return render(request, 'app/nannyscheduleadd.html',{'nannyavail_form': nannyavail_form})