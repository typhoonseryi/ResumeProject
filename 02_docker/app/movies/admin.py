from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmWork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 1


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name",)
    search_fields = ("full_name", "id")


@admin.register(Filmwork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ("title", "type", "creation_date", "rating")
    list_filter = ("type", "genres")
    search_fields = ("title", "description", "id")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("genres", "persons")
