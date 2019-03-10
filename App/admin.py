from django.contrib import admin
from .models import Nekretnina, SlikaNekretnine, PostaviPitanje

# Register your models here.
class SlikaNekretnineInline(admin.TabularInline):
    model = SlikaNekretnine
    extra = 0

class NekretninaAdmin(admin.ModelAdmin):
    search_fields = ['id', 'ulica']
    list_filter = ['tip', 'lokacija']
    inlines = [SlikaNekretnineInline,]
    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.slikanekretnine_set.create(slika=afile)

admin.site.register(Nekretnina, NekretninaAdmin)
admin.site.register(SlikaNekretnine)
admin.site.register(PostaviPitanje)