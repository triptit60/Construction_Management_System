from django.urls import path
from . import views

urlpatterns = [
    path("", views.inventory_dashboard, name="inventory_dashboard"),
    path("materials/", views.inventory_list, name="inventory_list"),
    path("create/", views.inventory_create, name="inventory_create"),
    path("<int:pk>/", views.inventory_detail, name="inventory_detail"),
    path("<int:pk>/edit/", views.inventory_update, name="inventory_update"),
    path("<int:pk>/delete/", views.inventory_delete, name="inventory_delete"),

    #Transaction
    path("transactions/add/",views.transaction_create, name="transaction_create",),
    path("transactions/",views.transaction_list,name="transaction_list",),
    path("item/<int:pk>/",views.inventory_detail,name="inventory_detail",),

    #Supplier
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
]
