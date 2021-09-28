from django.urls import path
from api.views import user_views as views



urlpatterns = [

    path('routes/',views.getRoutes),
    path('register/',views.registerUser,name='user-profile'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/',views.getUserProfile,name='user-profile'),
    path('profile/update',views.updateUserProfile,name='user-profile-update'),
    path('',views.getUsers,name='users'),
    path('<str:pk>/',views.getUserById,name='user-byId'),
    path('delete/<str:pk>/',views.deleteUser,name='user-delete'),
    path('update/<str:pk>/',views.updateUser,name='user-update'),


]