from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import User
# from .models import Detail
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from hotel import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render
from user.models import User  # Assuming your custom User model is here








from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.models import User  # Custom User model
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.urls import reverse_lazy

from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import User, HotelStaff
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import User, HotelStaff
import random

def staff_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Password validation
        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return redirect('user:staff_signup')  # Use namespace

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists")
            return redirect('user:staff_signup')  # Use namespace

        # Create new staff user
        user = User.objects.create_user(
            username=username,
            password=password1,
            name=name,
            email=username,
            phone=phone,
            is_staff=True,
            is_superuser=False,
            is_active=False  # Inactive until verified
        )

        # Create HotelStaff profile
        staff_id = f"HSTF{random.randint(100, 999)}"
        HotelStaff.objects.create(
            user=user,
            staff_id=staff_id,
            department='reception'
        )

        # Generate verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = request.build_absolute_uri(
            reverse('user:staff_verify_email', args=[uid, token])  # Use 'user:' namespace
        )

        # Email content
        subject = 'Welcome to Hotel Staff - Verify Your Account'
        html_message = render_to_string('staff_login/staff_verification_email.html', {
            'name': name,
            'username': username,
            'verification_url': verification_url,
            'domain': request.get_host(),
            'protocol': 'https' if request.is_secure() else 'http',
        })
        plain_message = strip_tags(html_message)

        # Send verification email with error handling
        try:
            email = EmailMultiAlternatives(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [username],
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            messages.success(request, "Registration successful. Please check your email for verification.")
        except Exception as e:
            user.delete()
            messages.error(request, f"Failed to send verification email: {str(e)}")
            return redirect('user:staff_signup')  # Use namespace

        return redirect('user:staff_signin')  # Use namespace

    return render(request, 'staff_login/staff_signup.html')

def staff_verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token) and user.is_staff:
            user.is_active = True
            user.save()
            return render(request, 'staff_login/staff_verification_success.html', {'message': 'Email verified successfully. You can now sign in.'})
        else:
            return render(request, 'staff_login/staff_verification_failure.html', {'message': 'Invalid verification link or account is not a staff account.'})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'staff_login/staff_verification_failure.html', {'message': 'Verification failed due to an invalid or expired link.'})

def staff_signin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/')  # Use namespace

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            return render(request, 'staff_login/staff_signup.html', {'message': "Staff doesn't exist. Please sign up"})

        user = User.objects.get(username=username)

        if not user.is_staff:
            return render(request, 'staff_login/staff_signin.html', {'message': 'This is not a staff account. Please use a staff username.'})

        if not user.is_active:
            return render(request, 'staff_login/staff_signin.html', {'message': 'Staff account is not verified yet. Please check your email for verification instructions.'})

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            if authenticated_user.is_staff and authenticated_user.is_active:
                request.session['username'] = username
                request.session.save()
                login(request, authenticated_user)
                return redirect('/')  # Use namespace
            else:
                return render(request, 'staff_login/staff_signin.html', {'message': 'Account is not authorized for staff access.'})

        return render(request, 'staff_login/staff_signin.html', {'message': 'Incorrect username or password'})

    return render(request, 'staff_login/staff_signin.html')

# Add staffpanel view if not already present


# Staff Logout
def staff_logout_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)
        request.session.flush()  # Clear session data
        return redirect('staff:staff_signin')
    return redirect('staff:staff_signin')

# Custom Staff Password Reset View
class StaffCustomPasswordResetView(PasswordResetView):
    template_name = 'staff_login/staff_password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('staff:staff_password_reset_done')

    def form_valid(self, form):
        # Ensure only staff users can reset their password via this view
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email, is_staff=True).exists():
            return render(self.request, self.template_name, {'form': form, 'error': 'No staff account found with this email.'})
        return super().form_valid(form)

# Custom Staff Password Reset Confirm View
class StaffCustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'staff_login/staff_password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('staff:staff_password_reset_complete')

    def dispatch(self, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if not user.is_staff:
                return render(self.request, 'staff_login/staff_password_reset_failure.html', {'message': 'This is not a staff account.'})
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(self.request, 'staff_login/staff_password_reset_failure.html', {'message': 'Invalid reset link.'})
        return super().dispatch(*args, **kwargs)





def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        phone = request.POST['phone']
        password = request.POST['password']
        
        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'user_login/signin.html', {'message': 'User already exists with that username. Please sign in.'})

        # Create the new user and deactivate it until verification
        user = User.objects.create_user(username=username, password=password, name=name, phone=phone)
        user.is_active = False
        user.email = username  # Assuming the username is used as email

        # Generate token for email verification
        token = default_token_generator.make_token(user)
        
        # Build the verification URL
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = request.build_absolute_uri(reverse('user:verify_email', args=[uid, token]))

        # Email subject
        subject = 'Welcome to PandharpurGuide, Verify your account'

        # Render the HTML email template with password
        html_message = render_to_string('user_login/verification_email.html', {
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'password': password,  # Sending the password here (NOT recommended for production!)
            'verification_url': verification_url,
            'domain': request.get_host(),
            'protocol': 'https' if request.is_secure() else 'http',
        })
        
        # Convert HTML to plain text for fallback
        plain_message = strip_tags(html_message)
        
        # Email setup using EmailMultiAlternatives
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [user.email],  # Send email to the user's email (username as email)
        )
        email.attach_alternative(html_message, "text/html")

        # Try sending the email
        try:
            email.send()
        except Exception as e:
            # If there's an error sending the email, render a failure message
            return render(request, 'user_login/signup.html', {'message': f'Error sending verification email. Please try again later. ({str(e)})'})
        
        # Save the user after email is sent
        user.save()
        
        # Redirect to signin page with a success message
        return render(request, 'user_login/signin.html', {'message': 'User created successfully. Please check your email for verification instructions.'})

    return render(request, 'user_login/signup.html')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'user_login/verification_success.html')
        else:
            return render(request, 'staff_login/staff_verification_failure.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'user_login/verification_failure.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if the user exists
        if not User.objects.filter(username=username).exists():
            return render(request, 'user_login/signup.html', {'message': "User doesn't exist. Please sign up"})
        
        user = User.objects.get(username=username)
        
        # Check if the user account is verified
        if not user.is_active:
            return render(request, 'user_login/signin.html', {'message': 'User account is not verified yet. Please check your email for verification instructions.'})
        
        # Authenticate the user with credentials
        authenticated_user = authenticate(username=username, password=password)
        
        if authenticated_user is not None:
            if authenticated_user.is_active:
                request.session['username'] = username
                request.session.save()
                login(request, authenticated_user)
                return redirect('/')
        
        return render(request, 'user_login/signin.html', {'message': 'Incorrect username or password'})
    
    return render(request, 'user_login/signin.html')


def logout_view(request):
    try:
        # Try to delete the 'username' from the session
        del request.session['username']
    except KeyError:
        # Handle the case where 'username' is not in the session
        pass
    
    # Save the session changes and log out the user
    request.session.save()
    logout(request)
    
    # Optionally redirect to home or another page after logout
    return render(request, 'index.html', {'message': 'Logged out successfully'})


from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
class CustomPasswordResetView(PasswordResetView):
    template_name = 'user_login/password_reset.html'
    success_url = reverse_lazy('user:password_reset_done')
    email_template_name = 'user_login/reset_password.html'  # Plain text version
    html_email_template_name = 'user_login/reset_password.html'  # HTML version

    def form_valid(self, form):
        email = form.cleaned_data['email']
        protocol = 'https' if self.request.is_secure() else 'http'
        domain = self.request.get_host()

        opts = {
            'use_https': self.request.is_secure(),
            'from_email': self.from_email,
            'request': self.request,
            'email_template_name': self.email_template_name,
            'html_email_template_name': self.html_email_template_name,  # Add this
            'extra_email_context': {
                'protocol': protocol,
                'domain': domain,
            },
        }
        
        form.save(**opts)
        return super().form_valid(form)
    
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_login/password_reset_confirm.html'
    success_url = reverse_lazy('user:password_reset_complete')
    form_class = SetPasswordForm
