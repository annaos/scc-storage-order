"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/comment/', views.comment, name='comment'),
    path('new/', views.edit, name='new'),
    path('persons/', views.PersonsView.as_view(), name='persons'),
    path('persons/<int:pk>', views.personadmin, name='persons-admin'),
    path('order/state/<int:pk>', views.order_next_state, name='order-next-state'),
]
