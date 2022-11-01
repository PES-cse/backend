from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets

from users.models import Certification, User, Research
from .serializers import ResearchSerializer, UserSerializer, CertificationSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/token',
        'token/refresh',
        'users',
        'certifications'
    ]

    return Response(routes)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(User, username=item)

    def get_queryset(self):
        return User.objects.all()


class CertificationViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Certification, user__username=item)

    def get_queryset(self):
        return Certification.objects.all()

    # @action(detail=False)
    # def get_certifications_by_user(self, request, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return Certification.objects.get(agency_name='test place')


class ResearchViewSet(viewsets.ModelViewSet):
    serializer_class = ResearchSerializer

    def get_queryset(self):
        return Research.objects.all()

    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(Certification, username=item)

    # @action(detail=False, url_path=r'{username}')
    # def get_research_by_user(self, request, **kwargs):
    #     item = self.kwargs.get('pk')
    #     print(item)
    #     return Research.objects.filter(users__user__username=item)
