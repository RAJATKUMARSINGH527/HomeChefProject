from rest_framework import generics, permissions, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Customer, MealKit, Order, Review, SubscriptionPlan, Company, ChefPlan, GiftCard, CartItem
from .serializers import CustomerSerializer, CustomerRegisterSerializer, CompanySerializer, CompanyRegisterSerializer, ChefPlanSerializer, SubscriptionPlanSerializer, MealKitSerializer,  GiftCardSerializer, CartItemSerializer, OrderSerializer, ReviewSerializer

import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Custom Pagination Class
class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

# Customer Registration View
class CustomerRegisterView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer

# User Login View (JWT Authentication)
class UserLoginView(generics.CreateAPIView):
    # Custom view for login using JWT
    pass


# Customer Detail View
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

# Company Views
class CompanyListView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyRegisterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['food_type', 'category']
    ordering_fields = ['name', 'food_type']

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

# ChefPlan Views
class ChefPlanListView(generics.ListCreateAPIView):
    queryset = ChefPlan.objects.all()
    serializer_class = ChefPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['price', 'chef__user__username']
    ordering_fields = ['price', 'plan_name']

class ChefPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChefPlan.objects.all()
    serializer_class = ChefPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

# SubscriptionPlan Views
class SubscriptionPlanListView(generics.ListCreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['price', 'meals_per_week', 'company__name']
    ordering_fields = ['price', 'meals_per_week']

class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

# MealKit Views
class MealKitListView(generics.ListCreateAPIView):
    queryset = MealKit.objects.all()
    serializer_class = MealKitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['price', 'chef__user__username']
    ordering_fields = ['price', 'name']

class MealKitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MealKit.objects.all()
    serializer_class = MealKitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

# GiftCard Views
class GiftCardListView(generics.ListCreateAPIView):
    queryset = GiftCard.objects.all()
    serializer_class = GiftCardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['value', 'status']
    ordering_fields = ['value', 'created_at']

class GiftCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GiftCard.objects.all()
    serializer_class = GiftCardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

# CartItem Views
class CartItemListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['quantity', 'meal_kit__name', 'customer__user__username']
    ordering_fields = ['quantity', 'created_at']

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

# Order Views
class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['status', 'payment_status']
    ordering_fields = ['order_date', 'status']

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

# Review Views
class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['rating', 'meal_kit__name']
    ordering_fields = ['review_date', 'rating']

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

# Payment View
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({
            'amount': int(order.meal_kit.price * 100),  # Amount in paisa
            'currency': 'INR',
            'payment_capture': '1'
        })

        order.payment_status = Order.PAYMENT_PENDING
        order.save()

        return Response(payment)

