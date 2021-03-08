from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.views import APIView

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ValidatePhoneSendOTPSerializer, \
    ValidateOTPSerializer, UserDetailSerializer, ForgetPasswordSerializer
# from .serializers import UserSerializer, LoginSerializer
from .models import CustomUser, PhoneOTP
from accounts.permissions import UpdateOwnProfile
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from django.db.models import Q
from .services import send_otp, otp_generator


class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', False)
        phone_number = request.data.get('phone', False)
        password = request.data.get('password', False)
        is_company = request.data.get('is_company', False)
        if username and phone_number and password:
            phone = str(phone_number)
            user = CustomUser.objects.filter(phone__iexact=phone)
            # user = user
            if user.exists() and user.first().is_active:
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                # logic to send the otp and store the phone number and that otp in table.
            else:
                otp = otp_generator()
                print(otp)
                if otp:
                    otp = str(otp)
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 7:
                            return Response({
                                'status': False,
                                'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            })
                        old.count = count + 1
                        old.otp = otp
                        send_otp(phone, otp)
                        old.save()
                        print("count increase", count)
                    else:
                        count = 1
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=otp,
                            count=count
                        )
                        send_otp(phone, otp)

                        temp_data = {'username': username, 'phone': phone, 'password': password, 'is_company': is_company}
                        serializer = RegisterSerializer(data=temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()

                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    })
                # print(request.session)
                # print(request.session.get('view'))
                request.session['phone'] = phone
                print('------------------')
                # print(request.session)
                # print(request.session.get('phone'))
                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })

        else:
            return Response({
                'status': 'False', 'detail': "I haven't received any phone number. Please do a POST request."
            })


class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password

    '''
    serializer_class = ValidateOTPSerializer

    def post(self, request, *args, **kwargs):
        # print(self.kwargs)
        # phone = self.kwargs['phone']
        # print(phone)
        # print('The requested phone (session) was:', request.session.get('phone'))
        # phone = request.data.get('phone', False)
        phone = request.session.get('phone')
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            user = CustomUser.objects.filter(phone__iexact=phone)
            user = user.first()
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()
                    user.is_active = True
                    user.save()
                    old.delete()
                    return Response({
                        'status': True,
                        'detail': 'OTP matched and registration completed. You can now log in into the system'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Kindly request a new otp with this number'
                })
        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not recieved in Post request'
            })



class RegisterAPI(APIView):
    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', False)
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)

        if username and phone and password:
            phone = str(phone)
            user = CustomUser.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({'status': False,
                                 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'username': username, 'phone': phone, 'password': password}
                        serializer = RegisterSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()

                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Congrts, user has been created successfully.'
                        })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Phone number not recognised. Kindly request a new otp with this number'
                    })





        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or password was not recieved in Post request'
            })


class ValidatePhoneForgot(APIView):
    '''
    Validate if account is there for a given phone number and then send otp for forgot password reset'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = CustomUser.objects.filter(phone__iexact=phone)
            if user.exists():
                otp = otp_generator()
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        k = old.count
                        if k > 7:
                            return Response({
                                'status': False,
                                'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            })
                        old.count = k + 1
                        old.otp = otp
                        send_otp(phone, otp)
                        old.save()
                        print("count increase", k)

                        return Response(
                            {'status': True, 'detail': 'OTP has been sent for password reset. Limits about to reach.'})

                    else:
                        count = 1

                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=otp,
                            count=count,
                            forgot=True,

                        )
                        send_otp(phone, otp)
                        request.session['phone_forgot'] = phone
                        print(request.session.get('phone_forgot'))
                        return Response({'status': True, 'detail': 'OTP has been sent for password reset'})

                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone number not recognised. Kindly try a new account for this number'
                })


class ForgotValidateOTP(APIView):
    '''
    If you have received an otp, post a request with phone and that otp and you will be redirected to reset  the forgotted password

    '''

    def post(self, request, *args, **kwargs):
        # phone = request.data.get('phone', False)
        phone = request.session.get('phone_forgot', False)
        otp_sent = request.data.get('otp', False)
        print(phone)
        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                if old.forgot == False:
                    return Response({
                        'status': False,
                        'detail': 'This phone havenot send valid otp for forgot password. Request a new otp or contact help centre.'
                    })

                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.forgot_logged = True
                    old.save()
                    request.session['phone_otp'] = otp
                    print(request.session.get('phone_otp'))
                    return Response({
                        'status': True,
                        'detail': 'OTP matched, kindly proceed to create new password'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not recieved in Post request'
            })


class ForgetPasswordChange(APIView):
    '''
    if forgot_logged is valid and account exists then only pass otp, phone and password to reset the password. All three should match.APIView
    '''

    def post(self, request, *args, **kwargs):
        # phone = request.data.get('phone', False)
        # otp = request.data.get("otp", False)
        phone = request.session.get('phone_forgot', False)
        otp = request.session.get('phone_otp', False)
        print(phone)
        print(otp)
        password = request.data.get('password', False)

        if phone and otp and password:
            old = PhoneOTP.objects.filter(Q(phone__iexact=phone) & Q(otp__iexact=otp))
            if old.exists():
                old = old.first()
                if old.forgot_logged:
                    post_data = {
                        'phone': phone,
                        'password': password
                    }
                    user_obj = get_object_or_404(CustomUser, phone__iexact=phone)
                    serializer = ForgetPasswordSerializer(data=post_data)
                    serializer.is_valid(raise_exception=True)
                    if user_obj:
                        user_obj.set_password(serializer.data.get('password'))
                        user_obj.active = True
                        user_obj.save()
                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Password changed successfully. Please Login'
                        })

                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP Verification failed. Please try again in previous step'
                    })

            else:
                return Response({
                    'status': False,
                    'detail': 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
                })




        else:
            return Response({
                'status': False,
                'detail': 'Post request have parameters missing.'
            })


# Register API
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "User": UserSerializer(user, context=self.get_serializer_context()).data,
#             "Message": "User create successfully"
#             # "token": AuthToken.objects.create(user)[1]
#         })


#
# # Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# # Get User API
class RetrieveUpdateDestroyUserAPI(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (UpdateOwnProfile,)


class ListUserAPI(generics.ListAPIView):
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    # def get_object(self):
    #     return self.request.user


class UserDetail(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UpdateOwnProfile]
    serializer_class = UserDetailSerializer

    # queryset = CustomUser.objects.all()
    def get_queryset(self):
        #     return self.request.user
        return CustomUser.objects.filter(id=self.request.user.id)

# return self.request.user.cars.all()
# return self.queryset.filter(owner=self.request.user)
# class UserAPI(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = CustomUser.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (UpdateOwnProfile,)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('username',)


# class LoginAPI(viewsets.ViewSet):
#     serializer_class = AuthTokenSerializer
#
#     def create(self, request):
#         return ObtainAuthToken().post(request)
