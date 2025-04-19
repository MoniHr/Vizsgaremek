from import_export import resources

from apps.job_post.models import Category, SubCategory

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'code', 'name', 'icon', 'featured', 'order')
        export_order = ('id', 'code', 'name', 'icon', 'featured', 'order')


class SubCategoryResource(resources.ModelResource):
    class Meta:
        model = SubCategory
        fields = ('id', 'category__name', 'code', 'name')
        export_order = ('id', 'category__name', 'code', 'name')
