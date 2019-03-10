from django.db import models

# Create your models here.

class Nekretnina(models.Model):
    TIPOVI = (('Kuća', 'Kuća'), ('Stan', 'Stan'), ('Stambeno poslovni prostor', 'Stambeno poslovni prostor'), ('Plac', 'Plac'), ('Lokal', 'Lokal'), ('Garaža', 'Garaža'))
    LOKACIJE = (
        ('-', '-'),
        ('Bair', 'Bair'),
        ('Bare', 'Bare'),
        ('Donji Šor', 'Donji Šor'),
        ('Preki Šor', 'Preki Šor'),
        ('Živinarnik', 'Živinarnik'),
        ('Trkalište', 'Trkalište'),
        ('Šipurske Livade', 'Šipurske Livade'),
        ('Kasarske Livade', 'Kasarske Livade'),
        ('Južna Karolina', 'Južna Karolina'),
        ('Čavić', 'Čavić'),
        ('Centar', 'Centar'),
        ('Kamenjak', 'Kamenjak'),
        ('Kamičak', 'Kamičak'),
        ('Triangla', 'Triangla'),
        ('Letnjikovac', 'Letnjikovac')
    )
    TIP_GREJANJA = (
        ('-', '-'),
        ('Centralno', 'Centralno'),
        ('Etažno', 'Etažno'),
        ('TA', 'TA'),
        ('Gas', 'Gas'),
        ('Podno', 'Podno')
    )
    STRUKTURE = (
        ('-', '-'),
        ('0.5', '0.5'),
        ('1.0', '1.0'),
        ('1.5', '1.5'),
        ('2.0', '2.0'),
        ('2.5', '2.5'),
        ('3.0', '3.0'),
        ('3.5', '3.5'),
        ('4.0', '4.0'),
        ('4.5', '4.5'),
        ('5.0', '5.0'),
    )
    tip = models.CharField(max_length=100, choices=TIPOVI)
    mesto = models.CharField(max_length=250)
    ulica = models.CharField(max_length=250, null=True, blank=True)
    lokacija = models.CharField(max_length=250, choices=LOKACIJE)
    cena = models.PositiveIntegerField()
    povrsina = models.PositiveIntegerField()
    opis = models.TextField(max_length=1500)
    struktura = models.CharField(max_length=20, choices=STRUKTURE)
    spratnost = models.CharField(max_length=100, null=True, blank=True)
    grejanje = models.CharField(max_length=50, choices=TIP_GREJANJA)
    specijalna_ponuda = models.BooleanField(default=False)
    thumbnail = models.ImageField(blank=True, null=True)
    napomena = models.TextField(max_length=1500, blank=True, null=True)

    def __str__(self):
        return str(self.pk) + ' - ' + self.tip + ' - ' + self.mesto + ' - ' + str(self.ulica)


class SlikaNekretnine(models.Model):
    nekretnina = models.ForeignKey(Nekretnina, default=None, on_delete=models.CASCADE)
    slika = models.ImageField(blank=True, null=True)


class PostaviPitanje(models.Model):
    ime = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    pitanje = models.TextField()

    def __str__(self):
        return str(self.pk) + ' - ' + self.ime + ' - ' + self.email
