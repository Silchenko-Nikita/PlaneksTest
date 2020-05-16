from django.conf.urls import url

from crm.views import RegisterFormView, EmailConfirmationFailView, EmailConfirmationSuccessView, EmailConfirmationView, \
    ActivateView, LoginFormView, ProfileView, logout, AvatarUploadView, GuestProfileView

urlpatterns = [
    url(r'register', RegisterFormView.as_view(), name='register'),
    url(r'login', LoginFormView.as_view(), name='login'),
    url(r'logout', logout, name="logout"),

    url(r'^profile/?$', ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<pk>[0-9]+)$', GuestProfileView.as_view(), name='guest-profile'),
    url(r'avatar-upload', AvatarUploadView.as_view(), name='avatar-upload'),

    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', ActivateView.as_view(), name='activate'),
    url(r'confirm-success', EmailConfirmationSuccessView.as_view(), name='confirm-success'),
    url(r'confirm-failure', EmailConfirmationFailView.as_view(), name='confirm-failure'),
    url(r'confirm', EmailConfirmationView.as_view(), name='confirm'),
]

