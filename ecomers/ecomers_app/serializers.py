from rest_framework import serializers
from . import models

class F_usuario(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = '__all__'

class F_producto(serializers.ModelSerializer):
    class Meta:
        model = models.Producto
        fields = '__all__'