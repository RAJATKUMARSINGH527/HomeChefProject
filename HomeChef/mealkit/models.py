from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_chef = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

class Company(models.Model):
    VEG = 'veg'
    NON_VEG = 'non_veg'
    BOTH = 'both'

    FOOD_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
        (BOTH, 'Both'),
    ]

    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'

    CATEGORY_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    email = models.EmailField()
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES, default=BOTH)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=LUNCH)

    def __str__(self):
        return self.company_name
    
class SubscriptionPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('2peopleperweek', '2 People Per Week Plan'),
        ('4peopleperweek', '4 People Per Week Plan'),
        
    ]

    plan_name = models.CharField(max_length=255, choices=PLAN_TYPE_CHOICES, default='2peopleperweek')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    meals_per_week = models.IntegerField()
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='subscription_plan')
    
    def __str__(self):
        return self.plan_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)
    age = models.IntegerField(null=True, blank=True)
    mobile = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='customers', blank=True)

    def __str__(self):
        return self.user.username


class MealKit(models.Model):
    meal_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    chef = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='meal_kits')
    ingredients = models.TextField()

    def __str__(self):
        return self.meal_name

class ChefPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    chef = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='chef_plan')
    plan_name = models.CharField(max_length=255)
    cooking_experience = models.IntegerField()
    event_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.plan_name

class Order(models.Model):
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

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    meal_kit = models.ForeignKey(MealKit, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class GiftCard(models.Model):
    GIFT_AMOUNT_CHOICES = [
        (70, '$70'),
        (140, '$140'),
        (280, '$280')
    ]
    gift_type = models.CharField(max_length=255,default='Meal')
    gift_amount = models.IntegerField(choices=GIFT_AMOUNT_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='giftcards')

    def __str__(self):
        return f"{self.gift_type} - {self.gift_amount}"

class CartItem(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.gift_card}"

class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    meal_kit = models.ForeignKey(MealKit, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} by {self.user.username}"
