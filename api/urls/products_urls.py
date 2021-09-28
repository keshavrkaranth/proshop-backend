from django.urls import path
from api.views import product_views as views

urlpatterns = [

    path('createProduct/', views.createProduct, name='product-create'),
    path('upload/', views.uploadImage, name='image-upload'),
    path('top/', views.getTopProducts),
    path('', views.getProducts),
    path('<str:pk>/', views.getProduct),
    path('<str:pk>/reviews/', views.createProductReview),
    path('update/<str:pk>/', views.updateProduct),
    path('delete/<str:pk>/', views.deleteProduct),

]
