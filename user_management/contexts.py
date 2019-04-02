from hyper_resource.contexts import FeatureResourceContext, FeatureCollectionResourceContext, ContextResource

class HyperUserLonginRegister(ContextResource):

    def initalize_context(self, resource_type):
        self.dict_context = {}
        a_context = self.get_subClassOf_term_definition()
        a_context.update(self.get_hydra_term_definition())
        self.dict_context["@context"] = a_context
        self.dict_context["hydra:supportedProperties"] = self.supportedProperties()
        self.dict_context["hydra:supportedOperations"] = []
        #self.dict_context["hydra:representationName"] = self.representationName()
        #self.dict_context["hydra:iriTemplate"] = self.iriTemplates()
        self.dict_context.update(self.get_default_context_superclass())
        self.dict_context.update(self.get_default_resource_type_identification())

'''
class APIResourceDetailContext(ContextResource):
    pass
class APIResourceListContext(ContextResource):
    pass
'''

class HyperUserDetailContext(ContextResource):
    pass
class HyperUserListContext(ContextResource):
    pass

class HyperUserGroupDetailContext(ContextResource):
    pass
class HyperUserGroupListContext(ContextResource):
    pass

class HyperUserRegisterContext(HyperUserLonginRegister):
    pass

class HyperUserLoginContext(HyperUserLonginRegister):
    pass

'''
class HyperUserGroupAPIResourceDetailContext(ContextResource):
    pass
class HyperUserGroupAPIResourceListContext(ContextResource):
    pass

class HyperUserContext(ContextResource):
    pass
'''