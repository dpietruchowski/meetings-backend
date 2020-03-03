from django.db import models

class MeetingRoom(models.Model):
    name = models.CharField(max_length=30)
    capacity = models.IntegerField()

class Meeting(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(MeetingRoom, on_delete=models. CASCADE, blank=True, null=True)