import requests
from django.http import StreamingHttpResponse
from .tasks import NetWorker

class Crack:
    def down_music(request):
        name = request.GET.get("name")



        reponse = StreamingHttpResponse('')
        reponse['Content-Type'] = 'application/octet-stream'
        reponse['Content-Disposition'] = 'attachment;filename="example.mp3"'

        return reponse
