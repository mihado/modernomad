import graphene
from graphene import AbstractType, Field, Node
from graphene_django.types import DjangoObjectType
from graphene.types import String
from graphene_django.filter import DjangoFilterConnectionField
from .users import UserNode
from core.models import Booking, Location
from django.contrib.auth.models import User


class BookingNode(DjangoObjectType):
    occupants = graphene.List(lambda: UserNode)

    class Meta:
        model = Booking
        interfaces = (Node, )
        filter_fields = ['arrive', 'location']
        filter_order_by = True

    def resolve_occupants(self, args, *_):
        return User.objects.all()[:15]


class Query(AbstractType):
    my_bookings = DjangoFilterConnectionField(BookingNode)

    def resolve_my_bookings(self, args, context, info):
        if not context.user.is_authenticated():
            return Booking.objects.none()
        else:
            return Booking.objects.filter(user=context.user)
