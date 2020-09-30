from django.urls import path
from . import views

urlpatterns = [
    path('', views.acasa, name='acasa'),
    path('categoria/<slug:slug_categorie>', views.acasa, name = 'produseDupaCategorie'),
    path('categoria/<slug:slug_categorie>/<slug:slug_produs>', views.paginaProdus, name='detaliiProdus'),
    path('cos/', views.detalii_cos, name='detalii_cos'),
    path('cos/adauga/<int:id_produs>', views.adauga_cos, name='adauga_cos'),
    path('cos/elimina/<int:id_produs>', views.elimina_produs, name='elimina_produs'),
    path('cos/sterge/<int:id_produs>', views.sterge_produs, name='sterge_produs'),
    path('va_multumim/', views.pagina_multumiri, name='pagina_multumiri'),
    path('creare/cont/', views.inregistrareUtilizator, name='inregistrare'),
    path('autentificare/cont/', views.autentificareUtilizator, name='autentificare'),
    path('deconectare/cont/', views.deconectareUtilizator, name='deconectare'),
    path('istoric-comenzi/', views.istoricComenzi, name='istoric'),
    path('comanda/<int:id_comanda>/', views.afiseazaComanda, name='detaliiComanda'),
    path('cautare/', views.cautare, name='cautare'),
    path('contact/', views.contact, name='contact'),
    path('despre_noi/', views.despre_noi, name='despreNoi'),
]
