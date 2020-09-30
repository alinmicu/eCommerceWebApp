from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Categorie(models.Model):
    nume = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    descriere = models.TextField(blank=True)
    imagine = models.ImageField(upload_to='categorie', blank=True)

    class Meta:
        ordering = ('nume',)
        verbose_name = 'categorie'
        verbose_name_plural = 'categorii'

    def get_url(self):
        return reverse('produseDupaCategorie', args=[self.slug])

    def __str__(self):
        return self.nume


class Produs(models.Model):
    nume = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    descriere = models.TextField(blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    imagine = models.ImageField(upload_to='produs', blank=True)
    stoc = models.IntegerField()
    disponibil = models.BooleanField(default=True, verbose_name = 'Disponibilitate')
    creat = models.DateTimeField(auto_now_add=True, verbose_name = 'Data crearii')
    updatat = models.DateTimeField(auto_now=True, verbose_name = 'Data actualizarii')

    class Meta:
        ordering = ('nume',)
        verbose_name = 'produs'
        verbose_name_plural = 'produse'

    def get_url(self):
        return reverse('detaliiProdus', args=[self.categorie.slug, self.slug])

    def __str__(self):
        return self.nume


class Cos(models.Model):
    id_cos = models.CharField(max_length=250, blank=True)
    data_adaugarii = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Cos'
        ordering = ['data_adaugarii']

    def __str__(self):
        return self.id_cos



class ObiectCos(models.Model):
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    cos = models.ForeignKey(Cos, on_delete=models.CASCADE)
    cantitate = models.IntegerField()
    stare_activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'ObiectCos'

    def subtotal(self):
        return self.produs.pret * self.cantitate

    def __str__(self):
        return self.produs



class Recenzie(models.Model):
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    utilizator = models.ForeignKey(User, on_delete=models.CASCADE)
    mesaj_recenzie = models.CharField(max_length=600)

    class Meta:
        verbose_name = 'Recenzie'
        verbose_name_plural = 'Recenzii'

    def __str__(self):
        return self.mesaj_recenzie



class Comanda(models.Model):
    token = models.CharField(max_length = 250, blank = True)
    total = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = 'Total comanda')
    adresa_email = models.EmailField(max_length = 250, blank = True, verbose_name = 'Adresa de email')
    numeFacturare = models.CharField(max_length = 250, blank = True, verbose_name = 'Nume facturare')
    adresaFacturare = models.CharField(max_length = 250, blank = True, verbose_name = 'Adresa facturare')
    orasFacturare = models.CharField(max_length = 250, blank = True, verbose_name = 'Oras facturare')
    codPostalFacturare = models.CharField(max_length = 250, blank = True, verbose_name = 'Cod postal facturare')
    taraFacturare = models.CharField(max_length=250, blank=True, verbose_name = 'Tara facturare')
    numeLivrare = models.CharField(max_length = 250, blank = True, verbose_name = 'Nume livrare')
    adresaLivrare = models.CharField(max_length = 250, blank = True, verbose_name = 'Adresa livrare')
    orasLivrare = models.CharField(max_length = 250, blank = True, verbose_name = 'Oras livrare')
    codPostalLivrare = models.CharField(max_length = 250, blank = True, verbose_name = 'Cod postal livrare')
    taraLivrare = models.CharField(max_length = 250, blank = True, verbose_name = 'Tara livrare')
    creata = models.DateTimeField(auto_now_add=True, verbose_name = 'Data crearii')


    class Meta:
        ordering = ['-creata']
        db_table = 'Comanda'
        verbose_name = 'Comanda'
        verbose_name_plural = 'Comenzi'

    def __str__(self):
        return str(self.id)



class ObiectComanda(models.Model):
    produs = models.CharField(max_length = 250)
    cantitate = models.IntegerField()
    pret = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = 'Pret:')
    comanda = models.ForeignKey(Comanda, on_delete = models.CASCADE)

    class Meta:
        db_table = 'ObiectComanda'

    def sub_total(self):
        return self.cantitate * self.pret

    def __str__(self):
        return self.produs
