from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random,time, json
from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def lobby(request):
    return render(request,'base/lobby.html')

def room(request):
    return render(request,'base/room.html')

def getToken(request):
    appId = 'b89b85f7677e4fc1b6a1af59a1089334'
    appCertificate = '329dd0af04f84f16a21f02e60a27e9a0'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid},safe=False)




@csrf_exempt
def createMember(request):
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name']
    )
    return JsonResponse({'name':data['name']},safe=False)



def getMember(request):
    uid = request.GET.get()
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name},safe=False)








