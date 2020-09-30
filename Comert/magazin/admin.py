from django.contrib import admin
from .models import Categorie, Produs, Comanda, ObiectComanda, Recenzie

class AdminCategorie(admin.ModelAdmin):
    list_display = ['nume', 'slug']
    prepopulated_fields = {'slug': ('nume',)}


admin.site.register(Categorie, AdminCategorie )


class AdminProdus(admin.ModelAdmin):
    list_display = ['nume', 'pret', 'disponibil', 'stoc', 'creat', 'updatat']
    list_editable = ['pret', 'disponibil', 'stoc']
    prepopulated_fields = {'slug': ('nume',)}
    list_per_page = 10

admin.site.register(Produs, AdminProdus)


class AdminObiectComanda(admin.TabularInline):
    model = ObiectComanda
    fieldsets = [
                ('Produs', {'fields': ['produs'],}),
                ('Cantitate', {'fields': ['cantitate'],}),
                ('Pret', {'fields': ['pret'],}),
                ]
    readonly_fields = ['produs', 'cantitate', 'pret']
    max_num=0


@admin.register(Comanda)
class AdminComanda(admin.ModelAdmin):
    list_display = ['id', 'numeFacturare', 'adresa_email', 'creata']
    list_display_links = ('id', 'numeFacturare')
    search_fields = ['id', 'numeFacturare', 'adresa_email']
    readonly_fields = ['id', 'token', 'total', 'adresa_email', 'creata',
                       'numeFacturare', 'adresaFacturare', 'orasFacturare', 'codPostalFacturare',
                       'taraFacturare', 'numeLivrare', 'adresaLivrare', 'orasLivrare',
                       'codPostalLivrare', 'taraLivrare']

    fieldsets = [
        ('INFORMATII COMANDA', {'fields': ['id', 'token', 'total', 'creata']}),
        ('INFORMATII ADRESA FACTURARE', {'fields': ['numeFacturare', 'adresaFacturare',
                                            'orasFacturare', 'codPostalFacturare', 'taraFacturare', 'adresa_email']}),
        ('INFORMATII ADRESA LIVRARE', {'fields': ['numeLivrare', 'adresaLivrare',
                                             'orasLivrare', 'codPostalLivrare', 'taraLivrare']}),
    ]

    inlines = [
        AdminObiectComanda,
    ]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False


admin.site.register(Recenzie)
