from django.urls import path

from . import views

urlpatterns = [

	path('dashboard', views.dashboard, name="dashboard"),
	path('active_orders',views.active_orders,name='active_orders'),
	path('update_order/<str:action>/<int:pk>',views.update_order,name='update_order'),
	path('',views.index,name='index'),
	path('products',views.products,name='products'),
	path('update_item/', views.updateItem, name="update_item"),
	path('cart', views.cart, name="cart"),
	path('checkout',views.checkout,name='checkout'),
	path('login',views.login,name='login'),
	path('logout', views.logout, name='logout'),
	path('products/<str:name>',views.products,name='products')
]