from django.urls import path
from . import views


urlpatterns = [
    # sign-up/sign-in process
    path("sign-up/", views.UserSignUp.as_view(), name="users_sign_up"),
    path('otp-verification/', views.OtpVerification.as_view(), name="users_otp_verify"),
    path('resend-otp/', views.ResendOtp.as_view(), name="resend_otp"),
    path("sign-in/", views.SignIn.as_view(), name="users_sign_in"),
    path("forgot-password/", views.ForgotPassword.as_view(), name="users_forgot_password"),
    path('forgot-otp-verify/', views.ValidateForgetPasswordOTP.as_view(), name="users_forgot_otp_verify"),
    path("reset-password/", views.ResetPassword.as_view(), name="users_reset_password"),
    path("change-password/", views.ChangePassword.as_view(), name="users_change_password"),
    path("logout/", views.LogoutApiView.as_view(), name="users_logout"),
    path("report/", views.ReportApiView.as_view(), name="users_reports"),
    path("Contact-Us/", views.ContactUsApiView.as_view(), name="users_contact_us"),
    path("english-level/", views.EnglishLevelApiView.as_view(), name="users_english_level"),
    # Onboarding process
    path("user-aim/", views.UserAimApiView.as_view(), name="onboarding_user_aim"),
    path("your-goal/", views.UserGoalApiView.as_view(), name="onboarding_user_goal_api"),
    path("choose-topics/", views.ChooseTopicsApiView.as_view(), name="choose_topics"),
    path("goal/", views.GoalApiView.as_view(), name="onboarding_goal_api"),
    path("user-onboarding/", views.UserOnboardingApiView.as_view(), name="user_onboarding"),
    path("select-level/", views.SelectLevelApi.as_view(), name="level"),
    # home process
    path("home/", views.HomeApiView.as_view(), name="home"),
    path("goal-update/", views.UpdateGoalApiView.as_view(), name="goal_update"),
    path("translate/", views.TranslateApiView.as_view(), name="translate"),
    path("event/", views.EventApiView.as_view(),name="create_event"),
    # add friend
    path("add-friend/", views.FriendRequestApiView.as_view(),name="add_friend"),
    path("manage-request/<uuid:pk>/", views.ManageFriendRequestApiView.as_view(),name="manage_request"),
    path("user-profile/", views.UserProfileApiView.as_view(), name="user_profile"),
]