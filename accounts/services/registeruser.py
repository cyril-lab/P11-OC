from substitute.models.user import User


class RegisterUser:
    """this class allows to register a user"""
    def __init__(self, request):
        self.request = request
        self.name = ""
        self.surname = ""
        self.email = ""
        self.password1 = ""
        self.password2 = ""
        self.username = ""

    def verify_post_request(self):
        """this function checks that the request type is POST"""
        if self.request.method == 'POST':
            return True

    @staticmethod
    def validate_form(form):
        """this function checks that the form is valid"""
        if form.is_valid():
            return True

    def get_form_data(self, form):
        """this function retrieves the data from the form"""
        self.name = form.cleaned_data['name']
        self.surname = form.cleaned_data['surname']
        self.email = form.cleaned_data['email']
        self.password1 = form.cleaned_data['password1']
        self.password2 = form.cleaned_data['password2']
        self.username = self.email

    def password_verification(self):
        """this function checks that the passwords are equal"""
        if self.password1 != self.password2:
            return True

    def mail_verification(self):
        """
        this function checks that the email address
         is not already registered
        """
        test_mail = User.objects.filter(username=self.username)
        if test_mail:
            return True

    def create_user(self):
        """this function create user in database"""
        user = User.objects.create_user(self.username,
                                        self.email,
                                        self.password1,
                                        first_name=self.name,
                                        last_name=self.surname)
        user.save()
