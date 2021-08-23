
import secrets


from rest_framework import generics, views
from authentication.models import User
from rest_framework.response import Response
from rest_framework import permissions
from authentication.serializers import UserSerializer


class SelectWinner(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.filter(is_staff=False).filter(is_superuser=False).filter(is_verified=True)
        user = secrets.choice(users)
        user  = self.serializer_class(instance = user)


        message = f"winner is {user.data.get('username')}"
        data = {
            'message':message,
            'info-user': user.data

        }

        return Response(data)