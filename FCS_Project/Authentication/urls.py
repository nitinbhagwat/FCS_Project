from django.urls import path
from Authentication.views import SignUpView, change_premium_plan, login_user
from Transactions.views import upgrade_account


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_user, name='login'),
    path('upgrade-account/', upgrade_account, name='upgrade_account'),
    path('change-premium-plan/', change_premium_plan, name= 'change_premium_plan')
]