from django.contrib import admin
from apps.product.models import Category, Product, Images, Comment, Banner, Size, Color, Variants, Category_Product_Detail, ProductAdvancedSearch, PhoneType, InternaMemory, AmountRAM, BatteryPerformance, ScreenSize, PhoneDesign, CameraFeature, SpecialFeatures, CompareProduct
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails



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



@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','image_thumbnail']


#Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status','image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline, ProductVariantsInline]
    prepopulated_fields = {'slug': ('title',)}




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


class BannerAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'banner']


class ColorAdmin(admin.ModelAdmin):
    list_display= ['name', 'code', 'color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product', 'color', 'size', 'price', 'quantity', 'image_tag']


class PhoneTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


class InternaMemoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class AmountRAMAdmin(admin.ModelAdmin):
    list_display = ['name']


class BatteryPerformanceAdmin(admin.ModelAdmin):
    list_display = ['name']


class ScreenSizeAdmin(admin.ModelAdmin):
    list_display = ['name']


class PhoneDesignAdmin(admin.ModelAdmin):
    list_display = ['name']


class CameraFeatureAdmin(admin.ModelAdmin):
    list_display = ['name']


class SpecialFeaturesAdmin(admin.ModelAdmin):
    list_display = ['name']


class ProductAdvancedSearchAdmin(admin.ModelAdmin):
	list_display = ['product']


class CompareProductAdmin(admin.ModelAdmin):
    list_display = ['ip', 'title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Category_Product_Detail, Category_Product_DetailAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(ProductAdvancedSearch, ProductAdvancedSearchAdmin)
admin.site.register(PhoneType, PhoneTypeAdmin)
admin.site.register(InternaMemory, InternaMemoryAdmin)
admin.site.register(AmountRAM, AmountRAMAdmin)
admin.site.register(BatteryPerformance, BatteryPerformanceAdmin)
admin.site.register(ScreenSize, ScreenSizeAdmin)
admin.site.register(PhoneDesign, PhoneDesignAdmin)
admin.site.register(CameraFeature, CameraFeatureAdmin)
admin.site.register(SpecialFeatures, SpecialFeaturesAdmin)
admin.site.register(CompareProduct, CompareProductAdmin)

