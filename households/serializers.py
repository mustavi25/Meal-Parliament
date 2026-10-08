import secrets
from rest_framework import serializers
from .models import Household, HouseholdMember


class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ['id', 'name', 'invite_code', 'created_at']
        read_only_fields = ['created_at']
        extra_kwargs = {'invite_code': {'required': False, 'validators': []}}

    def validate_invite_code(self, value):
        value = value.strip().upper()
        if value:
            qs = Household.objects.filter(invite_code=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("That invite code is already taken.")
        return value

    def create(self, validated_data):
        # If no code was typed in, generate a random unique one
        if not validated_data.get('invite_code'):
            while True:
                code = secrets.token_hex(3).upper()
                if not Household.objects.filter(invite_code=code).exists():
                    validated_data['invite_code'] = code
                    break
        return super().create(validated_data)


class HouseholdMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    household_name = serializers.CharField(source='household.name', read_only=True)

    class Meta:
        model = HouseholdMember
        fields = ['id', 'household', 'household_name', 'user', 'username', 'role', 'joined_at']
        read_only_fields = ['joined_at']