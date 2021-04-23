from django.contrib import admin
from apps.product.models import Category, Product, Images, Comment, Category_Product_Detail, Product_Type_Color, Product_Type_Size, ProductBanner
from mptt.admin import DraggableMPTTAdmin


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display_links = ('indented_title',)
    list_display = ('tree_actions','indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    prepopulated_fields = {'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                Product,
                'category',
                'products_count',
                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


class ProductImageInline(admin.TabularInline):
    model = Images
    min_num = 1
    max_num = 20
    extra = 5

class ProductColorInline(admin.TabularInline):
    model = Product_Type_Color


#Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'category','status']   #thể hiện field slug trong model admin
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug':('title',)}
    class Meta:
        model = Product




class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'status', 'create_at']
    list_filter = ['status']
    readonly_fields =('subject','comment','ip','user','product', 'rate')

class Category_Product_DetailAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display_links = ('indented_title',)
    list_display = ('tree_actions','indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    prepopulated_fields = {'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category_Product_Detail.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category_Product_Detail.objects.add_related_count(qs,
                Product,
                'category',
                'products_count',
                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['product', 'title']


class ProductBannerAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'banner']


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Category_Product_Detail, Category_Product_DetailAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images)
admin.site.register(Product_Type_Color, ProductColorAdmin)
admin.site.register(Product_Type_Size)
admin.site.register(ProductBanner, ProductBannerAdmin)
