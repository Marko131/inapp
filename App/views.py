from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Nekretnina, PostaviPitanje
from django.core.mail import EmailMessage

# Create your views here.

def index(request):
    nekretnine = Nekretnina.objects.all()
    specijalna_ponuda = Nekretnina.objects.filter(specijalna_ponuda=True)

    tip = request.GET.get('tip_nekretnine')
    cena_od = request.GET.get('cena_od')
    cena_do = request.GET.get('cena_do')
    povrsina_od = request.GET.get('povrsina_od')
    povrsina_do = request.GET.get('povrsina_do')
    lokacije = request.GET.getlist('lokacija[]')
    grejanje = request.GET.getlist('grejanje[]')
    struktura = request.GET.getlist('struktura[]')

    filter_tip = nekretnine.filter(tip__contains=tip) if tip else  nekretnine
    filter_cena_od = filter_tip.filter(cena__gte=cena_od) if cena_od else filter_tip
    filter_cena_do = filter_cena_od.filter(cena__lte=cena_do) if cena_do else filter_cena_od
    filter_povrsina_od = filter_cena_do.filter(povrsina__gte=povrsina_od) if povrsina_od else filter_cena_do
    filter_povrsina_do = filter_povrsina_od.filter(povrsina__lte=povrsina_do) if povrsina_do else filter_povrsina_od
    filter_lokacija = filter_povrsina_do.filter(lokacija__in=lokacije) if lokacije else filter_povrsina_do
    filter_grejanje = filter_lokacija.filter(grejanje__in=grejanje) if grejanje else filter_lokacija
    filter_struktura = filter_grejanje.filter(struktura__in=struktura) if struktura else filter_grejanje

    filtrirano = filter_struktura

    try:
        sort = request.GET['sort']
        if sort == '0':
            sortirano = filtrirano.order_by('-id')
        elif sort == '1':
            sortirano = filtrirano.order_by('cena')
        elif sort == '2':
            sortirano = filtrirano.order_by('-cena')
        elif sort == '3':
            sortirano = filtrirano.order_by('povrsina')
        elif sort == '4':
            sortirano = filtrirano.order_by('-povrsina')
        else:
            sortirano = filtrirano
    except:
        sortirano = filtrirano

    try:
        page = int(request.GET['page'])
    except:
        page = 1
    print(page)
    paginator = Paginator(list(sortirano), 1)
    lista_nekretnina = paginator.get_page(page)
    stranice = [i+1 for i in range(lista_nekretnina.paginator.num_pages)]
    rezultati = len(sortirano)
    return render(request, 'index.html', {"nekretnine": lista_nekretnina, "stranice": stranice, "broj_rezultata": rezultati, 'specijalna_ponuda': specijalna_ponuda, 'trenutna_stranica':page})


def home(request):
    specijalna_ponuda = Nekretnina.objects.filter(specijalna_ponuda=True)
    nekretnine = Nekretnina.objects.all().order_by('-id')
    lista_nekretnina = list(nekretnine)
    return render(request, 'home.html', {'specijalna_ponuda': specijalna_ponuda, 'nekretnine': lista_nekretnina[:10]})


def about(request):
    specijalna_ponuda = Nekretnina.objects.filter(specijalna_ponuda=True)
    return render(request, 'about.html', {'specijalna_ponuda': specijalna_ponuda})


def location(request):
    specijalna_ponuda = Nekretnina.objects.filter(specijalna_ponuda=True)
    return render(request, 'location.html', {'specijalna_ponuda': specijalna_ponuda})


def contact(request):
    specijalna_ponuda = Nekretnina.objects.filter(specijalna_ponuda=True)
    return render(request, 'contact.html', {'specijalna_ponuda': specijalna_ponuda})


def detail(request, nekretnina_id):
    nekretnina = get_object_or_404(Nekretnina, pk=nekretnina_id)
    specijalna_ponuda = Nekretnina.objects.filter(specijalna_ponuda=True)
    return render(request, 'detail.html', {'nekretnina': nekretnina, 'specijalna_ponuda': specijalna_ponuda})


def postavi_pitanje(request):
    ime = request.POST.get('ime')
    email = request.POST.get('email')
    pitanje = request.POST.get('poruka')

    pp = PostaviPitanje(ime=ime, email=email, pitanje=pitanje)
    pp.save()

    e = EmailMessage('InNekretnine', ime + '\n\n' + email + '\n\n' + pitanje, to=['zivkovic97nemanja@gmail.com'])
    e.send()
    return contact(request)
