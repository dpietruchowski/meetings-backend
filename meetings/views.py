from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from common.views import (
    dict_object,
    BaseView,
    QueryView
)
from .models import (
    MeetingRoom,
    Meeting
)

import json
import pdb

class MeetingRoomListView(QueryView):
    queries = [u'query']
    model_class = MeetingRoom
    form = ['name', 'capacity']


class MeetingRoomView(BaseView):
    model_class = MeetingRoom
    form = ['name', 'capacity']


class MeetingListView(QueryView):
    queries = [u'query']
    model_class = Meeting
    form = ['date', 'start_time', 'end_time']


class MeetingView(BaseView):
    model_class = Meeting
    form = ['date', 'start_time', 'end_time']