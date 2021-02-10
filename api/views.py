import datetime

from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.db.utils import IntegrityError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN)

from .models import UserData
from .validators import validate_password


@api_view(["POST"])
def reg(request):
    data = request.data

    if data.get('login') is None or data.get('password') is None:
        return Response({'Error': 'Login and password are required'},
                        status=HTTP_403_FORBIDDEN)

    lgn = data['login']
    password = data['password']

    if validate_password(password):
        try:
            UserData.objects.create(login=lgn, password=password)
        except IntegrityError:  # login must be unique (DB validation)
            return Response({'Error': f'The name: {login} is already taken'},
                            status=HTTP_403_FORBIDDEN)
    else:
        return Response({'Error': 'Password should contain letters, digits and symbols'},
                        status=HTTP_403_FORBIDDEN)

    return Response(status=HTTP_201_CREATED)


def create_session(response):
    """ Creates and saves in db new session according to django docs.
        Sets sessionid cookie to a response (passed as argument).
        Sessionid cookie lifetime - 2 weeks
    """
    new_session = SessionStore()
    new_session.create()
    new_session.save()

    sessionid = new_session.session_key
    response.set_cookie('sessionid', sessionid,
                        expires=(datetime.datetime.now() + datetime.timedelta(weeks=2)))


@api_view(["POST"])
def login(request):
    data = request.data

    if data.get('login') is None or data.get('password') is None:
        return Response({'Error': 'Login and password are required'},
                        status=HTTP_403_FORBIDDEN)

    lgn = data['login']
    password = data['password']

    try:
        UserData.objects.get(login=lgn, password=password)
    except UserData.DoesNotExist:
        return Response({'Error': 'Wrong login or password'},
                        status=HTTP_403_FORBIDDEN)

    response = Response({'Success': 'Logged in'}, status=HTTP_200_OK)

    if 'sessionid' in request.COOKIES:
        try:
            # Session expires in two weeks (like sessionid cookie)
            # so we need to check if it's still in db
            Session.objects.get(pk=request.COOKIES['sessionid'])
        except Session.DoesNotExist:
            create_session(response)    # create new session if old expired
    else:
        create_session(response)    # create new session if no sessionid

    return response


@api_view(["GET"])
def status(request):

    if 'sessionid' in request.COOKIES:
        try:
            Session.objects.get(pk=request.COOKIES['sessionid'])
        except Session.DoesNotExist:
            return Response({'Error': 'Login required / Session expired, please re-login'},
                            status=HTTP_403_FORBIDDEN)
        print(request.session.get_expiry_age())
        # now we checked that session is in place
        # to access session use:
        # session = request.session   or
        # session = SessionStore(session_key=request.COOKIES['sessionid'])

        return Response({'Status': 'Logged in'}, status=HTTP_200_OK)

    return Response({'Status': 'Login required'}, status=HTTP_403_FORBIDDEN)