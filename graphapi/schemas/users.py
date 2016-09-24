import graphene
from graphene import AbstractType, Field, Node
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import User
from core.models import UserProfile


class UserProfileNode(DjangoObjectType):
    class Meta:
        model = UserProfile
        interfaces = (Node, )


class UserNode(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = User
        interfaces = (Node, )

    def resolve_name(self, args, *_):
        return " ".join([self.first_name, self.last_name])


class Query(AbstractType):
    all_users = DjangoFilterConnectionField(UserNode)