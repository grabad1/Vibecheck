#Maša Cvetanovski 2022/0128
#Nikola Simikić 2022/0281
#Dušan Grabović 2022/0099
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('adminpage/', admin, name="admin"),
    path('checkout/', checkout, name="checkout"),
    path('collabPage/<int:id>', collabPage, name='collabPage'),
    path('createCollab/<int:collabid>', createCollab, name="createCollab"),
    path('loginuser/', loginuser, name="loginuser"),
    path('moderator/', moderator, name="moderator"),
    path('passwordChange/', passwordChange, name="passwordChange"),
    path('pricing/', pricing, name="pricing"),
    path('signup/', signup, name="signup"),
    path('successful_password_change/', successful_password_change, name="successful_password_change"),
    path('successful_payment/', successful_payment, name="successful_payment"),
    path('trending/', trending, name="trending"),
    path('user/', userpage, name="user"),
    path('logoutuser/', logoutuser, name="logoutuser"),
    path("search/<int:id>", search_spotify, name="search_spotify"),
    path('add_track/<int:id>', add_track, name='add_track'),
    path('add_track/<int:id>/<int:idsong>', remove_track, name='remove_track'),
    path('like/<int:id>', like, name='like'),
    path('rate/<int:id>', rate, name='rate'),
    path('cancelrate/<int:id>', cancelrate, name='cancelrate'),
    path('makePlaylist/<int:id>', makePlaylist, name='makePlaylist'),
    path('ajax/friends/', ajax_get_friends, name='ajax_friends'),
    path('ajax/collabs/', ajax_get_collabs, name='ajax_collabs'),
    path('ajax/messages/', ajax_get_messages, name='ajax_messages'),
    path('ajax/participants/<int:collabid>/', ajax_get_participants, name='ajax_participants'),
    path('ajax/mailbox-action/', ajax_mailbox_action, name='ajax_mailbox_action'),
    path('ajax/friends-collab/<int:collabid>/', ajax_friends_collab, name='ajax_friends_collab'),
    path('already_premium/', already_premium, name='already_premium'),
    path('help/', help, name='help'),
    path('viewPlaylist/<int:id>', viewPlaylist, name='viewPlaylist'),
]