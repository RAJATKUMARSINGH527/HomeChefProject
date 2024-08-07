from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view as get_swagger_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as get_redoc_view

# Swagger schema view for API documentation
schema_view = get_swagger_view(
    openapi.Info(
        title="HomeChef API",
        default_version='v1',
        description="API documentation for HomeChef",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# ReDoc schema view for alternative API documentation
redoc_view = get_redoc_view(
    openapi.Info(
        title="HomeChef API",
        default_version='v1',
        description="API documentation for HomeChef",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL pattern for user registration
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),

    # URL pattern for user login
    path('login/', UserLoginView.as_view(), name='login'),

    # URL pattern for listing customers view
    path('customers/', CustomerListView.as_view(), name='customer-list'),
     # URL pattern for customers detail view
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),

    # URL pattern for listing companies
    path('companies/', CompanyListView.as_view(), name='company-list'),
    # URL pattern for company detail view
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    # URL pattern for listing chef plans
    path('chef-plans/', ChefPlanListView.as_view(), name='chef-plan-list'),
    # URL pattern for chef plan detail view
    path('chef-plans/<int:pk>/', ChefPlanDetailView.as_view(), name='chef-plan-detail'),

    # URL pattern for listing subscription plans
    path('subscription-plans/', SubscriptionPlanListView.as_view(), name='subscription-plan-list'),
    # URL pattern for subscription plan detail view
    path('subscription-plans/<int:pk>/', SubscriptionPlanDetailView.as_view(), name='subscription-plan-detail'),

    # URL pattern for listing meal kits
    path('meal-kits/', MealKitListView.as_view(), name='meal-kit-list'),
    # URL pattern for meal kit detail view
    path('meal-kits/<int:pk>/', MealKitDetailView.as_view(), name='meal-kit-detail'),

    # URL pattern for listing gift cards
    path('gift-cards/', GiftCardListView.as_view(), name='gift-card-list'),
    # URL pattern for gift card detail view
    path('gift-cards/<int:pk>/', GiftCardDetailView.as_view(), name='gift-card-detail'),

    # URL pattern for listing cart items
    path('cart-items/', CartItemListView.as_view(), name='cart-item-list'),
    # URL pattern for cart item detail view
    path('cart-items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),

    # URL pattern for listing orders
    path('orders/', OrderListView.as_view(), name='order-list'),
    # URL pattern for order detail view
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # URL pattern for listing reviews
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    # URL pattern for review detail view
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # URL pattern for payment processing
    path('razorpay/', RazorpayPaymentView.as_view(), name='razorpay-payment'),
    path('verify/', VerifyPaymentView.as_view(), name='verify-payment'),
    
    # URL pattern for Swagger UI documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # URL pattern for ReDoc documentation
    path('redoc/', redoc_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
]
