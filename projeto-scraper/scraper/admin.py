from django.contrib import admin
from .models import Category, Store, URL, Product, History


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Admin interface for managing stores."""
    list_display = ('id', 'description')  # Mostra o ID e a descrição da loja
    search_fields = ('description',)  # Permite busca pela descrição


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    """Admin interface for managing URLs."""
    list_display = ('id', 'store', 'url', 'created_at')  # Mostra informações principais da URL
    list_filter = ('store', 'created_at')  # Filtro por loja e data de criação
    search_fields = ('url',)  # Permite busca pela URL


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for managing products."""
    readonly_fields = ('id', 'description', 'store')  # Campos somente leitura
    list_display = ('id', 'sku', 'description', 'store', 'get_category')  # Adiciona categoria na lista
    list_filter = ('store', 'category')  # Filtros por loja e categoria
    search_fields = ('description', 'sku')  # Busca por descrição e SKU

    def get_category(self, obj):
        """Exibe a categoria associada ao produto."""
        return obj.category.name if obj.category else "Sem categoria"
    get_category.short_description = 'Category'  # Nome da coluna no admin


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    """Admin interface para o histórico de preços."""
    readonly_fields = ('product', 'at', 'default_price', 'offer_price', 'offer')  # Campos somente leitura
    list_display = ('product', 'default_price', 'offer_price', 'offer', 'at')  # Lista os principais campos
    list_filter = ('product__description', 'offer', 'at')  # Filtros por descrição do produto, oferta e data
    search_fields = ('product__description',)  # Busca pela descrição do produto


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface para gerenciar categorias."""
    list_display = ('id', 'name')  # Exibe ID e nome da categoria
    search_fields = ('name',)  # Permite busca pelo nome da categoria
