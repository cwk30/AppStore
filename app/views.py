from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import usersext

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
def nanny_profile_page(request):
    return render(request,'app/Nanny Profile Page.html')
def nanny_requests(request):
    return render(request,'app/Nanny Requests.html')

def parents_browse_sitters(request):
    return render(request,'app/Parent browse sitter.html')
def parent_make_offer(request):
    return render(request,'app/Parents make offers.html')
def parent_offers(request):
    return render(request,'app/Parent offers.html')
def parent_page(request):
    return render(request,'app/Parent page.html')
def parent_profile(request):
    return render(request,'app/Parent profile.html')
def parent_bookings(request):
    return render(request,'app/Parent Bookings.html')
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
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

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
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
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