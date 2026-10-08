from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from households.models import Household
from .models import MealItem, Ingredient, MealSlot
from .serializers import MealItemSerializer, IngredientSerializer, MealSlotSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]


class MealItemViewSet(viewsets.ModelViewSet):
    queryset = MealItem.objects.all()
    serializer_class = MealItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MealSlotViewSet(viewsets.ModelViewSet):
    serializer_class = MealSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MealSlot.objects.filter(household__members__user=self.request.user).distinct()

    def perform_create(self, serializer):
        household = serializer.validated_data['household']
        is_member = household.members.filter(user=self.request.user).exists()
        if not is_member:
            raise ValidationError("You're not a member of that household.")
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError("This household already has that meal type booked for that date.")