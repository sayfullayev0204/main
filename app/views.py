from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer, ServiceCategorySerializer, ServiceSerializer
from rest_framework.permissions import IsAuthenticated
from .authentication import CookieAuthentication
from rest_framework import viewsets, filters
from .models import Apartment, Citizn, Service, ServiceCategory
from .serializers import ApartmentSerializer, ApartmentDetailSerializer, CitiznSerializer
from .permissions import IsVillageAdmin
from .pagination import CustomPagination

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = CustomUserSerializer(user).data  # Custom serializer for user data

            response = Response(
                {"user": user_data},
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=False,
                secure=True,
                samesite="None",
            )
            return response

        return Response(
            {"detail": "Foydalanuvchi topilmadi yoki parol noto‘g‘ri!"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserProfileView(APIView):
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = CustomUserSerializer(user).data
        return Response({"user": user_data})

class CitiznViewSet(viewsets.ModelViewSet):
    serializer_class = CitiznSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated, IsVillageAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'gender', 'phone']
    pagination_class = CustomPagination

    def get_queryset(self):
        return Citizn.objects.filter(Village=self.request.user.village).select_related('apartment').prefetch_related('leaves', 'personal_statuses')

    def perform_create(self, serializer):
        serializer.save(Village=self.request.user.village)

class ApartmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated, IsVillageAdmin]
    pagination_class = CustomPagination
    queryset = Apartment.objects.all().select_related('village__district__region')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApartmentDetailSerializer
        return ApartmentSerializer

    def get_queryset(self):
        return Apartment.objects.filter(village=self.request.user.village).select_related('village__district__region')

class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceCategorySerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ServiceCategory.objects.all()

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user).select_related('user', 'category').prefetch_related('images')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)