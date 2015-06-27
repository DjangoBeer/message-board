from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from django.core.files import File

import base64


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Message.objects.all()

    @list_route(methods=['get'], permission_classes=[permissions.AllowAny])
    def all(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        photo_file = None
        if 'photo' in self.request.data:
            photo = base64.b64decode(self.request.data['photo'])
            with open('media/img/snapshot.jpg', 'wb') as f:
                f.write(photo)
                photo_file = File(f, name='snapshot.jpg')
        serializer.save(
            author=self.request.user,
            message=self.request.data['message'],
            image=photo_file
        )
