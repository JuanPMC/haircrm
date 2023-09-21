from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home),
    path('workers',views.workers),
    path('workers_delete',views.workers_delete),
    path('workers_edit', views.worker_edit),
    path('clients',views.clients),
    path('client_delete',views.clients_delete),
    path('clients_edit', views.client_edit),
    path('client_view',views.client_data),
    path('client_view_delete',views.client_data_delete),
    path('schedule',views.schedule),
    path('booking',views.booking),
    path('booking_edit', views.booking_edit)
]
