from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Flash-Cards'),
    path('add/', views.add_new_subject, name='Add-Subject'),
    path('details/<int:subject_id>', views.subject_details, name='Subjects-Details'),
    path('addcard/<int:subject_id>', views.add_new_card, name='Add-Card'),
    path('practise/<int:subject_id>', views.practise, name="Practise"),
    path('known/<int:subject_id>', views.view_known, name='Known'),
    path('view_card_practise/<int:card_id>/<int:side>', views.view_card_practise, name='View-Card-Practise'),
    path('view_card_known/<int:card_id>/<int:side>', views.view_card_known, name='View-Card-Known'),
    path('edit_card/<int:card_id>', views.edit_card, name="Edit-Card")
]
