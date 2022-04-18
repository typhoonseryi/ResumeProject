import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class FilmType(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv_show")


class PersonRole(models.TextChoices):
    ACTOR = "actor", _("actor")
    DIRECTOR = "director", _("director")
    WRITER = "writer", _("writer")


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Pesons")
        indexes = [
            models.Index(fields=("full_name",), name="person_full_name_idx"),
        ]

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        _("type"), max_length=7, choices=FilmType.choices, default=FilmType.MOVIE
    )
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Filmwork")
        verbose_name_plural = _("Filmworks")
        indexes = [
            models.Index(fields=("title",), name="film_work_title_idx"),
            models.Index(fields=("creation_date",), name="film_work_creation_date_idx"),
            models.Index(fields=("rating",), name="film_work_rating_idx"),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("Genre Filmwork")
        verbose_name_plural = _("Genres Filmwork")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"], name="genre_film_work_idx"
            ),
        ]


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.TextField(
        _("role"), max_length=8, choices=PersonRole.choices, default=PersonRole.ACTOR
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("Person Filmwork")
        verbose_name_plural = _("Persons Filmwork")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"], name="person_film_work_idx"
            ),
        ]
