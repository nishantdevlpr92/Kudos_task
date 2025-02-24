from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Kudos
from .serializers import KudosSerializer, UserSerializer


User = get_user_model()

class SendKudosView(APIView):
    """
    API view to allow authenticated users to send kudos to other users.
    This view ensures that:
    - The user has remaining kudos for the week.
    - A user cannot send kudos to themselves.
    - The sender and receiver must belong to the same organization.
    - The message cannot be empty or just spaces.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get("receiver")
        message = request.data.get("message")

        if not all([receiver_id, message]) or not message.strip():
            return Response({"error": "Receiver and non-empty message are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(id=receiver_id, organization=sender.organization)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found or in a different organization"}, status=status.HTTP_404_NOT_FOUND)

        if sender == receiver:
            return Response({"error": "You cannot send kudos to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if sender.remaining_kudos <= 0:
            return Response({"error": "Weekly kudos limit reached"}, status=status.HTTP_400_BAD_REQUEST)

        Kudos.objects.create(sender=sender, receiver=receiver, message=message)
        sender.remaining_kudos -= 1
        sender.save(update_fields=["remaining_kudos"])

        return Response({
            "message": "Kudos sent successfully",
            "kudos": {
                "sender": sender.username,
                "receiver": receiver.username,
                "message": message,
            }
        }, status=status.HTTP_201_CREATED)


class ReceivedKudosView(APIView):
    """
    API view to retrieve the kudos received by the authenticated user during the current week.
    The kudos are ordered by the most recent first.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_of_week = now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now().weekday())
        kudos = Kudos.objects.filter(receiver=request.user, created_at__gte=start_of_week).order_by('-created_at')
        return Response(KudosSerializer(kudos, many=True).data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    API view to retrieve the current logged-in user's details, including the remaining kudos
    for the week and the number of kudos they have sent this week.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # Fetch the user from the database with the remaining_kudos field
        user_data = UserSerializer(user).data
        user_data['remaining_kudos'] = User.objects.get(id=user.id).remaining_kudos
        return Response({"user": user_data})

class KudosPagination(PageNumberPagination):
    """ Custom pagination class for Kudos API """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class UsersListAPIView(APIView):
    """
    API to retrieve a list of users in the same organization as the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_org = request.user.organization
        if not user_org:
            return Response({"message": "You are not part of any organization."}, status=400)

        users = User.objects.filter(organization=user_org).exclude(id=request.user.id)
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=200)
