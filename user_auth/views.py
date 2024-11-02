from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer, PasswordResetSerializers, PasswordResetConfirmSerializers, ActivateAccountSerializer
from rest_framework.views import APIView
from .permissions import Isadmin
from .models import RoleChoices


# Create your views here.

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    # # permission_classes = [any]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            print (data)
            return Response({'message' : 'login success', 'data' : data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializers
    def post(self,request):
        serializers = self.serializer_class(data = request.data)
        if serializers.is_valid(raise_exception=True):
            return Response({'reset link send successfully'}, status= status.HTTP_200_OK)
        return Response(serializers.errors, status= status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.CreateAPIView): 
    serializer_class = PasswordResetConfirmSerializers

    def post(self, request, uid64 , token  ):
        serializer = self.get_serializer(data = request.data, context = {'uid64' : uid64 , 'token' : token})
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'password reset , login with the new password'}, status= status.HTTP_202_ACCEPTED)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ActivateAccountView(generics.CreateAPIView) :
    serializer_class = ActivateAccountSerializer
    def  get(self,request, uid64, token) :
        serializers = self.get_serializer(data={}, context = {'uid64': uid64, 'token': token})
        if serializers.is_valid():
            serializers.save()
            return Response({'message' : 'account Activated successly login now '}, status= status.HTTP_200_OK)
        return Response(serializers.errors, status= status.HTTP_400_BAD_REQUEST)
               




#     serializer_class = LoginSerializer
# def validate(self, data, request):
#         serializers = LoginSerializer(data = request.data)
#         email = serializers.EmailField()
#         password = serializers.CharField()


#         #getting the required information 
#         email = data.get('email')
#         password = data.get('password')

#         #checking if the credential exist by autheneticating the user
#         user = authenticate( email = email , password = password)

#         if user is None :
#             raise serializers.ValidationError('invalid login credentials')
        
#         #Generating a token for the user
#         refresh = RefreshToken.for_user(user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['user'] = {
#             'id': user.id,
#             'email': user.email,
#             'role': user.role,
#         }
#         return  Response({'user login', data}, status= status.HTTP_202_ACCEPTED)

#     # def create(self, request, *args, **kwargs):
    #     serializer = self.get(data = request.data)
    #     serializer.data.set_password(validated_data['password'])
    #     if serializer.is_valid():
    #         serializer.save()
    # if serializer_class.is_valid():
    #     serializer_class.save()
    #             return Response({'message : user sucessfully login', serializer_class.data}, status= status.HTTP_201_CREATED)
 
    #      return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class LiberianCreationView(APIView):
    permission_classes = [Isadmin]

    def post(self, request) :
        if not request.user.userrole.is_admin():
            return Response({'action not allowed'}, status= status.HTTP_403_FORBIDDEN)
         
        liberian_data = request.data.copy()
        liberian_data['role'] = RoleChoices.LIBRARIAN

        serializers = RegistrationSerializer(data = liberian_data)

        if serializers.is_valid():
            serializers.save()

            return Response({'librian created', serializers.data}, status= status.HTTP_201_CREATED)
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)






