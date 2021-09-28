from django.urls import path
from api.views import order_views as views



urlpatterns = [


    path('',views.getOrders,name='all-orders'),
    path('add/',views.addOrder,name='orders-add'),
    path('myorders/',views.getMyOrders,name='myorders'),
    path('<str:pk>/',views.getOrderById,name='user-order'),
    path('<str:pk>/deliver/',views.updateOrderToDelivered,name='order-deliver'),
    path('<str:pk>/pay/',views.updateOrderToPaid,name='pay'),


]