from datetime import date, timedelta
from django.http import StreamingHttpResponse
from .services import open_file
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.base import View
from django.urls import reverse
from rest_framework import permissions
from .models import Movie, Category, Actor, Genre, Rating, Reviews, Paket, UserProfile
from .forms import ReviewForm, RatingForm, AddUserForm, SaveBuyForm
from .mixins import ProfileMixin


def get_video(request,pk:int):
    _video=get_object_or_404(Movie,id=pk)
    return render (request, 'movies/movie_detail.html', {'video':_video})


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").distinct()


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 3

class PaketsView(ProfileMixin, View):

    """Список пакетов"""

    def get(self,request):
        pakets = Paket.objects.all()
        context = {'pr': pakets}
        return render(request, 'movies/email.html',context)

class About(View):
    def get(self, request):
        return render(request, 'movies/about.html')

    """покупка подписки"""
def order(request, pk):
        # print(id)
        form=SaveBuyForm (request.POST or None)
        paket = Paket.objects.get(id=pk)
        return render(request, 'movies/order.html', {"paket":paket, "form":form})

def saveorder(request):
    model= UserProfile
    model.podpiska=True
    return render(request, 'movies/paymentsuccess.html', )

class SavePay(UpdateView):
    model = UserProfile
    form_class = AddUserForm
    tamplate_name="movies/userprofile_form.html"

    def get_success_url(self):
        return reverse ('index')

class SaveBuy (ProfileMixin,View):

    def post(self, request, pk):
        paket = Paket.objects.get(id=pk)
        m = paket.months
        startdate = date.today()
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.podpiska = True
        userprofile.DateSubDie = str(startdate + timedelta(days=30*m) )
        # form.userprofile = userprofile
        userprofile.save()

        return render(request, 'movies/paymentsuccess.html')


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 3

    def get_queryset(self):
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist("year")) |
                                        Q(geners__in=self.request.GET.getlist("genre"))).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context



class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

























class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


