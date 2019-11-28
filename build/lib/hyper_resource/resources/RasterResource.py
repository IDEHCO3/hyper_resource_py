from django.contrib.gis.gdal import GDALRaster

from hyper_resource.models import RasterOperationController
from hyper_resource.resources.SpatialResource import SpatialResource
from hyper_resource.utils import CONTENT_TYPE_IMAGE_TIFF

class RasterResource(SpatialResource):
    def __init__(self):
        super(RasterResource, self).__init__()
        self.operation_controller = RasterOperationController()

    def default_file_name(self):
        return self.object_model.model_class_name() + '_' + str(self.object_model.pk) + '.tiff'

    def default_resource_type(self):
        return 'Raster'

    def get_object_model_raster(self, kwargs):
        pass

    def resource_type_content_type_dict(self):
        contypes_dict = super(RasterResource, self).resource_type_content_type_dict()
        contypes_dict.update({
            GDALRaster: [CONTENT_TYPE_IMAGE_TIFF],
        })
        return contypes_dict