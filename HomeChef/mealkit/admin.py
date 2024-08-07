from django.contrib import admin
from .models import *

# Customize the User model admin interface
class UserAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('username', 'email', 'is_chef', 'is_customer', 'is_company', 'is_staff', 'is_active')
    # Enable search functionality on these fields
    search_fields = ('username', 'email')
    # Add filter options for these fields
    list_filter = ('is_chef', 'is_customer', 'is_company', 'is_staff', 'is_active')

# Customize the Company model admin interface
class CompanyAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('company_name', 'email', 'food_type', 'category')
    # Enable search functionality on these fields
    search_fields = ('company_name', 'email')
    # Add filter options for these fields
    list_filter = ('food_type', 'category')

# Customize the SubscriptionPlan model admin interface
class SubscriptionPlanAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('plan_name', 'description', 'price', 'meals_per_week', 'company')
    # Enable search functionality on these fields
    search_fields = ('plan_name', 'company__company_name')
    # Add filter options for these fields
    list_filter = ('price',)

# Customize the Customer model admin interface
class CustomerAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('customer_name', 'gender', 'age', 'mobile', 'address', 'subscription_plan')
    # Enable search functionality on these fields
    search_fields = ('customer_name', 'user__username', 'mobile')
    # Add filter options for these fields
    list_filter = ('gender', 'subscription_plan')

# Customize the MealKit model admin interface
class MealKitAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('meal_name', 'price', 'chef')
    # Enable search functionality on these fields
    search_fields = ('meal_name', 'chef__user__username')
    # Add filter options for these fields
    list_filter = ('price',)

# Customize the Order model admin interface
class OrderAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('user', 'meal_kit', 'status', 'payment_status', 'order_date')
    # Enable search functionality on these fields
    search_fields = ('user__user__username', 'meal_kit__meal_name')
    # Add filter options for these fields
    list_filter = ('status', 'payment_status', 'order_date')

# Customize the Review model admin interface
class ReviewAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('user', 'meal_kit', 'rating', 'review_date')
    # Enable search functionality on these fields
    search_fields = ('user__user__username', 'meal_kit__meal_name')
    # Add filter options for these fields
    list_filter = ('rating', 'review_date')

# Customize the ChefPlan model admin interface
class ChefPlanAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('chef', 'plan_name', 'cooking_experience', 'event_type', 'price')
    # Enable search functionality on these fields
    search_fields = ('chef__user__username', 'plan_name')
    # Add filter options for these fields
    list_filter = ('price', 'cooking_experience', 'event_type')

# Customize the GiftCard model admin interface
class GiftCardAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('gift_type', 'gift_amount', 'quantity', 'customer')
    # Enable search functionality on these fields
    search_fields = ('gift_type', 'customer__user__username')
    # Add filter options for these fields
    list_filter = ('gift_amount',)

# Customize the CartItem model admin interface
class CartItemAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('user', 'gift_card', 'quantity')
    # Enable search functionality on these fields
    search_fields = ('user__user__username', 'gift_card__gift_type')
    # Add filter options for these fields
    list_filter = ('quantity',)

# Register models and their corresponding admin classes with the Django admin site
admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(MealKit, MealKitAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ChefPlan, ChefPlanAdmin)
admin.site.register(GiftCard, GiftCardAdmin)
admin.site.register(CartItem, CartItemAdmin)
