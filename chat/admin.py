from django.contrib import admin

from .models import Record,RoomMember


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "language", "voice_record")

@admin.register(RoomMember)
class RoomAdmin(admin.ModelAdmin):
    list_display = ( "room_name",)

