from django.urls import path
from .views import SignupView, LoginView, UserView, get_csrf_token, logout_view, ProviderListView, AppointmentListCreateView, AppointmentDetailView, available_time_slots

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/user/', UserView.as_view(), name='user'),
    path('auth/logout/', logout_view),
    path('providers/', ProviderListView.as_view()),
    path('providers/<int:provider_id>/timeslots/', available_time_slots),
    path('appointments/', AppointmentListCreateView.as_view()),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view()),
    path('csrf/', get_csrf_token)
]
