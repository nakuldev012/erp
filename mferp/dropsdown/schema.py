import graphene
from graphene_django.types import DjangoObjectType
from mferp.mastertableconfig.models import MasterConfig, Organization
from hr.hrconfig.models import HrConfig

class MasterConfigType(DjangoObjectType):
    class Meta:
        model = MasterConfig

class HrConfigType(DjangoObjectType):
    class Meta:
        model = HrConfig

class OrgConfigType(DjangoObjectType):
    class Meta:
        model = Organization


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


    all_hr_configs = graphene.List(HrConfigType, label=graphene.String(), id=graphene.Int())
    
    def resolve_all_hr_configs(self, info, label=None, id=None):
        
        if label is not None and id is None: 
            return HrConfig.objects.filter(parent__label=label)
        elif id is not None and label is None:
            return HrConfig.objects.filter(parent_id=id)
        else:
            return HrConfig.objects.filter(parent__isnull=True)
        

    all_org_configs = graphene.List(OrgConfigType, org_name=graphene.String(), id=graphene.Int())

    def resolve_all_org_configs(self, info, org_name=None, id=None):
        if org_name is not None and id is None: 
            return Organization.objects.filter(parent__org_name=org_name)
        elif id is not None and org_name is None:
            return Organization.objects.filter(parent_id=id)
        else:
            return Organization.objects.filter(parent__isnull=True)
    

schema = graphene.Schema(query=Query)