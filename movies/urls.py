from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    path("", views.MoviesView.as_view()),

    path("", cache_page(60)(views.MoviesView.as_view()), name="index"),
    path("saveorder/<int:pk>/", views.SaveBuy.as_view(), name="update_user_after"),
    path("about/",views.About.as_view(), name='about'),
    path("email/", views.PaketsView.as_view(), name='movies_email'),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("<slug:slug>/", cache_page(60)(views.MovieDetailView.as_view()), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("email/order/<int:pk>/", views.order),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),
    path("stream/<int:pk>/", views.get_streaming_video, name='stream'),
]
