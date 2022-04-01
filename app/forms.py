from django import forms

class UserLoginForm(forms.Form):
    email=forms.CharField(label='Email', max_length=100)
    password = forms.CharField(widget = forms.PasswordInput())

class ParentRegistrationForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    nric = forms.CharField(label='NRIC', max_length=100)
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget)
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)
    
    
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