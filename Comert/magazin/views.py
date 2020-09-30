from django.shortcuts import render, get_object_or_404, redirect
from .models import Categorie, Produs, Recenzie, Cos, ObiectCos, Comanda, ObiectComanda
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.contrib.auth.models import Group, User
from .formulare import FormularInregistrare, FormularContact
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.mail import EmailMessage


# Create your views here.
def acasa(request, slug_categorie = None):
    pagina_categorie = None
    produse = None
    if slug_categorie != None:
        pagina_categorie = get_object_or_404(Categorie, slug = slug_categorie)
        produse = Produs.objects.filter(categorie = pagina_categorie, disponibil = True)
    else:
        produse = Produs.objects.all().filter(disponibil = True)
    return render(request, 'acasa.html', {'categorie': pagina_categorie, 'produse': produse})


def paginaProdus(request, slug_categorie, slug_produs):
    try:
        produs = Produs.objects.get(categorie__slug = slug_categorie, slug = slug_produs)
    except Exception as e:
        raise e

    if request.method == 'POST' and request.user.is_authenticated and request.POST['mesaj_recenzie'].strip() != '':
        Recenzie.objects.create(produs = produs, utilizator = request.user, mesaj_recenzie = request.POST['mesaj_recenzie'])
    recenzii = Recenzie.objects.filter(produs = produs)

    return render(request, 'produs.html', {'produs': produs, 'recenzii': recenzii})


def cosID(request):
    cos = request.session.session_key
    if not cos:
        cos = request.session.create()
    return cos

def adauga_cos(request, id_produs):
    produs = Produs.objects.get(id=id_produs)
    try:
        cos = Cos.objects.get(id_cos=cosID(request))
    except Cos.DoesNotExist:
        cos = Cos.objects.create(id_cos=cosID(request))
        cos.save()
    try:
        obiect_cos = ObiectCos.objects.get(produs=produs, cos=cos)
        if obiect_cos.cantitate < obiect_cos.produs.stoc:
            obiect_cos.cantitate += 1
        obiect_cos.save()
    except ObiectCos.DoesNotExist:
        obiect_cos = ObiectCos.objects.create(produs=produs, cantitate=1, cos=cos)
        obiect_cos.save()
    return redirect('detalii_cos')

def detalii_cos(request, total=0, contor=0, obiecte_cos=None):
    try:
        cos = Cos.objects.get(id_cos=cosID(request))
        obiecte_cos = ObiectCos.objects.filter(cos=cos, stare_activa=True)
        for obiect_cos in obiecte_cos:
            total +=(obiect_cos.produs.pret * obiect_cos.cantitate)
            contor += obiect_cos.cantitate
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    descriere = 'Comanda noua - Magazin Online'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            numeFacturare = request.POST['stripeBillingName']
            adresaFacturare = request.POST['stripeBillingAddressLine1']
            orasFacturare = request.POST['stripeBillingAddressCity']
            codPostalFacturare = request.POST['stripeBillingAddressZip']
            taraFacturare = request.POST['stripeBillingAddressCountryCode']
            numeLivrare = request.POST['stripeShippingName']
            adresaLivrare = request.POST['stripeShippingAddressLine1']
            orasLivrare = request.POST['stripeShippingAddressCity']
            codPostalLivrare = request.POST['stripeShippingAddressZip']
            taraLivrare = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(email = email, source = token)
            charge = stripe.Charge.create(amount = stripe_total, currency ='ron',
            description = descriere, customer = customer.id)
        # Crearea comenzii
            try:
                detalii_comanda = Comanda.objects.create(
                    token = token,
                    adresa_email = email,
                    numeFacturare = numeFacturare,
                    adresaFacturare = adresaFacturare,
                    orasFacturare = orasFacturare,
                    codPostalFacturare = codPostalFacturare,
                    taraFacturare = taraFacturare,
                    numeLivrare = numeLivrare,
                    adresaLivrare = adresaLivrare,
                    orasLivrare = orasLivrare,
                    codPostalLivrare = codPostalLivrare,
                    taraLivrare = taraLivrare,
                    total = total

                )
                detalii_comanda.save()
                for obiect_comanda in obiecte_cos:
                    obComanda = ObiectComanda.objects.create(
                        produs = obiect_comanda.produs.nume,
                        cantitate = obiect_comanda.cantitate,
                        pret = obiect_comanda.produs.pret,
                        comanda = detalii_comanda
                    )
                    obComanda.save()

                #Reducerea stocului
                    produse = Produs.objects.get(id = obiect_comanda.produs.id)
                    produse.stoc = int(obiect_comanda.produs.stoc - obiect_comanda.cantitate)
                    produse.save()
                    obiect_comanda.delete()

                    print('Comanda a fost plasata cu succes')
                try:
                    trimiteEmail(detalii_comanda.id)
                    print('Email-ul ce contine detaliile comenzii a fost trimis')
                except IOError as e:
                    return e

                return redirect('pagina_multumiri')
            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return False, e

    return render(request, 'cos.html', dict(obiecte_cos = obiecte_cos, total = total, contor = contor, data_key = data_key, stripe_total = stripe_total, descriere = descriere))


def elimina_produs(request, id_produs):
    cos= Cos.objects.get(id_cos=cosID(request))
    produs = get_object_or_404(Produs, id = id_produs)
    obiect_cos = ObiectCos.objects.get(produs = produs, cos = cos)
    if obiect_cos.cantitate > 1:
        obiect_cos.cantitate -= 1
        obiect_cos.save()
    else:
        obiect_cos.delete()

    return redirect('detalii_cos')


def sterge_produs(request, id_produs):
    cos= Cos.objects.get(id_cos=cosID(request))
    produs = get_object_or_404(Produs, id = id_produs)
    obiect_cos = ObiectCos.objects.get(produs = produs, cos = cos)
    obiect_cos.delete()

    return redirect('detalii_cos')


def pagina_multumiri(request):
    return render(request, 'multumiri.html')


def inregistrareUtilizator(request):
    if not request.method == 'POST':
        formular = FormularInregistrare()
        formular.fields['first_name'].label = "Prenume"
        formular.fields['last_name'].label = "Nume"
        formular.fields['username'].label = "Nume de utilizator"
        formular.fields['username'].help_text = ""
        formular.fields['password1'].label = "Parola"
        formular.fields['password1'].help_text = ""
        formular.fields['password2'].label = "Confirmarea parolei"
        formular.fields['password2'].help_text = ""
    else:
        formular = FormularInregistrare(request.POST)
        if formular.is_valid():
            formular.save()
            username = formular.cleaned_data.get('username')
            inreg_util = User.objects.get(username=username)
            grup_client = Group.objects.get(name='Client')
            grup_client.user_set.add(inreg_util)

    return render(request, 'inregistrare.html', {'formular': formular})


def autentificareUtilizator(request):
    if not request.method == 'POST':
        formular = AuthenticationForm()
    else:
        formular = AuthenticationForm(data = request.POST)
        if formular.is_valid():
            nume_utilizator = request.POST['username']
            parola = request.POST['password']
            utilizator = authenticate(username = nume_utilizator, password = parola)
            if utilizator is not None:
                login(request, utilizator)
                return redirect('acasa')
            else:
                return redirect('inregistrare')
    return render(request, 'autentificare.html', {'formular': formular})


def deconectareUtilizator(request):
    logout(request)
    return redirect('autentificare')

@login_required(redirect_field_name = 'n', login_url = 'autentificare')
def istoricComenzi(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        detalii_comanda = Comanda.objects.filter(adresa_email = email)

    return render(request, 'listaComenzi.html', {'detalii_comanda': detalii_comanda})


@login_required(redirect_field_name = 'n', login_url = 'autentificare')
def afiseazaComanda(request, id_comanda):
    if request.user.is_authenticated:
        email = str(request.user.email)
        comanda = Comanda.objects.get(id = id_comanda, adresa_email = email)
        obiecte_comanda = ObiectComanda.objects.filter(comanda = comanda)

    return render(request, 'detaliiComanda.html', {'comanda': comanda, 'obiecte_comanda': obiecte_comanda})


def cautare(request):
    produse = Produs.objects.filter(nume__contains=request.GET['nume_produs'])
    return render(request, 'acasa.html', {'produse': produse})



def trimiteEmail(id_comanda):
    comanda_plasata = Comanda.objects.get(id = id_comanda)
    obiecte_comanda = ObiectComanda.objects.filter(comanda = comanda_plasata)

    try:
        subiect = "Magazin Online - Comanda cu numarul #{}".format(comanda_plasata.id)
        catre = ['{}'.format(comanda_plasata.adresa_email)]
        email = "comenzi@testmagazinonline.site"
        informatii_comanda = {
            'comanda_plasata': comanda_plasata,
            'obiecte_comanda': obiecte_comanda
        }
        mesaj = get_template('email.html').render(informatii_comanda)
        msj = EmailMessage(subiect, mesaj, to = catre, from_email = email)
        msj.content_subtype = 'html'
        msj.send()
    except IOError as e:
        return e



def contact(request):
    if not request.method == 'POST':
        formular = FormularContact()
    else:
        formular = FormularContact(request.POST)
        if formular.is_valid():
            subiect = formular.cleaned_data.get('subiect')
            email_expeditor = formular.cleaned_data.get('email_expeditor')
            mesaj = formular.cleaned_data.get('mesaj')
            nume = formular.cleaned_data.get('nume')

            format_mesaj = "{0} a trimis un mesaj:\n\n{1}".format(nume, mesaj)

            msj = EmailMessage(subiect, format_mesaj,
            to = ['comenzi@testmagazinonline.site'], from_email = email_expeditor)
            msj.send()

            return render(request, 'succesContact.html')

    return render(request, 'contact.html', {'formular': formular})

def despre_noi(request):
    return render(request, 'despreNoi.html')
