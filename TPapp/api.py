from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Ds18b20
from .serializer import dstser



@api_view(['Get'])
def Dlist(request):
    all_data = Ds18b20.objects.all()
    data = dstser(all_data,many=True).data

    return Response({'data':data})


class Dsviews(generics.CreateAPIView):
    queryset = Ds18b20.objects.all()
    serializer_class = dstser
