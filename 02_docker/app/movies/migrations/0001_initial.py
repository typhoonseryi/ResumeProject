import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Filmwork",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(null=True, blank=True, verbose_name="description"),
                ),
                (
                    "creation_date",
                    models.DateField(
                        null=True, blank=True, verbose_name="creation_date"
                    ),
                ),
                (
                    "rating",
                    models.FloatField(
                        null=True,
                        blank=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="rating",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("movie", "movie"), ("tv_show", "tv_show")],
                        default="movie",
                        max_length=7,
                        verbose_name="type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Filmwork",
                "verbose_name_plural": "Filmworks",
                "db_table": 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, unique=True, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(null=True, blank=True, verbose_name="description"),
                ),
            ],
            options={
                "verbose_name": "genre",
                "verbose_name_plural": "genres",
                "db_table": 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name="GenreFilmwork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "film_work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.filmwork",
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.genre"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Genre Filmwork",
                "verbose_name_plural": "Genres Filmwork",
                "db_table": 'content"."genre_film_work',
            },
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="full_name"),
                ),
            ],
            options={
                "verbose_name": "Person",
                "verbose_name_plural": "Pesons",
                "db_table": 'content"."person',
            },
        ),
        migrations.CreateModel(
            name="PersonFilmWork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "role",
                    models.TextField(
                        choices=[
                            ("actor", "actor"),
                            ("director", "director"),
                            ("writer", "writer"),
                        ],
                        default="actor",
                        max_length=8,
                        verbose_name="role",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "film_work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.filmwork",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.person"
                    ),
                ),
            ],
            options={
                "verbose_name": "Person Filmwork",
                "verbose_name_plural": "Persons Filmwork",
                "db_table": 'content"."person_film_work',
            },
        ),
        migrations.AddField(
            model_name="filmwork",
            name="genres",
            field=models.ManyToManyField(
                through="movies.GenreFilmwork", to="movies.Genre"
            ),
        ),
        migrations.AddField(
            model_name="filmwork",
            name="persons",
            field=models.ManyToManyField(
                through="movies.PersonFilmWork", to="movies.Person"
            ),
        ),
        migrations.AddConstraint(
            model_name="personfilmwork",
            constraint=models.UniqueConstraint(
                fields=("film_work", "person", "role"), name="person_film_work_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="genrefilmwork",
            constraint=models.UniqueConstraint(
                fields=("film_work", "genre"), name="genre_film_work_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="filmwork",
            index=models.Index(fields=["title"], name="film_work_title_idx"),
        ),
        migrations.AddIndex(
            model_name="filmwork",
            index=models.Index(
                fields=["creation_date"], name="film_work_creation_date_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="filmwork",
            index=models.Index(fields=["rating"], name="film_work_rating_idx"),
        ),
        migrations.AddIndex(
            model_name="person",
            index=models.Index(fields=["full_name"], name="person_full_name_idx"),
        ),
    ]
