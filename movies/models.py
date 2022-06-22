
from django.db import models
from datetime import date
from django.core.validators import FileExtensionValidator
from django.urls import reverse

from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/users', default="static/images/user.png", null=False, blank=False,verbose_name='Изображение')
    podpiska = models.BooleanField("Подписка",default=False)
    DateSubDie = models.DateField("Дата истечения подписки",default=date.today)


    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def date_past(self):
        if(self.user.userprofile.DateSubDie>date.today()):
            return True
        else:
            return False

class Paket (models.Model):
    name= models.CharField("Название пакета",max_length=150)
    price=models.IntegerField("Цена пакета")
    months=models.IntegerField("Количество месяцев")
    pic = models.ImageField(upload_to='images/pakets', null=True, blank=True, verbose_name='Изображение')

    def get_all_pakets(self):
        return Paket.objects.all()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пакет"
        verbose_name_plural = "Пакеты"

class Category (models.Model):
    name = models.CharField("Категория",max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Actor (models.Model):
    name = models.CharField("Имя",max_length=150)
    age = models.PositiveSmallIntegerField("Возраст",default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение",upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Актеры и режиссеры"
        verbose_name_plural="Актеры и режиссеры"

class Genre (models.Model):
    name=models.CharField("Имя",max_length=100)
    description=models.TextField("Описание")
    url=models.SlugField(max_length=160,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Жанр"
        verbose_name_plural="Жанры"

class Movie(models.Model):
    title=models.CharField("Название",max_length=100)
    tagline=models.CharField("Слоган",max_length=100, default='')
    description=models.TextField("Описание",null=True, blank=True)
    poster=models.ImageField("Постер",upload_to="movies/")
    year=models.PositiveSmallIntegerField("Дата выхода",default=2019)
    country=models.CharField("Страна",max_length=30)
    directors=models.ManyToManyField(Actor, verbose_name="режиссер",related_name="film_director")
    actors=models.ManyToManyField(Actor,verbose_name="актер",related_name="film_actor")
    geners=models.ManyToManyField(Genre,verbose_name="жанры")
    world_premiere=models.DateField("Примьера в мире",default=date.today)
    budget=models.PositiveIntegerField("Бюджет",default=0,help_text="указывать сумму в долларах")
    fess_in_usa=models.PositiveIntegerField("Сборы в США",default=0,help_text="указывать сумму в долларах")
    fess_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="указывать сумму в долларах")
    category=models.ForeignKey(Category,verbose_name="Категория",on_delete=models.SET_NULL, null=True)
    file=models.FileField("Фильм",upload_to='video/', null=True, blank=True,
                          validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    url= models.SlugField(max_length=160,unique=True)
    draft=models.BooleanField("Черновик",default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)


    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

class MovieShots (models.Model):
    title=models.CharField("Заголовок",max_length=100)
    description = models.TextField("Описание")
    image= models.ImageField("Изображение",upload_to="movie_shots/")
    movie=models.ForeignKey(Movie,verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return  self.title

    class Meta:
        verbose_name="Кадр из фильма"
        verbose_name_plural="Кадры из фильма"

class Reviews (models.Model):

    email=models.EmailField()
    name=models.CharField("Имя",max_length=100)
    text=models.TextField("Сообщение",max_length=5000)
    parent=models.ForeignKey("self", verbose_name="Родитель",on_delete=models.SET_NULL,blank=True
                             , null=True)
    movie=models.ForeignKey(Movie,verbose_name="фильм",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}-{self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"






















class RatingStar (models.Model):
    value=models.PositiveSmallIntegerField("Значение",default=0)

    def __str__(self):
        return  self.value

    class Meta:
        verbose_name="Звезда рейтинга"
        verbose_name_plural="Звезды рейтинга"


class Rating(models.Model):
    ip=models.CharField("IP адрес",max_length=15)
    star= models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie= models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.star}-{self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
