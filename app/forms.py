from django import forms

class UserLoginForm(forms.Form):
    email=forms.CharField(label='Email', max_length=100)
    password = forms.CharField(widget = forms.PasswordInput())

class UserRegistrationForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    nric = forms.CharField(label='NRIC', max_length=100)
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=range(1950, 2012)))
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)
    
class JobCreationForm(forms.Form):
    start_date = forms.DateField(label='Start Date',widget=forms.SelectDateWidget(years=range(2022, 2023)))
    start_time = forms.TimeField(label='Daily Start Time',widget=forms.TimeInput(format='%H:%M'))
    end_date = forms.DateField(label='End Date',widget=forms.SelectDateWidget(years=range(2022, 2023)))
    end_time = forms.TimeField(label='Daily End Time',widget=forms.TimeInput(format='%H:%M'))
    rate = forms.CharField(label="Rate")
    experience_req = forms.CharField(label='Years of Experience Required',max_length = 3)
    job_requirement = forms.CharField(max_length = 500)

class NannyAvailableForm(forms.Form):
    start_date = forms.DateField(label='Start Date',widget=forms.SelectDateWidget(years=range(2022, 2023)))
    start_time = forms.TimeField(label='Start Time')
    end_date = forms.DateField(label='Daily End Date',widget=forms.SelectDateWidget(years=range(2022, 2023)))
    end_time = forms.TimeField(label='Daily End Time')
    rate = forms.CharField(max_length = 5)
    experience = forms.CharField(max_length = 3)
    about_me = forms.CharField(max_length=500)

class JobFilterForm(forms.Form):
    min_start_date = forms.DateField(label='Earliest Start Date',widget=forms.SelectDateWidget(years=range(2022, 2023)))
    min_start_time = forms.TimeField(label='Earliest Start Time',widget=forms.TimeInput(format='%H:%M'))
    max_end_date = forms.DateField(label='Latest End Date',widget=forms.SelectDateWidget(years=range(2022, 2023)))
    max_end_time = forms.TimeField(label='Latest End Time',widget=forms.TimeInput(format='%H:%M'))
    min_rate = forms.CharField(label='Minimum Rate($)')
    max_experience_req = forms.CharField(label='Maximum Experience Required (Years)')

class NannyFilterForm(forms.Form):
    max_start_date = forms.DateField(label='Start Date',widget=forms.SelectDateWidget(years=range(2022, 2023)))
    max_start_time = forms.TimeField(label='Start Time',widget=forms.TimeInput(format='%H:%M'))
    min_end_date = forms.DateField(label='End Date',widget=forms.SelectDateWidget(years=range(2022, 2023)))
    min_end_time = forms.TimeField(label='End Time',widget=forms.TimeInput(format='%H:%M'))
    max_rate = forms.CharField(label='Maximum Rate($)')
    min_experience_req = forms.CharField(label='Minimum Experience Required (Years)')

class UserUpdateForm(forms.Form):
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)
    dob = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=range(1950, 2012)))


    
    # username =  StringField("Username", validators=[Required(), Length(min=2, max=20)])
    # #name =  StringField("Name", validators=[Required(), Length(min=1, max=40)]) 

    # email = StringField('Email', validators=[Required(), Email()]) 
    # password = PasswordField('Password', validators=[Required()])
    # #contactno = StringField('Contact No.', validators=[Required(), Length(min=8, max=8)]) 

    # confirm_password = PasswordField('Confirm Password', validators=[Required(), EqualTo('password')])

    # submit = SubmitField('Sign Up') 

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first() 
    #     if user:
    #         raise ValidationError('That username is already registered. Please choose another.')
    
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first() 
    #     if user:
    #         raise ValidationError('That email is already registered. Please login with your registered account.')