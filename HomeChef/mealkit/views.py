# Import necessary modules and classes from rest_framework and other packages
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *

from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

# Custom Pagination Class
class CustomPagination(PageNumberPagination):
    # Set default page size
    page_size = 2
    # Allow clients to override the page size using the `page_size` query parameter
    page_size_query_param = 'page_size'
    # Set the maximum page size
    max_page_size = 10


class CustomerRegisterView(generics.CreateAPIView):
    # Allow any user to access this view
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # Serialize the incoming data
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new customer if the data is valid
            customer = serializer.save()
            # Return a success response with the new customer's ID
            return Response({'detail': 'Customer registered successfully', 'customer_id': customer.id}, status=status.HTTP_201_CREATED)
        # Return validation errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View (JWT Authentication)
class UserLoginView(APIView):
    # Allow any user to access this view
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # Get username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        # Find the user by username
        user = User.objects.filter(username=username).first()
        
        if user is not None:
            # Check the type of user and generate JWT tokens
            if user.is_customer or user.is_company or user.is_chef:
                refresh = RefreshToken.for_user(user)
                if user.is_customer:
                    user_type = 'customer'
                elif user.is_company:
                    user_type = 'company'
                else:
                    user_type = 'chef'
                # Return the JWT tokens and user type
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_type': user_type
                })
            else:
                # Return an error if the user type is not recognized
                return Response({'detail': 'User type not recognized'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Return an error if the credentials are invalid
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
# Customer Registration View
class CustomerListView(generics.ListAPIView):
    # Define the queryset to retrieve all Customer objects
    queryset = Customer.objects.all()
    # Use CustomerSerializer to serialize the queryset
    serializer_class = CustomerSerializer

# Customer Detail View
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Customer objects
    queryset = Customer.objects.all()
    # Use CustomerSerializer to serialize the queryset
    serializer_class = CustomerSerializer

# Company Views
class CompanyListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all Company objects
    queryset = Company.objects.all()
    # Use CompanyRegisterSerializer to serialize the queryset
    serializer_class = CompanyRegisterSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['food_type', 'category']
    # Define ordering fields
    ordering_fields = ['name', 'food_type']
    # Define filterset fields
    filterset_fields = ['name']

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Company objects
    queryset = Company.objects.all()
    # Use CompanySerializer to serialize the queryset
    serializer_class = CompanySerializer

# ChefPlan Views
class ChefPlanListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all ChefPlan objects
    queryset = ChefPlan.objects.all()
    # Use ChefPlanSerializer to serialize the queryset
    serializer_class = ChefPlanSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['price', 'chef__user__username']
    # Define ordering fields
    ordering_fields = ['price', 'plan_name']
    # Define filterset fields
    filterset_fields = ['price']

class ChefPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all ChefPlan objects
    queryset = ChefPlan.objects.all()
    # Use ChefPlanSerializer to serialize the queryset
    serializer_class = ChefPlanSerializer

# SubscriptionPlan Views
class SubscriptionPlanListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all SubscriptionPlan objects
    queryset = SubscriptionPlan.objects.all()
    # Use SubscriptionPlanSerializer to serialize the queryset
    serializer_class = SubscriptionPlanSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['price', 'meals_per_week', 'company__name']
    # Define ordering fields
    ordering_fields = ['price', 'meals_per_week']
    # Define filterset fields
    filterset_fields = ['price']

class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all SubscriptionPlan objects
    queryset = SubscriptionPlan.objects.all()
    # Use SubscriptionPlanSerializer to serialize the queryset
    serializer_class = SubscriptionPlanSerializer

# MealKit Views
class MealKitListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all MealKit objects
    queryset = MealKit.objects.all()
    # Use MealKitSerializer to serialize the queryset
    serializer_class = MealKitSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['price', 'chef__user__username']
    # Define ordering fields
    ordering_fields = ['price', 'name']
    # Define filterset fields
    filterset_fields = ['price']

class MealKitDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all MealKit objects
    queryset = MealKit.objects.all()
    # Use MealKitSerializer to serialize the queryset
    serializer_class = MealKitSerializer

# GiftCard Views
class GiftCardListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all GiftCard objects
    queryset = GiftCard.objects.all()
    # Use GiftCardSerializer to serialize the queryset
    serializer_class = GiftCardSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['value', 'status']
    # Define ordering fields
    ordering_fields = ['value', 'created_at']
    # Define filterset fields
    filterset_fields = ['value']

class GiftCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all GiftCard objects
    queryset = GiftCard.objects.all()
    # Use GiftCardSerializer to serialize the queryset
    serializer_class = GiftCardSerializer

# CartItem Views
class CartItemListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all CartItem objects
    queryset = CartItem.objects.all()
    # Use CartItemSerializer to serialize the queryset
    serializer_class = CartItemSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['quantity', 'meal_kit__name', 'customer__user__username']
    # Define ordering fields
    ordering_fields = ['quantity', 'created_at']
    # Define filterset fields
    filterset_fields = ['quantity']

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all CartItem objects
    queryset = CartItem.objects.all()
    # Use CartItemSerializer to serialize the queryset
    serializer_class = CartItemSerializer

# Order Views
class OrderListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all Order objects
    queryset = Order.objects.all()
    # Use OrderSerializer to serialize the queryset
    serializer_class = OrderSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['status', 'payment_status']
    # Define ordering fields
    ordering_fields = ['order_date', 'status']
    # Define filterset fields
    filterset_fields = ['status']

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Order objects
    queryset = Order.objects.all()
    # Use OrderSerializer to serialize the queryset
    serializer_class = OrderSerializer

# Review Views
class ReviewListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all Review objects
    queryset = Review.objects.all()
    # Use ReviewSerializer to serialize the queryset
    serializer_class = ReviewSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['rating', 'meal_kit__name']
    # Define ordering fields
    ordering_fields = ['review_date', 'rating']
    # Define filterset fields
    filterset_fields = ['rating']

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Review objects
    queryset = Review.objects.all()
    # Use ReviewSerializer to serialize the queryset
    serializer_class = ReviewSerializer

# Payment View
class PaymentView(APIView):
    def post(self, request):
        # Get the currently authenticated user
        user = request.user
        # Get the order ID from the request data
        order_id = request.data.get('order_id')
        # Retrieve the order by ID
        order = Order.objects.get(id=order_id)
        # Create a Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        # Create a Razorpay payment
        payment = client.order.create({
            'amount': int(order.meal_kit.price * 100),  # Amount in paisa
            'currency': 'INR',
            'payment_capture': '1'
        })
        # Set the order's payment status to pending
        order.payment_status = Order.PAYMENT_PENDING
        # Save the order
        order.save()
        # Return the payment details
        return Response(payment)
