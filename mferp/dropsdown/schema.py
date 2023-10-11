import graphene
from graphene_django.types import DjangoObjectType
from mferp.auth.user.models import MasterConfig

class MasterConfigType(DjangoObjectType):
    class Meta:
        model = MasterConfig



class Query(graphene.ObjectType):
    all_master_configs = graphene.List(MasterConfigType, label=graphene.String(), id=graphene.Int())

    def resolve_all_master_configs(self, info, label=None, id=None):
        if label is not None and id is None:
            # Retrieve all subcategories of the specified label
            return MasterConfig.objects.filter(parent__label=label)
        elif id is not None and label is None:
            # Retrieve all subcategories of the specified id
            return MasterConfig.objects.filter(parent_id=id)
        else:
            # Retrieve all categories (where parent is None)
            return MasterConfig.objects.filter(parent__isnull=True)

schema = graphene.Schema(query=Query)
