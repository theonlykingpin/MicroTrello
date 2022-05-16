from django.contrib.auth import get_user_model
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OTPRequest
from .serializers import RequestOTPSerializer, RequestOTPResponseSerializer, VerifyOtpRequestSerializer, \
    ObtainTokenSerializer


class OTPView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTPRequest.objects.generate(data)
                serializer = RequestOTPResponseSerializer(otp)
                return Response(data=serializer.data)
            except Exception as e:
                return Response(data=str(e), status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data):
                return Response(self._handle_login(data))
            else:
                return Response(data='Your credentials is incorrect.', status=HTTP_401_UNAUTHORIZED)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def _handle_login(data):
        current_user = get_user_model()
        user, created = current_user.objects.get_or_create(username=data['receiver'])
        refresh = RefreshToken.for_user(user)
        return ObtainTokenSerializer({'refresh': str(refresh),
                                      'token': str(refresh.access_token),
                                      'created': bool(created)}).data
