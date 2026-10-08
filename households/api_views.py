from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Household, HouseholdMember
from .serializers import HouseholdSerializer, HouseholdMemberSerializer


class HouseholdViewSet(viewsets.ModelViewSet):
    serializer_class = HouseholdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only show households the logged-in user actually belongs to
        return Household.objects.filter(members__user=self.request.user).distinct()

    def perform_create(self, serializer):
        household = serializer.save()
        HouseholdMember.objects.create(household=household, user=self.request.user, role='admin')

    @action(detail=False, methods=['post'])
    def join(self, request):
        code = request.data.get('invite_code', '').strip().upper()
        try:
            household = Household.objects.get(invite_code=code)
        except Household.DoesNotExist:
            return Response({'error': 'Invalid invite code'}, status=404)

        if HouseholdMember.objects.filter(household=household, user=request.user).exists():
            return Response({'message': f'Already a member of {household.name}'}, status=200)

        HouseholdMember.objects.create(household=household, user=request.user, role='member')
        return Response({'message': f'Joined {household.name}'}, status=201)


class HouseholdMemberViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HouseholdMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HouseholdMember.objects.filter(household__members__user=self.request.user).distinct()