from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>/listing", views.listing, name="listing"),
    path("<int:listing_id>/watch_list", views.watch_list, name="watch_list"),
    path("watchlist", views.watch_list, name="watchlist"),
    path("<int:listing_id>/close", views.close, name="close")
]
