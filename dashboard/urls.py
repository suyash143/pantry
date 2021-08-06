from django.urls import path

from . import views

urlpatterns = [

	path('dashboard', views.dashboard, name="dashboard"),
	path('',views.index,name='index'),
	path('products',views.products,name='products'),
	path('products/<str:name>',views.products,name='products')
]