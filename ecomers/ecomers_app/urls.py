from django.urls import path
from . import views


urlpatterns = [
    path('formulario/', views.V_usuario, name='formulario'),
    path('productos/', views.V_productos.as_view(), name='producto'),
    path('process-payment/', views.process_payment, name='process_payment'),
]