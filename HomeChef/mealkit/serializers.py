from rest_framework import serializers
from .models import User, Customer, MealKit, Order, Review, SubscriptionPlan, Company, ChefPlan, GiftCard, CartItem
from django.contrib.auth.hashers import make_password


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

 
# Serializer for the Company model
class CompanyRegisterSerializer(serializers.ModelSerializer):
    # Field for password that is write-only
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'password', 'email', 'food_type', 'category']

    def create(self, validated_data):
        # Extract name and password from validated data
        company_name = validated_data.get('company_name')
        password = validated_data.pop('password')
        # Hash the password
        password = make_password(password)
        # Extract email
        email = validated_data.get('email')
        # Create a User object for the company
        user = User.objects.create_user(username=company_name, password=password, email=email, is_company=True)
        # Create a Company object and associate it with the User object
        company = Company.objects.create(user=user, **validated_data)
        return company

# Serializer for the SubscriptionPlan model
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    # Nested CompanySerializer to include company details in the subscription plan
    company = CompanySerializer(read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    subscription_plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'


# Serializer for the User model, which is used for Customer
class CustomerRegisterSerializer(serializers.ModelSerializer):
   
    # Fields for username and password, with password being write-only
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    # Nested SubscriptionPlanSerializer to include subscription plan details
    subscription_plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'password', 'customer_name', 'age', 'gender', 'mobile', 'address', 'subscription_plan']

    def create(self, validated_data):
        # Extract username and password from validated data
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.get('email')

         # Extract subscription plan if provided
        subscription_plan_data = validated_data.pop('subscription_plan', None)

        # Create a User object for the customer
        user = User.objects.create_user(username=username, password=password, email=email, is_customer=True)
        # Create a Customer object and associate it with the User object
        customer = Customer.objects.create(user=user, **validated_data)

        # If subscription plan is provided, set it for the customer
        if subscription_plan_data:
            subscription_plan = SubscriptionPlan.objects.create(**subscription_plan_data)
            customer.subscription_plan = subscription_plan
            customer.save()
        
        return customer

# Serializer for the MealKit model
class MealKitSerializer(serializers.ModelSerializer):
    # Nested UserSerializer to include chef details in the meal kit
    chef = CustomerSerializer(read_only=True)

    class Meta:
        model = MealKit
        fields = '__all__'

# Serializer for the ChefPlan model
class ChefPlanSerializer(serializers.ModelSerializer):
    # Nested UserSerializer to include chef details in the chef plan
    chef = CustomerSerializer(read_only=True)

    class Meta:
        model = ChefPlan
        fields = '__all__'

# Serializer for the GiftCard model
class GiftCardSerializer(serializers.ModelSerializer):
    # Nested UserSerializer to include customer details in the gift card
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = GiftCard
        fields = '__all__'

# Serializer for the CartItem model
class CartItemSerializer(serializers.ModelSerializer):
    # Nested UserSerializer to include user details in the cart item
    user = CustomerSerializer(read_only=True)
    # Nested GiftCardSerializer to include gift card details in the cart item
    gift_card = GiftCardSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'

# Serializer for the Order model
class OrderSerializer(serializers.ModelSerializer):
    # Nested UserSerializer to include user details in the order
    user = CustomerSerializer(read_only=True)
    # Nested MealKitSerializer to include meal kit details in the order
    meal_kit = MealKitSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

# Serializer for the Review model
class ReviewSerializer(serializers.ModelSerializer):
    # Nested UserSerializer to include user details in the review
    user = CustomerSerializer(read_only=True)
    # Nested MealKitSerializer to include meal kit details in the review
    meal_kit = MealKitSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
