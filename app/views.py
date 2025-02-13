from cmd import IDENTCHARS
from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserLoginForm, JobCreationForm, JobFilterForm, NannyAvailableForm, UserUpdateForm, NannyFilterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import usersext, jobs, nanny, appliednanny, request
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
def nanny_page(request):
    current_user = request.user
    result_dict={}
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM app_appliednanny a, app_nanny n WHERE a.nannyid_id=n.id AND n.user_id=%s"
                        , [current_user.id])
        counts = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM app_appliednanny a, app_nanny n WHERE a.nannyid_id=n.id AND a.status='accepted' AND n.user_id=%s"
                        , [current_user.id])
        countsa = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM app_request r WHERE r.tositter_id=%s"
                        , [current_user.id])
        countsb = cursor.fetchone()
        
    result_dict['applications'] = counts[0]
    result_dict['bookings'] = countsa[0]
    result_dict['requests'] = countsb[0]
    return render(request,'app/Nanny Page.html',result_dict)

def nanny_bookings(request):
    return render(request,'app/Nanny Bookings.html')



def parent_page(request):
    current_user = request.user
    result_dict={}
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM app_appliednanny a, app_jobs j WHERE a.jobid_id=j.jobid AND a.status='accepted' AND j.user_id=%s"
                        , [current_user.id])
        counts = cursor.fetchone()
        cursor.execute("SELECT * FROM app_jobs WHERE user_id=%s"
                        , [current_user.id])
        countsa = cursor.fetchone()
        cursor.execute("SELECT * FROM app_request WHERE fromparent_id=%s"
                        , [current_user.id])
        countsb = cursor.fetchone()
        cursor.execute("SELECT u.first_name, u.last_name, COUNT(r.tositter_id) FROM app_request r, auth_user u WHERE r.tositter_id = u.id GROUP BY u.first_name, u.last_name ORDER BY COUNT(u.first_name) DESC LIMIT 1")
        countsc = cursor.fetchone()
        
    if counts is None:
        result_dict['bookings'] = 0
    else:
        result_dict['bookings'] = counts[0]
    if countsa is None:
        result_dict['offers'] = 0
    else:
        result_dict['offers'] = countsa[0]
    if countsb is None:
        result_dict['requests'] = 0
    else:
        result_dict['requests'] = countsb[0]
    
    result_dict['supersitter'] = countsc
    

    return render(request,'app/Parent page.html',result_dict)

def elements(request):
    return render(request,'app/elements.html')
# def index(request):
#     return render(request,'app/index.html')
# def index2(request):
#     return render(request,'app/index 2.html')


#-----------------------------------LOGIN REGISTER FUNCTIONS-----------------------------------#
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
                return redirect('/parent_page')
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
            return redirect('/nanny#login')
        if userlogin_form.is_valid():
            user = authenticate(username=userlogin_form.cleaned_data['email'], password=userlogin_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.info(request, 'Login Successful')
                return redirect('/nanny_page')
            else:
                messages.info(request, 'Login fail')
                return redirect('/nanny#login')
            
    # If this is a GET (or any other method) create the default form.
    else:
        
        userregister_form = UserRegistrationForm
        userlogin_form = UserLoginForm

    return render(request, 'app/nannyloginregister.html',{'userregister_form': userregister_form, 'userlogin_form':userlogin_form})

#-----------------------------------PARENT ROLE FUNCTIONS-----------------------------------#
@login_required
def parent_make_offer(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        createjob_form = JobCreationForm(request.POST)
        # Check if the form is valid:
        print(request.POST)
        if createjob_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            current_user = request.user
            print(current_user.id)        
            new_job = jobs(user_id=current_user.id, 
                        start_date=createjob_form.cleaned_data['start_date'], 
                        start_time=createjob_form.cleaned_data['start_time'],
                        end_date=createjob_form.cleaned_data['end_date'],
                        end_time=createjob_form.cleaned_data['end_time'],
                        rate=createjob_form.cleaned_data['rate'],
                        experience_req=createjob_form.cleaned_data['experience_req'],
                        job_requirement=createjob_form.cleaned_data['job_requirement'])
            new_job.save()
            messages.info(request, 'Your job creation is successful! Eligible nannies can now see the job you created')
            return redirect('/parent_offers')
    # If this is a GET (or any other method) create the default form.
    else:
        createjob_form = JobCreationForm
        
    return render(request, 'app/Parent make offers.html',{'createjob_form': createjob_form})

#VIEW PARENT PROFILE (CURRENT USER)
@login_required
def parent_profile(request):
    current_user = request.user
    result_dict = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT e.nric, u.first_name, u.last_name, u.email, e.dob FROM auth_user u left join app_usersext e on u.id = e.user_id where u.id = %s"
                        , [current_user.id])
        results = cursor.fetchone()
    result_dict['records'] = results
    return render(request,'app/Parent Profile.html',result_dict)

#UPDATE PARENT PROFILE (CURRENT USER)
@login_required
def parent_profile_update(request):
    current_user = request.user
    if request.method == 'POST':
        
        # Create a form instance and populate it with data from the request (binding):
        userupdate_form = UserUpdateForm(request.POST)
        # Check if the form is valid:
        if userupdate_form.is_valid():
            #PERFORM SINGLE TXN
            with transaction.atomic():
                with connection.cursor() as cursor:     
                    cursor.execute("UPDATE auth_user SET first_name = %s, last_name = %s WHERE id = %s"
                            , [userupdate_form.cleaned_data['first_name'], userupdate_form.cleaned_data['last_name'], current_user.id])
                    cursor.execute("UPDATE app_usersext SET dob = %s WHERE user_id = %s"
                            ,  [userupdate_form.cleaned_data['dob'], current_user.id])
            return redirect('/parent_profile')
    # If this is a GET (or any other method) create the default form.
    else:
        userupdate_form = UserUpdateForm

    return render(request, 'app/Parent Profile Update.html',{'userupdate_form': userupdate_form})


#-----------------------------------NANNY ROLE FUNCTIONS-----------------------------------#
#NANNY PROFILE PAGE (ALSO SEE AVAILABILITY)
@login_required
def nanny_profile_page(request):
    current_user = request.user
    result_dict = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT e.nric, u.first_name, u.last_name, u.email, e.dob, u.password, n.start_date, n.end_date, n.start_time, n.end_time, n.rate, n.experience, n.about_me FROM auth_user u left join app_usersext e on  u.id = e.user_id left join app_nanny n on u.id = n.user_id where u.id = %s"
                        , [current_user.id])
        results = cursor.fetchone()
    result_dict['records'] = results
    return render(request,'app/Nanny Profile Page.html',result_dict)

#VIEW CURRENT AVAILABILITY SET (OBSOLETE)
@login_required
def nannyscheduleview(request):
    print(request.user)
    """Shows the main page"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT u.first_name, u.last_name, n.start_date, n.end_date, n.start_time, n.end_time, n.rate, n.experience, n.about_me FROM auth_user u, app_nanny n WHERE n.user_id=u.id") 
        #results = namedtuplefetchall(cursor)
        nanny_schedule = cursor.fetchone()
    nanny_dict = {'results': nanny_schedule}
    return render(request, 'app/nannyscheduleview.html',nanny_dict)

#EDIT CURRENT AVAILABILITY
@login_required
def nanny_availability_update(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        nannyavail_form = NannyAvailableForm(request.POST)
        # Check if the form is valid:
        if nannyavail_form.is_valid():
            # print("%s %s %s %s %s %s %s %s %s %s %s",min_start_date.strftime("%Y-%m-%d"), max_end_date.strftime("%Y-%m-%d"), str(min_rate), str(min_experience_req), min_start_time.strftime("%-H"),min_start_time.strftime("%-H"),min_start_time.strftime("%-M"), max_end_time.strftime("%-H"),max_end_time.strftime("%-H"),max_end_time.strftime("%-M"))
            with connection.cursor() as cursor:
                cursor.execute("UPDATE app_nanny SET start_date = %s, end_date = %s, start_time = %s, end_time = %s, rate = %s, experience = %s, about_me = %s FROM auth_user u, app_nanny n WHERE n.user_id = u.id AND n.user_id = %s"
                        , [nannyavail_form.cleaned_data['start_date'], nannyavail_form.cleaned_data['end_date'], nannyavail_form.cleaned_data['start_time'],
                            nannyavail_form.cleaned_data['end_time'] , nannyavail_form.cleaned_data['rate'], nannyavail_form.cleaned_data['experience'], nannyavail_form.cleaned_data['about_me'], str(request.user.id)])
            return redirect('/nannyscheduleview')
    # If this is a GET (or any other method) create the default form.
    else:
        nannyavail_form = NannyAvailableForm
    
    return render(request, 'app/Nanny Availability Update.html',{'nannyavail_form': nannyavail_form})

#UPDATE PROFILE 
@login_required
def nanny_profile_update(request):
    current_user = request.user
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        userupdate_form = UserUpdateForm(request.POST)
        # Check if the form is valid:
        if userupdate_form.is_valid():
            #PERFORM SINGLE TXN
            with transaction.atomic():
                with connection.cursor() as cursor:     
                    cursor.execute("UPDATE auth_user SET first_name = %s, last_name = %s, email = %s, username = %s WHERE id = %s"
                            , [userupdate_form.cleaned_data['first_name'], userupdate_form.cleaned_data['last_name'], userupdate_form.cleaned_data['email'], userupdate_form.cleaned_data['email'], current_user.id])
                    cursor.execute("UPDATE app_usersext SET dob = %s WHERE user_id = %s"
                            ,  [userupdate_form.cleaned_data['dob'], current_user.id])
            return redirect('/nanny_profile_page')
    # If this is a GET (or any other method) create the default form.
    userupdate_form = UserUpdateForm

    return render(request, 'app/Nanny Profile Update.html',{'userupdate_form':userupdate_form})

#NANNY BROWSE JOBS CREATED BY PARENTS

@login_required
def nanny_opportunities(request):
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
                cursor.execute("SELECT u.first_name, u.last_name, j.start_date, j.end_date, j.start_time, j.end_time, j.rate, j.experience_req, j.job_requirement, j.jobid FROM auth_user u, app_jobs j WHERE (j.user_id=u.id AND j.start_date >= %s AND j.end_date <= %s AND j.rate>=%s AND j.experience_req<=%s) AND ((date_part('hour',j.start_time) > %s) OR ((date_part('hour',j.start_time) = %s AND (date_part('minute',j.start_time) > %s)))) AND ((date_part('hour',j.end_time) < %s) OR ((date_part('hour',j.end_time) = %s AND (date_part('minute',j.end_time) < %s))))",
                [min_start_date.strftime("%Y-%m-%d"), max_end_date.strftime("%Y-%m-%d"), str(min_rate), str(max_experience_req), min_start_time.strftime("%H"),min_start_time.strftime("%H"),min_start_time.strftime("%M"), max_end_time.strftime("%H"),max_end_time.strftime("%H"),max_end_time.strftime("%M")]) 
                results = namedtuplefetchall(cursor)
            return render(request, 'app/Nanny Opportunities.html',{'filterjob_form': JobFilter_form, 'results': results})
    # If this is a GET (or any other method) create the default form.
    else:
        JobFilter_form = JobFilterForm
        with connection.cursor() as cursor:
            cursor.execute("SELECT u.first_name, u.last_name, j.start_date, j.end_date, j.start_time, j.end_time, j.rate, j.experience_req, j.job_requirement, j.jobid FROM auth_user u, app_jobs j WHERE j.user_id=u.id") 
            results = namedtuplefetchall(cursor)    
    return render(request, 'app/Nanny Opportunities.html',{'filterjob_form': JobFilter_form, 'results': results})

#NANNY SEE JOB AND APPLY
@login_required
def parents_browse_sitters(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        NannyFilter_form = NannyFilterForm(request.POST)
        # Check if the form is valid:
        print(NannyFilter_form.is_valid())
        print(NannyFilter_form.cleaned_data)
        if NannyFilter_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            
            max_start_date=NannyFilter_form.cleaned_data['max_start_date']
            max_start_time=NannyFilter_form.cleaned_data['max_start_time']
            min_end_date=NannyFilter_form.cleaned_data['min_end_date']
            
            min_end_time=NannyFilter_form.cleaned_data['min_end_time']
            max_rate=NannyFilter_form.cleaned_data['max_rate']
            min_experience_req=NannyFilter_form.cleaned_data['min_experience_req']
            with connection.cursor() as cursor:
                cursor.execute("SELECT u.first_name, u.last_name, n.start_date, n.end_date, n.start_time, n.end_time, n.rate, n.experience, n.about_me, n.id FROM auth_user u, app_nanny n WHERE (n.user_id=u.id AND n.start_date <= %s AND n.end_date >= %s AND n.rate<=%s AND n.experience>=%s) AND ((date_part('hour',n.start_time) < %s) OR ((date_part('hour',n.start_time) = %s AND (date_part('minute',n.start_time) < %s)))) AND ((date_part('hour',n.end_time) > %s) OR ((date_part('hour',n.end_time) = %s AND (date_part('minute',n.end_time) > %s))))",
                [max_start_date.strftime("%Y-%m-%d"), min_end_date.strftime("%Y-%m-%d"), str(max_rate), str(min_experience_req), max_start_time.strftime("%H"),max_start_time.strftime("%H"),max_start_time.strftime("%M"), min_end_time.strftime("%H"),min_end_time.strftime("%H"),min_end_time.strftime("%M")]) 
                results = namedtuplefetchall(cursor)
            return render(request, 'app/Parent browse sitter.html',{'NannyFilter_form': NannyFilter_form, 'results': results})
    # If this is a GET (or any other method) create the default form.
    else:
        NannyFilter_form = NannyFilterForm
        with connection.cursor() as cursor:
            cursor.execute("SELECT u.first_name, u.last_name, n.start_date, n.end_date, n.start_time, n.end_time, n.rate, n.experience, n.about_me, n.id FROM auth_user u, app_nanny n WHERE n.user_id=u.id") 
            results = namedtuplefetchall(cursor)    
    return render(request, 'app/Parent browse sitter.html',{'NannyFilter_form': NannyFilter_form, 'results': results})
@login_required
def nanny_view_offer(request, id):
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
        current_user = request.user
        with connection.cursor() as cursor:
            #check if nanny already applied
            cursor.execute("SELECT * FROM app_appliednanny a, app_nanny n WHERE a.nannyid_id=n.id AND n.user_id = %s AND a.jobid_id = %s", [str(current_user.id),str(id)])
            curr_nannyid = cursor.fetchone()
            
            ## No nanny with same id
            if curr_nannyid == None:
                cursor.execute("INSERT INTO app_appliednanny (jobid_id,nannyid_id,status) SELECT %s, app_nanny.id,'pending' FROM app_nanny WHERE app_nanny.user_id=%s", [str(id), str(current_user.id)])
                status = 'Applied successfully!'
                return redirect('/nanny_opportunities')
            else:
                status = 'You have already applied!'
    
    context['status'] = status
    print(view_job)
    return render(request,'app/Nanny view offer.html',{'jobv': view_job, 'status': status })

def parent_view_sitter(request,id):

    # dictionary for initial data with
    # field names as keys
    context ={}
    """Shows the main page"""
    ## Use raw query to get the job
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_nanny WHERE id = %s", [id])
        view_nanny = cursor.fetchone()
    nannyv_dict = {'nannyv': view_nanny}
    targetuser = User.objects.get(id=nannyv_dict["nannyv"][8])
        
    status = ''
    # save the data from the form
    if request.POST:
        current_user = request.user
        with connection.cursor() as cursor:
            #check if nanny already applied
            cursor.execute('SELECT requestid FROM app_request WHERE fromparent_id = %s AND tositter_id = %s', [str(current_user.id),id])
            curr_nannyid = cursor.fetchone()
            ## No nanny with same id
            if curr_nannyid == None:
                cursor.execute("INSERT INTO app_request (tositter_id, fromparent_id, status) VALUES (%s, %s, 'pending')", [str(nannyv_dict["nannyv"][8]),str(current_user.id)])
                status = 'Requested successfully!'
                return redirect('/parent_browse_sitters')
            else:
                status = 'You have already requested!'
                messages.info(request, 'You have already requested!')
    
    context['status'] = status
    return render(request,'app/Parent view sitter.html',{'nannyv': view_nanny, 'fname': targetuser.first_name, 'lname': targetuser.last_name, 'status': status })
    
    
@login_required

def nanny_requests(request):
    """Shows the main page""" 
    current_user = request.user
    ## Accept
    if request.POST:
        
        if request.POST['action'] == 'accept':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE app_request SET status='accepted' WHERE requestid = %s", [request.POST['id']])
                cursor.execute("SELECT u.username FROM auth_user u,app_request r WHERE r.requestid = %s and r.fromparent_id=u.id", [request.POST['id']])
                view_email = cursor.fetchone()
                print(view_email)
                
                messages.info(request,view_email )
        
        if request.POST['action'] == 'reject':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE app_request SET status='rejected' WHERE requestid = %s", [request.POST['id']])
                

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT u.first_name, u.last_name, r.requestid, u.id FROM app_request r, auth_user u WHERE tositter_id= %s and status=%s and r.fromparent_id=u.id",[str(current_user.id),'pending'])
        pendings = cursor.fetchall()
        cursor.execute("SELECT u.first_name, u.last_name, u.username, u.id FROM app_request r, auth_user u WHERE tositter_id= %s and status=%s and r.fromparent_id=u.id",[str(current_user.id),'accepted'])
        accepts = cursor.fetchall()
        cursor.execute("SELECT u.first_name, u.last_name FROM app_request r, auth_user u WHERE tositter_id= %s and status=%s and r.fromparent_id=u.id",[str(current_user.id),'rejected'])
        rejects = cursor.fetchall()

    result_dict = {'pending': pendings, 'accepted':accepts, 'rejected':rejects}

    return render(request,'app/Nanny Requests.html',result_dict)

@login_required
def nanny_view_parent_jobs(request,id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_jobs WHERE user_id = %s", [id])
        results = cursor.fetchall()
        cursor.execute("SELECT first_name, last_name FROM auth_user WHERE id = %s", [id])
        name = cursor.fetchone()
        print(name)
        
        result_dict = {'record':results, 'names':name}
    return render(request,'app/Nanny view parent jobs.html',result_dict)

@login_required
def parent_offers(request):
    current_user = request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_jobs WHERE user_id = %s AND status='pending'", [str(current_user.id)])
        results = cursor.fetchall()
        cursor.execute("SELECT * FROM app_jobs WHERE user_id = %s AND status='closed'", [str(current_user.id)])
        resultsclosed = cursor.fetchall()
        cursor.execute("SELECT first_name, last_name FROM auth_user WHERE id = %s", [str(current_user.id)])
        name = cursor.fetchone()
        print(name)
        
        result_dict = {'record':results, 'names':name, 'resultsclosed':resultsclosed}
    return render(request,'app/Parent Offers.html',result_dict)

def view_applicants(request,id):
    current_user = request.user
    ## Accept
    jobidnow=id
    # print('id now is'+str(jobidnow))
    if request.POST:
        # print('thingy to delete is'+str(request.POST['ids']))
        if request.POST['action'] == 'accept':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE app_appliednanny SET status='accepted' WHERE applyid = %s", [request.POST['ids']])
                cursor.execute("UPDATE app_jobs SET status='closed' WHERE jobid = %s", [id])
                
                
                
        if request.POST['action'] == 'reject':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE app_appliednanny SET status='rejected' WHERE applyid = %s", [request.POST['ids']])
      
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT u.first_name, u.last_name, u.username, n.id, a.applyid, n.start_date, n.start_time, n.end_date, n.end_time, n.rate, n.experience, n.about_me FROM app_appliednanny a, app_jobs j, app_nanny n, auth_user u WHERE a.jobid_id=j.jobid AND j.user_id=%s AND a.nannyid_id=n.id AND n.user_id=u.id AND a.status=%s AND j.jobid=%s",[str(current_user.id),'pending',jobidnow])
        pendings = cursor.fetchall()
        cursor.execute("SELECT u.first_name, u.last_name, u.username, n.id, a.applyid, n.start_date, n.start_time, n.end_date, n.end_time, n.rate, n.experience, n.about_me FROM app_appliednanny a, app_jobs j, app_nanny n, auth_user u WHERE a.jobid_id=j.jobid AND j.user_id=%s AND a.nannyid_id=n.id AND n.user_id=u.id AND a.status=%s AND j.jobid=%s",[str(current_user.id),'accepted',jobidnow])
        accepts = cursor.fetchall()
        cursor.execute("SELECT u.first_name, u.last_name, u.username, n.id, a.applyid, n.start_date, n.start_time, n.end_date, n.end_time, n.rate, n.experience, n.about_me FROM app_appliednanny a, app_jobs j, app_nanny n, auth_user u WHERE a.jobid_id=j.jobid AND j.user_id=%s AND a.nannyid_id=n.id AND n.user_id=u.id AND a.status=%s AND j.jobid=%s",[str(current_user.id),'rejected',jobidnow])
        rejects = cursor.fetchall()
    
    result_dict = {'pending': pendings, 'accepted':accepts, 'rejected':rejects, 'jobid':id}
    print(result_dict['pending'])
    return render(request,'app/Parent view offer applicants.html',result_dict)

#VIEW ALL JOBS WHICH NANNY (CURRENT USER) HAS APPLIED
@login_required
def nanny_application(request):
    # dictionary for initial data with field names as keys
    result_dict ={}
    current_user = request.user
    print(current_user.id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT j.jobid, j.start_date, j.end_date, j.start_time, j.end_time, j.rate, j.job_requirement, a.status FROM app_jobs j, app_appliednanny a, app_nanny n WHERE j.jobid=a.jobid_id and a.nannyid_id=n.id and n.user_id = %s",[str(current_user.id)])
        results = cursor.fetchall()
    result_dict={'records': results}
    
    print(results)
    print(result_dict)
    return render(request, "app/Nanny Application.html", result_dict)

@login_required
def logoutuser(request):
    logout(request)
    user = None
    return render(request, "app/landing.html", {"message": "You have been logged out"})
    














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
def nanny_availability_create(request):
    # Create a form instance and populate it with data from the request (binding):
    nannyavail_form = NannyAvailableForm(request.POST)
    # Check if the form is valid:
    if nannyavail_form.is_valid():
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
        current_user = request.user
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
        return redirect('/nanny_page')

    else:
        nannyavail_form = NannyAvailableForm # If this is a GET (or any other method) create the default form.

    return render(request, 'app/Nanny Availability Create.html',{'nannyavail_form': nannyavail_form})


#-----------------------------------WHY ARE U HERE-----------------------------------#
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
