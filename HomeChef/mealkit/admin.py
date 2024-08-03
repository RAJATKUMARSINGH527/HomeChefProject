from django.contrib import admin
from .models import User, Company, SubscriptionPlan, Customer, MealKit, Order, Review, ChefPlan, GiftCard, CartItem


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_chef', 'is_customer', 'is_company', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_chef', 'is_customer', 'is_company', 'is_staff', 'is_active')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'food_type', 'category')
    search_fields = ('company_name', 'email')
    list_filter = ('food_type', 'category')

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'description', 'price', 'meals_per_week', 'company')
    search_fields = ('plan_name', 'company__company_name')
    list_filter = ('price',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'gender', 'age', 'mobile', 'address', 'subscription_plan')
    search_fields = ('customer_name', 'user__username', 'mobile')
    list_filter = ('gender', 'subscription_plan')

class MealKitAdmin(admin.ModelAdmin):
    list_display = ('meal_name', 'price', 'chef')
    search_fields = ('meal_name', 'chef__user__username')
    list_filter = ('price',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_kit', 'status', 'payment_status', 'order_date')
    search_fields = ('user__user__username', 'meal_kit__meal_name')
    list_filter = ('status', 'payment_status', 'order_date')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_kit', 'rating', 'review_date')
    search_fields = ('user__user__username', 'meal_kit__meal_name')
    list_filter = ('rating', 'review_date')

class ChefPlanAdmin(admin.ModelAdmin):
    list_display = ('chef', 'plan_name', 'cooking_experience', 'event_type', 'price')
    search_fields = ('chef__user__username', 'plan_name')
    list_filter = ('price', 'cooking_experience', 'event_type')

class GiftCardAdmin(admin.ModelAdmin):
    list_display = ('gift_type', 'gift_amount', 'quantity', 'customer')
    search_fields = ('gift_type', 'customer__user__username')
    list_filter = ('gift_amount',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'gift_card', 'quantity')
    search_fields = ('user__user__username', 'gift_card__gift_type')
    list_filter = ('quantity',)

admin.site.register(User,UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(MealKit, MealKitAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ChefPlan, ChefPlanAdmin)
admin.site.register(GiftCard, GiftCardAdmin)
admin.site.register(CartItem, CartItemAdmin)
