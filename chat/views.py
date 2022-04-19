from django.shortcuts import render

from .utils import get_turn_info
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import render

from .models import Record, RoomMember
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def record(request):
    if request.method == "POST":
        print("file saving start--------=========")
        audio_file = request.FILES.get("video")
        language = request.POST.get("language")
        record = Record.objects.create(language=language, voice_record=audio_file)
        record.save()
        messages.success(request, "Audio recording successfully added!")
        print("\n\n\n=============================\nrecording saved in database",record,"\n\n\n")
        return JsonResponse(
            {
                "url": record.get_absolute_url(),
                "success": True,
            }
        )
    context = get_turn_info()
    return render(request, "chat/peer.html", context)

def peer(request):
    # get numb turn info
    context = get_turn_info()
    print('context context context context: ', context)

    return render(request, 'chat/peer.html', context=context)

def create_or_join(request):
    if request.method == "POST":
        roomname = request.POST.get("roomname")
        try:
            if RoomMember.objects.get(room_name = roomname):
                return render(request,'chat/index.html',{'error':f'Room Already Exists with name - '+roomname})
        except:
            pass
        room = RoomMember.objects.create(room_name = roomname)
        room.save()
        return render(request,'chat/peer.html',{'roomname':roomname,'isCreater':True})

    return render(request,'chat/index.html')

def temp_redirect(request):
    print("inside temp_redirect")
    return render(request,'main.html',{'error':'Room Not Exists!'})