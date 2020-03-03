from django.urls import path
from . import views

urlpatterns = [
  path('rooms/<int:pk>', views.MeetingRoomView.as_view(), name='room'),
  path('rooms', views.MeetingRoomListView.as_view(), name='rooms'),
  path('meetings/<int:pk>', views.MeetingView.as_view(), name='meeting'),
  path('meetings', views.MeetingListView.as_view(), name='meetings'),
]
