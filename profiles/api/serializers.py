from cphapp.models import Device
from rest_framework import serializers

from profiles.models import Profile, SummaryCard
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class SummaryCardSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(
        choices=['sales', 'rebates', 'topups', 'cashin'])
    retailer = serializers.StringRelatedField()

    class Meta:
        model = SummaryCard
        fields = ['name', 'color', 'is_dark', 'retailer', 'title']


class DeviceHashSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['device_hash']


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.ImageField(read_only=True)
    devices = serializers.SerializerMethodField()
    cards = SummaryCardSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def get_devices(self, instance):
        return [device.device_hash for device in instance.devices.all()]


class ProfileAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['avatar']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'groups', 'profile']
