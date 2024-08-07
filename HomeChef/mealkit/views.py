# Import necessary modules and classes from rest_framework and other packages
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
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

# Customer Register View
class CustomerRegisterView(generics.CreateAPIView):
    # Allow any user to access this view
    permission_classes = [AllowAny]
    # Use the CustomerRegisterSerializer for this view
    serializer_class = CustomerRegisterSerializer

    def post(self, request, *args, **kwargs):
        # Serialize the incoming data
        serializer = self.get_serializer(data=request.data)
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

# Customer List View
class CustomerListView(generics.ListAPIView):
    # Define the queryset to retrieve all Customer objects
    queryset = Customer.objects.all()
    # Use CustomerSerializer to serialize the queryset
    serializer_class = CustomerSerializer
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['customer_name', 'age']
    # Define ordering fields
    ordering_fields = ['customer_name', 'age']
    # Define filterset fields
    filterset_fields = ['customer_name']

# Customer Detail View
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Customer objects
    queryset = Customer.objects.all()
    # Use CustomerSerializer to serialize the queryset
    serializer_class = CustomerSerializer

# Company List View
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
    ordering_fields = ['company_name', 'food_type']
    # Define filterset fields
    filterset_fields = ['company_name']

# Company Detail View
class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Company objects
    queryset = Company.objects.all()
    # Use CompanySerializer to serialize the queryset
    serializer_class = CompanySerializer

# Chef Plan List View
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

# Chef Plan Detail View
class ChefPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all ChefPlan objects
    queryset = ChefPlan.objects.all()
    # Use ChefPlanSerializer to serialize the queryset
    serializer_class = ChefPlanSerializer

# Subscription Plan List View
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

# Subscription Plan Detail View
class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all SubscriptionPlan objects
    queryset = SubscriptionPlan.objects.all()
    # Use SubscriptionPlanSerializer to serialize the queryset
    serializer_class = SubscriptionPlanSerializer

# Meal Kit List View
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
    ordering_fields = ['price', 'meal_name']
    # Define filterset fields
    filterset_fields = ['price']

# Meal Kit Detail View
class MealKitDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all MealKit objects
    queryset = MealKit.objects.all()
    # Use MealKitSerializer to serialize the queryset
    serializer_class = MealKitSerializer

# Gift Card List View
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

# Gift Card Detail View
class GiftCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all GiftCard objects
    queryset = GiftCard.objects.all()
    # Use GiftCardSerializer to serialize the queryset
    serializer_class = GiftCardSerializer

# Cart Item List View
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

# Cart Item Detail View
class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all CartItem objects
    queryset = CartItem.objects.all()
    # Use CartItemSerializer to serialize the queryset
    serializer_class = CartItemSerializer

# Review List View
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
    search_fields = ['rating', 'comment', 'meal_kit__name', 'customer__user__username']
    # Define ordering fields
    ordering_fields = ['rating', 'created_at']
    # Define filterset fields
    filterset_fields = ['rating']

# Review Detail View
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Review objects
    queryset = Review.objects.all()
    # Use ReviewSerializer to serialize the queryset
    serializer_class = ReviewSerializer

# # Razorpay Payment View
# class RazorpayPaymentView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Create Razorpay client using API keys from settings
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         # Get amount and currency from the request data
#         amount = request.data.get('amount')
#         currency = request.data.get('currency', 'INR')
#         # Create order on Razorpay
#         payment = client.order.create({
#             'amount': amount,
#             'currency': currency,
#             'payment_capture': '1'
#         })
#         # Return the payment details
#         return Response(payment)
    
class RazorpayPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        # Create Razorpay client using API keys from settings
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Get amount and currency from the request data
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'INR')
        user_id = request.data.get('user_id')
        meal_kit_id = request.data.get('meal_kit_id')
        
        if not amount or not user_id or not meal_kit_id:
            return Response({"error": "Amount, user ID, and meal kit ID are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create an order on Razorpay
        payment = client.order.create({
            'amount': int(amount) * 100,  # Amount should be in paise
            'currency': currency,
            'payment_capture': '1'
        })
        
        razorpay_order_id = payment['id']
        
        # Create an order in your system
        order = Order.objects.create(
            user_id=user_id,
            meal_kit_id=meal_kit_id,
            total_price=amount,
            razorpay_order_id=razorpay_order_id
        )
        
        # Return the payment details and order ID
        return Response({
            'order_id': razorpay_order_id,
            'amount': amount,
            'currency': currency,
            'order': order.id
        })

class VerifyPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')
        order_id = request.data.get('order_id')

        # Verify the payment signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = Order.objects.get(id=order_id)
        
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            
            # Update the order status
            order.payment_status = Order.PAID
            order.status = Order.COMPLETED
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.save()
            
            return Response({"success": "Payment verified and order completed"})
        
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

# Order List View
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
    search_fields = ['total_price', 'status', 'customer__user__username']
    # Define ordering fields
    ordering_fields = ['total_price', 'created_at']
    # Define filterset fields
    filterset_fields = ['total_price']

# Order Detail View
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Order objects
    queryset = Order.objects.all()
    # Use OrderSerializer to serialize the queryset
    serializer_class = OrderSerializer
