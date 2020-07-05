from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("register", views.register, name="register"),
    path("registeragent", views.registeragent, name="registeragent"),
    path("loginpage", views.loginpage, name="login"),
    path("resetpassword", views.resetpassword, name="resetpassword"),
    path("registerapi", views.user_registrationapi, name="registerapi"),
    path("contactus", views.contactusapi, name="contactus"),
    path("team", views.ourteam, name="team"),
    path("faq", views.faq, name="faq"),
    path("privatepolicy", views.privatepolicy, name="privatepolicy"),
    path("subscribe", views.subscribeapi, name="subscribe"),
    path("agentregisterapi", views.agent_registrationapi, name="agentregisterapi"),
    path("loginapi", views.user_loginapi, name="loginapi"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard_agent", views.dashboard_agent, name="dashboard_agent"),
    path("dashboard_admin", views.dashboard_admin, name="dashboard_admin"),
    path("profile", views.profile, name="profile"),
    path("transaction_agent_search", views.transaction_agent_search, name="transaction_agent_search"),
    path("transaction_user_search", views.transaction_user_search, name="transaction_user_search"),
    path("profile_agent", views.profile_agent, name="profile_agent"),
    path("wallet", views.wallet, name="wallet"),
    path("wallet_agent", views.wallet_agent, name="wallet_agent"),
    path("notification", views.notification, name="notification"),
    path("signout", views.signout, name="signout"),
    path("update_biodata", views.update_biodata, name="update_biodata"),
    path("redeem_coins", views.redeem_coins, name="redeem_coins"),
    path("send_coins", views.send_coins, name="send_coins"),
    path("update_agent_biodata", views.update_agent_biodata, name="update_agent_biodata"),
    path("dashboard_query", views.dashboard_search_query, name="dashboard_query"),
    # path("resend_code", views.resend_code, name="resend_code"),
    path("update_account", views.update_account, name="update_account"),
    path("update_agent_account", views.update_agent_account, name="update_agent_account"),
    
]

