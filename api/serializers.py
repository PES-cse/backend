from rest_framework import serializers
from users.models import Certification, Research, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'phone_no', 'aadhar_no', 'joined_date')


class CertificationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Certification
        fields = ('title', 'date', 'agency_name', 'place', 'username')


class ResearchSerializer(serializers.ModelSerializer):
    usernames = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)

    class Meta:
        model = Research
        fields = ('title', 'date', 'agency_name', 'place', 'usernames')
