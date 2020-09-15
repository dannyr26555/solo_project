from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    path('register_attendee', views.registerAttendee),
    path('register_organizer', views.registerOrganizer),

    path('login', views.login),

    path('home', views.home),

    path('viewaccount/<int:id>',views.viewaccount),
    path('viewcon/<int:id>', views.viewcon),

    path('vieworg/<int:id>', views.vieworg),
    # path('viewatt/<int:id>', views.viewatt),

    path('create_con', views.create_con),

    path('like/<int:id>', views.like),
    path('unlike/<int:id>', views.unlike),

    path('conlike/<int:id>', views.conlike),
    path('conunlike/<int:id>', views.conunlike),

    path('userlike/<int:id>', views.userlike),
    path('userunlike/<int:id>', views.userunlike),

    path('rsvp/<int:id>', views.rsvp),
    path('unrsvp/<int:id>', views.unrsvp),

    path('conrsvp/<int:id>', views.conrsvp),
    path('conunrsvp/<int:id>', views.conunrsvp),

    path('userrsvp/<int:id>', views.userrsvp),
    path('userunrsvp/<int:id>', views.userunrsvp),

    path('edit_att', views.edit_att),
    path('edit_org', views.edit_org),

    path('delete/<int:id>', views.delete),

    path('logout', views.logout)
]