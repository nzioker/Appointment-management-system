from django.urls import path
from .views import (
    SignupUserView, SignupProviderView, ProviderListView,
    SlotCreateView, SlotListView, AppointmentCreateView, AppointmentListView, ProviderAppointmentsView,
    logout_view, LoginView, get_csrf_token
)

urlpatterns = [
    path('auth/signup-user/', SignupUserView.as_view()),
    path('auth/signup-provider/', SignupProviderView.as_view()),
    path('auth/logout/', logout_view),

    path('auth/login/', LoginView.as_view()),

    path('providers/', ProviderListView.as_view()),
    path('slots/', SlotListView.as_view()),
    path('slots/create/', SlotCreateView.as_view()),

    path('appointments/', AppointmentListView.as_view()),
    path('appointments/create/', AppointmentCreateView.as_view()),

    path('appointments/provider/', ProviderAppointmentsView.as_view()),


    path('auth/csrf/', get_csrf_token),

]
