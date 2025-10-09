from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('adminpage/', admin, name="admin"),
    path('checkout/', checkout, name="checkout"),
    path('createCollab/', createCollab, name="createCollab"),
    path('loginuser/', loginuser, name="loginuser"),
    path('moderator/', moderator, name="moderator"),
    path('passwordChange/', passwordChange, name="passwordChange"),
    path('playlist/<int:idplaylist>', playlist, name="playlist"),
    path('playlistView/', playlistView, name="playlistView"),
    path('pricing/', pricing, name="pricing"),
    path('signup/', signup, name="signup"),
    path('successful_password_change/', successful_password_change, name="successful_password_change"),
    path('successful_payment/', successful_payment, name="successful_payment"),
    path('trending/', trending, name="trending"),
    path('user/', user, name="user"),
    path('collabPage/<int:id>', collabPage, name='collabPage' ),
    path("search/<int:id>", search_spotify, name="search_spotify"),
    path('add_track/<int:id>', add_track, name='add_track'),
    path('add_track/<int:id>/<int:idsong>', remove_track, name='remove_track'),
    path('logoutuser/', logoutuser, name="logoutuser"),
    path('like/<int:id>', like, name='like'),
    path('rate/<int:id>', rate, name='rate'),

    path('cancelrate/<int:id>', cancelrate, name='cancelrate'),

]