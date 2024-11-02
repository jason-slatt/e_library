# user_auth/serializers.py
from rest_framework import serializers
from .models import RoleChoices, UserRole
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.utils.http import urlsafe_base64_decode



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        print("Creating user...")  # Debugging
        # Create the user
        user = User(
            name=validated_data['name'],
            email=validated_data['email'],
            is_active=False  # User is inactive until activation
        )
        user.set_password(validated_data['password'])
        user.save()
        print("User created:", user)  # Debugging

        # Assign "User" role by default
        UserRole.objects.create(user=user, role=RoleChoices.USER)

        # Send the activation email
        self.send_activation_email(user)
        
        return user

    def send_activation_email(self, user):
        token_generator = PasswordResetTokenGenerator()
        print("Sending activation email...")  # Debugging
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://127.0.0.1:8000/user_auth/Activate-account/{uid}/{token}/"

        send_mail(
            subject='Activate your account',
            message=f'Please click the link to activate your account: {activation_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        print("Activation email sent to:", user.email)  # Debugging
    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data, *args , **kwargs):

        #getting the required information 
        email = data.get('email')
        password = data.get('password')

        #checking if the credential exist by autheneticating the user
        user = authenticate( email = email , password = password)

        if user is None :
            raise serializers.ValidationError('invalid login credentials')
        
       # Generate or retrieve the token
        token, _ = Token.objects.get_or_create(user=user)

        # Retrieve user role if managed through a related model
        try:
            user_role = UserRole.objects.get(user=user).role
        except UserRole.DoesNotExist:
            raise serializers.ValidationError("Role information not found for this user.")
        
         # Return user info and token
        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'role' : user_role
            },
            'token': token.key
        }
 
class PasswordResetSerializers(serializers.Serializer) :
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email = value)
            self.send_password_reset_email(user)

        except User.DoesNotExist :
            raise serializers.ValidationError("no user with this email")
        return value
    
    def send_password_reset_email(self, user):
        token_genarator = PasswordResetTokenGenerator()
        token = token_genarator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://127.0.0.1:8000/user_auth/password-reset-confirm/{uid}/{token}/"

        send_mail(
            subject='Reset password',
            message= f'click the link to reset the your password : {reset_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently= False
        )

class PasswordResetConfirmSerializers(serializers.Serializer):

    new_password = serializers.CharField(write_only = True)

    def validate(self, data):
        # retrieving the uid and the token from the context
        uid64= self.context.get('uid64')
        token = self.context.get('token')

        # decoding the user Id and check if he exist
        try :
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk = uid)
        except (User.DoesNotExist,  ValueError, TypeError):
                   raise serializers.ValidationError('user does not exist')
        
        # checking the user Token 
        token_genarator = PasswordResetTokenGenerator()
        if not token_genarator.check_token(user, token):
         print(f"Token validation failed for user {user.email}: {token}")
         raise serializers.ValidationError('invalid token or token expired')
        
        self.user = user
        return data
    
    def create(self, validated_data):
        # This method is called after the data has been validated
        new_password = validated_data.get('new_password')
        # Set the new password
        self.user.set_password(new_password)
        # Save the user instance
        self.user.save()
        return self.user  
        
        
        # if everything is okay take the new password and save it
       
class ActivateAccountSerializer(serializers.Serializer):
      def validate(self, data):
          uid64 = self.context.get('uid64')
          token = self.context.get('token')
          token_generator = PasswordResetTokenGenerator()

          try :
               uid = urlsafe_base64_decode(uid64).decode()
               user = User.objects.get(pk = uid)
          except (User.DoesNotExist,  ValueError, TypeError):
              raise serializers.ValidationError('No user found try again')
          
          if not token_generator.check_token(user, token):
              raise serializers.ValidationError('token expired or invalid token')
          self.user = user
          return data 
      def create(self, validated_data):
          self.user.is_active = True
          self.user.save()
          return self.user
          
          

           
          

          

   
