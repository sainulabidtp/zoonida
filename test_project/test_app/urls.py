from .import views
from django.urls import path
from .views import shorten_url,redirect_original,view_url,list_urls,edit_url,delete_url
urlpatterns = [
    path('register',views.register, name="register"),
    path('login', views.login, name='login'),
    path('logout', views.logout,name='logout'),
    path('shorten/', shorten_url, name='shorten_url'),
    path('<str:short_code>/', redirect_original, name="redirect_original"),
    path('<str:short_code>/view/', view_url, name="view_url"),
    path('', list_urls, name="list_url"),
    path('<str:short_code>/edit/', edit_url, name="edit_url"),
    path('<str:short_code>/delete/', delete_url, name="delete_url"),

]