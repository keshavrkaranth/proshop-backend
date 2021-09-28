from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api import models
from api import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.email import sendEmail




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/create/',
        '/api/products/upload/',
        '/api/products/<id>/reviews/',
        '/api/products/<id>/top/',
        '/api/products/delete/<id>/',
        '/api/products/update/<id>/',

    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = serializers.UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    user = models.User.objects.all()
    serializer = serializers.UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    if len(data) == 0:
        return Response({'success': False, 'message': "Fill all necessary Details"}, status=422)
    else:
        try:
            user = models.User.objects.create(
                first_name=data['name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password'])

            )

            sendEmail(tomail=data['email'],name=data['name'],type='register')
            serializer = serializers.UserSerializerWithToken(user, many=False)
            return Response(serializer.data)

        except:
            message = {'message': 'Email id already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = serializers.UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] != "":
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = models.User.objects.get(id=pk)
    serializer = serializers.UserSerializer(user, many=False)
    return Response(serializer.data)





@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = models.User.objects.get(id=pk)

    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user.save()

    serializer = serializers.UserSerializer(user, many=False)

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = models.User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')
