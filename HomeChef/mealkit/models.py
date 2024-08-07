# Import AbstractUser for extending the default User model
from django.contrib.auth.models import AbstractUser
# Import models from Django's ORM
from django.db import models

# Custom User model extending AbstractUser
class User(AbstractUser):
    # Boolean field to check if the user is a chef
    is_chef = models.BooleanField(default=False)
    # Boolean field to check if the user is a customer
    is_customer = models.BooleanField(default=False)
    # Boolean field to check if the user is a company
    is_company = models.BooleanField(default=False)

# Model representing a Company
class Company(models.Model):
    # Choices for food type
    VEG = 'veg'
    NON_VEG = 'non_veg'
    BOTH = 'both'

    FOOD_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
        (BOTH, 'Both'),
    ]

    # Choices for meal category
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'

    CATEGORY_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]

    # One-to-one relationship with User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # Company name
    company_name = models.CharField(max_length=255)
    # Email address
    email = models.EmailField()
    # Food type choice
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES, default=BOTH)
    # Meal category choice
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=LUNCH)

    # String representation of the Company model
    def __str__(self):
        return self.company_name

# Model representing a Subscription Plan
class SubscriptionPlan(models.Model):
    # Choices for plan type
    PLAN_TYPE_CHOICES = [
        ('2peopleperweek', '2 People Per Week Plan'),
        ('4peopleperweek', '4 People Per Week Plan'),
    ]

    # Plan name with choices
    plan_name = models.CharField(max_length=255, choices=PLAN_TYPE_CHOICES, default='2peopleperweek')
    # Description of the plan
    description = models.TextField(blank=True, null=True)
    # Price of the plan
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Number of meals per week
    meals_per_week = models.IntegerField()
    # One-to-one relationship with Company model
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='subscription_plan')

    # String representation of the SubscriptionPlan model
    def __str__(self):
        return self.plan_name

# Model representing a Customer
class Customer(models.Model):
    # One-to-one relationship with User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # Customer name
    customer_name = models.CharField(max_length=20, null=True, blank=True)
    # Gender choice
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)
    # Age of the customer
    age = models.IntegerField(null=True, blank=True)
    # Mobile number of the customer
    mobile = models.CharField(max_length=10)
    # Address of the customer
    address = models.TextField(blank=True, null=True)
    # Foreign key relationship with SubscriptionPlan model
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='customers', blank=True)

    # String representation of the Customer model
    def __str__(self):
        return self.user.username

# Model representing a Meal Kit
class MealKit(models.Model):
    # Name of the meal
    meal_name = models.CharField(max_length=255)
    # Description of the meal
    description = models.TextField(blank=True)
    # Price of the meal
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Foreign key relationship with Customer model (chef)
    chef = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='meal_kits')
    # Ingredients of the meal
    ingredients = models.TextField()

    # String representation of the MealKit model
    def __str__(self):
        return self.meal_name

# Model representing a Chef Plan
class ChefPlan(models.Model):
    # One-to-one relationship with User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # One-to-one relationship with Customer model (chef)
    chef = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='chef_plan')
    # Name of the plan
    plan_name = models.CharField(max_length=255)
    # Cooking experience in years
    cooking_experience = models.IntegerField()
    # Type of event the chef plan is for
    event_type = models.CharField(max_length=255)
    # Price of the chef plan
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # String representation of the ChefPlan model
    def __str__(self):
        return self.plan_name

# Model representing an Order
class Order(models.Model):
    # Choices for order status
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    PAYMENT_PENDING = 'Pending'
    PAID = 'Paid'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAID, 'Paid'),
    ]

    # Foreign key relationship with Customer model (user)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    # Foreign key relationship with MealKit model
    meal_kit = models.ForeignKey(MealKit, on_delete=models.CASCADE, related_name='orders')
    # Status of the order
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    # Payment status of the order
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    # Date and time when the order was placed
    order_date = models.DateTimeField(auto_now_add=True)

    # String representation of the Order model
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# Model representing a Gift Card
class GiftCard(models.Model):
    # Choices for gift amount
    GIFT_AMOUNT_CHOICES = [
        (70, '$70'),
        (140, '$140'),
        (280, '$280')
    ]

    # Type of the gift
    gift_type = models.CharField(max_length=255, default='Meal')
    # Amount of the gift card
    gift_amount = models.IntegerField(choices=GIFT_AMOUNT_CHOICES)
    # Quantity of gift cards
    quantity = models.PositiveIntegerField(default=1)
    # Foreign key relationship with Customer model
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='giftcards')

    # String representation of the GiftCard model
    def __str__(self):
        return f"{self.gift_type} - {self.gift_amount}"

# Model representing a Cart Item
class CartItem(models.Model):
    # Foreign key relationship with Customer model (user)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    # Foreign key relationship with GiftCard model
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    # Quantity of the cart item
    quantity = models.PositiveIntegerField(default=1)

    # String representation of the CartItem model
    def __str__(self):
        return f"{self.user.username} - {self.gift_card}"

# Model representing a Review
class Review(models.Model):
    # Foreign key relationship with Customer model (user)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    # Foreign key relationship with MealKit model
    meal_kit = models.ForeignKey(MealKit, on_delete=models.CASCADE, related_name='reviews')
    # Rating given by the user
    rating = models.PositiveIntegerField()
    # Comment by the user
    comment = models.TextField()
    # Date and time when the review was created
    review_date = models.DateTimeField(auto_now_add=True)

    # String representation of the Review model
    def __str__(self):
        return f"Review {self.id} by {self.user.username}"
