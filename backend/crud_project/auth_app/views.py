from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token  # Assuming you're using token authentication
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

class SignUpAPI(APIView):
    def post(self, request):
        try:
            # Extract data from request
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {"message": "Username already taken"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create a new user
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)  # Hash the password
            )

            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"message": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class SignInAPI(APIView):
    def post(self, request):
        try:
            # Extract credentials from request
            username = request.data.get('username')
            password = request.data.get('password')

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Create or get token for the user
                token, created = Token.objects.get_or_create(user=user)

                return Response(
                    {"message": "User signed in successfully", "token": token.key},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                {"message": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class ForgotPasswordAPI(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')

            # Check if the user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"message": "User with this email does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Generate a password reset token (random string)
            reset_token = get_random_string(32)

            # Send the email (this assumes an email backend is configured)
            reset_link = f"http://yourdomain.com/reset-password/{reset_token}/"
            email_subject = "Password Reset Request"
            email_body = render_to_string('reset_password_email.html', {
                'user': user,
                'reset_link': reset_link
            })

            send_mail(
                email_subject,
                email_body,
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False
            )

            return Response(
                {"message": "Password reset email sent"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )