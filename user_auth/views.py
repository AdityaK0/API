from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from cms_app.serializers import UserSerializer, UserUpdateSerializer

from django.urls import reverse
from .models import Profile

User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request):
    return Response({"message":"CMS Authentication API's"})



@api_view(['POST', 'PUT', 'DELETE'])
def accounts(request):
    if request.method == 'POST':
        return register(request)

    elif request.method == 'PUT':
        return update_user_profile(request)

    elif request.method == 'DELETE':
        return delete_user_account(request)



@api_view(["POST","PUT","DELETE"])
def register(request):
        parameters = request.data
        print("Parameters -:-  ", parameters )
        required = ["username","phonenumber","email","password","fullname"]
        missing_fields = [ field for field in required  if not parameters.get(field)]
        if missing_fields:
            return Response({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
                            
        
        username = parameters["username"]
        if User.objects.filter(username=username).exists():
            return Response({"already exists":"user with this username already exists >>>> "},status=status.HTTP_400_BAD_REQUEST)

        email = parameters["email"]
        if User.objects.filter(email=email).exists():
            return Response({"already exists":"user with this email already exists >>>> "},status=status.HTTP_400_BAD_REQUEST)
        
        phonenumber = parameters["phonenumber"]
        if Profile.objects.filter(phonenumber=phonenumber).exists():
            return Response({"already exists":"user with this phone number already exists >>>> "},status=status.HTTP_400_BAD_REQUEST)
        
        fullname = parameters["fullname"]
        password = parameters["password"]
        
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        
        user_profile = Profile.objects.create(
            user=user,
            fullname=fullname,
            phonenumber=phonenumber
        )
        user_profile.save()
        
        token = get_tokens_for_user(user)
        
        return Response(
            {     
            "message":"user created successfully "
            ,
            
                "token":token
            },
            status=status.HTTP_201_CREATED
            )

            



@api_view(["POST"])
def login(request):
    identifier = request.data.get("identifier")
    password = request.data.get("password")
    
    if not identifier and not password:
        return Response({"message":"Please provide username/phonenumber and password"},status=status.HTTP_400_BAD_REQUEST)
    
    user = None
    
    if str(identifier).isdigit() and len(str(identifier))==10:
        if Profile.objects.filter(phonenumber=identifier).exists():
            user_phone = Profile.objects.get(phonenumber = identifier)
            user = User.objects.get(username=user_phone.user)
            print("GOT USERP ",user)
        else:
            return Response({"invalid":"User with this phone number does not exists"})
    else:
        if User.objects.filter(username=identifier).exists():
            user =  User.objects.get(username=identifier)
            print("GOT USERSX : ",user)
        else:
            return Response({"invalid":"User with this phone number does not exists"})
        
    authenticated_user = authenticate(username=user,password=password)    
    if authenticated_user:
       print("AUTHENTICATED ",authenticated_user)
       token = get_tokens_for_user(authenticated_user)
       return Response(
           {
               "message":"User logged in Successfully ",
               "token":token
           }
       )
    else:
        return Response({"message":"Invalid Credentials "},status=status.HTTP_400_BAD_REQUEST)
       
            
    

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = None
        if request.data:
           token = request.data["refresh"]  if request.data["refresh"] else None
        if not token:
                return Response({"invalid":"Refresh Token is required "},status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = RefreshToken(token) 
        refresh_token.blacklist()
        return Response({"message":"User logged out successfully "},status=status.HTTP_200_OK)
    
    except TokenError :
        return Response({"error": "Token is already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_access_token(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)

        return Response({'access': new_access_token}, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request):
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user_account(request):

    user = request.user
    user.delete()
    return Response({
        'message': 'Account deleted successfully'
    }, status=status.HTTP_204_NO_CONTENT)