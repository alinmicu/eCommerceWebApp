from .models import Categorie, Cos, ObiectCos
from .views import cosID

def linkuri_meniu(request):
    linkuri = Categorie.objects.all()
    return dict(linkuri=linkuri)

def contor (request):
    contor_obiecte = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cos = Cos.objects.filter(id_cos = cosID(request))
            obiecte_cos = ObiectCos.objects.all().filter(cos=cos[:1])
            for obiect_cos in obiecte_cos:
                contor_obiecte += obiect_cos.cantitate
        except Cos.DoesNotExist:
            contor_obiecte = 0

    return dict(contor_obiecte = contor_obiecte)
