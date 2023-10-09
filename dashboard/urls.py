from django.urls import path
from .views import *

urlpatterns=[
    path('',home, name='home'),
    path('notes',notes, name='notes'),
    path('delete_notes/<int:pk>',delete_notes,name='delete_notes'),
    path('NotesView/<int:pk>',NotesView.as_view(),name='NotesView'),
    path('homework',homework, name='homework'),
    path('update_homework/<int:pk>',update_homework, name='update_homework'),
    path('delete_homework/<int:pk>',delete_homework, name='delete_homework'),
    path('youtube',youtube, name='youtube'),
    path('todo',todo, name='todo'),
    path('update_todo/<int:pk>',update_todo, name='update_todo'),
    path('delete_todo/<int:pk>',delete_todo, name='delete_todo'),
    path('books',books, name='books'),
    path('dictionary',dictionary, name='dictionary'),
    path('wiki',wiki, name='wiki'),
    path('conversion',conversion, name='conversion'),

    path('profile/notes',notes, name='notes'),
    path('profile/delete_notes/<int:pk>',delete_notes,name='delete_notes'),
    path('profile/NotesView/<int:pk>',NotesView.as_view(),name='NotesView'),
    path('profile/homework',homework, name='homework'),
    path('profile/update_homework/<int:pk>',update_homework, name='update_homework'),
    path('profile/delete_homework/<int:pk>',delete_homework, name='delete_homework'),
    path('profile/youtube',youtube, name='youtube'),
    path('profile/todo',todo, name='todo'),
    path('update_todo/<int:pk>',update_todo, name='update_todo'),
    path('profile/delete_todo/<int:pk>',delete_todo, name='delete_todo'),
    path('profile/books',books, name='books'),
    path('profile/dictionary',dictionary, name='dictionary'),
    path('profile/wiki',wiki, name='wiki'),
    path('profile/conversion',conversion, name='conversion'),

    
]