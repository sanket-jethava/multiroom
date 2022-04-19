import uuid
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.db import models
from django.urls.base import reverse


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice_record = models.FileField(
        upload_to="records", storage=RawMediaCloudinaryStorage())
    language = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("core:record_detail", kwargs={"id": str(self.id)})

class RoomMember(models.Model):
    room_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.room_name)


# class Room(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     room_name = models.CharField(max_length=100, null=True, blank=True)

#     class Meta:
#         verbose_name = "Room"
#         verbose_name_plural = "Rooms"
    
#     def __str__(self):
#         return str(self.id),str(self.room_name)

# class RoomMate(models.Model):
#     room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name = "Room Id")
#     user_id = 