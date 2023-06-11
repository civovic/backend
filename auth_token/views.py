from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from auth_token import serializers
from auth_token.models import User
from auth_token.serializers import UserListSerializer

from drf_yasg.utils import swagger_auto_schema

from shared.exceptions import ConflictEmailEx, ConflictPhoneEx


@swagger_auto_schema(
    methods=['POST'],
    operation_id="users_register",
    request_body=serializers.UserRegisterSerializer(),
    responses={
        201: ": (Created) Success.",
        400: ": (Bad Request) Invalid request body.",
        409: ": (Conflict) User email already exists."
    })
@api_view(['POST'])
def register(request):
    """ Register new user


    """
    # validate request_body
    context = {"request": request}
    serializer = serializers.UserRegisterSerializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)

    # create user
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')
    mobile_phone_number = serializer.validated_data.get('mobile_phone_number')

    user_exists = User.objects.filter(Q(username=email) | Q(email=email)).first()
    if user_exists:
        raise ConflictEmailEx("This email already exists.")

    phone_exists = User.objects.filter(Q(mobile_phone_number=mobile_phone_number)).first()
    if phone_exists:
        raise ConflictPhoneEx("This mobile phone number already exists.")

    user = User.objects.create_user(
        username=email, email=email,
        password=email,
        mobile_phone_number=serializer.validated_data.get('mobile_phone_number'),
        first_name=serializer.validated_data.get('first_name'),
        last_name=serializer.validated_data.get('last_name', ""),
        birth_date=serializer.validated_data.get('birth_date'),
        gender=serializer.validated_data.get('gender'),
        )
    serializer = serializers.UserSerializer(user, context=context)

    return Response(serializer.data, status.HTTP_201_CREATED)


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('username',)
