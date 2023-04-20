from django.contrib.auth import hashers
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import *
from .models import FriendRequest, Profile
from .serializer import AuthUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


@api_view(['POST'], )
def UserCreateAPIView(request):
    form = UserRegisterForm(data=request.POST) or None
    if form.is_valid():
        data = {'username': request.data['username'], 'email': request.data['email'],
                'password': hashers.make_password(request.data['password1'])}
        serializer = AuthUserSerializer(data=data)

        if serializer.is_valid():
            User(username=request.data['username'].lower(), email=request.data['email'].lower(),
                 password=hashers.make_password(request.data['password1'])).save()
            return Response({'message': 'signup successful'}, status=status.HTTP_201_CREATED)
        else:
            data = {"data": serializer._errors}
            print(data)
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': form._errors}
    print(data)
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'], )
def UserLoginAPIView(request):
    if User.objects.filter(email=request.data['email']).exists():
        user_obj = User.objects.get(email=request.data['email'])
        if user_obj.check_password(request.data['password']):
            serializer = TokenObtainPairSerializer(
                data={'email': request.data['email'], 'password': request.data['password']})
            token = serializer.validate({'username': user_obj.username, 'password': request.data['password']})
            print(token)
            data = {'email': request.data['email'], 'token': token['access']}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': 'Invalid user'}
    print(data)
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'], )
def UserListAPIView(request):
    print(request.user)
    if request.user.is_authenticated:
        try:
            if User.objects.filter(username=request.user).exists():
                user_obj = list(User.objects.all().values().exclude(is_superuser=True))
                return Response(user_obj, status=status.HTTP_200_OK)

        except Exception as error:
            data = {'data': 'No users.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': 'Unauthorized request'}
    return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'], )
def SearchUserAPIView(request):
    q = request.data['query']
    if request.user.is_authenticated:
        try:
            if '@' in q:
                user_obj = User.objects.get(email__exact=q)
                data = {'email': str(user_obj.email)}
                return Response(data, status=status.HTTP_200_OK)
            else:
                user_obj = User.objects.filter(username__icontains=q).values_list('username')
                data = {'username': user_obj}
                return Response(data, status=status.HTTP_200_OK)

        except Exception as error:
            data = {'data': str(error)}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': 'Unauthorized request'}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'], )
def SearchUserAPIView(request):
    q = request.data['query']

    if request.user.is_authenticated:
        try:
            if '@' in q:
                user_obj = User.objects.get(email__exact=q)
                data = {'email': str(user_obj.email)}
                return Response(data, status=status.HTTP_200_OK)
            else:
                user_obj = User.objects.filter(username__icontains=q).values_list('username')
                data = {'username': user_obj}
                return Response(data, status=status.HTTP_200_OK)

        except Exception as error:
            data = {'data': str(error)}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': 'Unauthorized request'}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'], )
def SendFriendRequestAPIView(request):
    print('MA ' + str(request.user))
    if request.user.is_authenticated:
        try:
            user = get_object_or_404(User, id=request.POST.get('to_user'))

            frequest, created = FriendRequest.objects.get_or_create(
                from_user=request.user,
                to_user=user)
            print("USER " + str(user))
            data = {'data': 'Friend Request Sent.'}
            return Response(data, status=status.HTTP_200_OK)

        except Exception as error:
            data = {'error': str(error)}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': 'Unauthorized request'}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'], )
def AcceptFriendRequestAPIView(request):
    print(request.user)
    if request.user.is_authenticated:
        try:
            from_user = get_object_or_404(User, id=request.POST.get('to_user', ''))
            frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
            user1 = frequest.to_user
            user2 = from_user
            user1.profile.friends.add(user2.profile)
            user2.profile.friends.add(user1.profile)
            frequest.delete()

            data = {'msg': 'Friend Request Accepted.'}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            data = {'error': 'Friend Request not found. May be earlier you accepted ! else canceled by sender user.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': 'Unauthorized request'}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'], )
def RejectFriendRequestAPIView(request):
    print(request.user)
    if request.user.is_authenticated:
        try:
            from_user = get_object_or_404(User, id=request.POST.get('from_user', ''))
            frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
            frequest.delete()
            data = {'msg': 'Friend Request Rejected.'}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            data = {
                'error': 'Friend Request not found. May be earlier you accepted ! else rejected by you.',
                'error1': str(error)}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': 'Unauthorized request'}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'], )
def MyProfileAPIView(request):
    print(request.user)
    if request.user.is_authenticated:
        try:
            print(request.user)
            p = Profile.objects.filter(user=request.user).first()
            print('DATA : ' + str(p))
            u = p.user
            sent_friend_requests = list(FriendRequest.objects.filter(from_user=request.user).values())
            rec_friend_requests = list(FriendRequest.objects.filter(to_user=request.user).values())
            friends = list(p.friends.all().values())

            data = {'my_name': str(u), 'sent_friend_requests': sent_friend_requests,
                    'pending_friend_requests': rec_friend_requests,
                    'friends_list': friends}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            data = {'error': 'Invalid user.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    data = {'data': 'Unauthorized request'}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
