from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Usuario Model
# class Usuario(AbstractUser):
#     direccion = models.CharField(max_length=255, blank=True, null=True)

#     def iniciar_sesion(self):
#         # Implementación para iniciar sesión
#         pass

#     def registrarse(self):
#         # Implementación para registrarse
#         pass

#     def actualizar_perfil(self):
#         # Implementación para actualizar el perfil
#         pass

class Usuario(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    contraseña = models.CharField(max_length=8, null=False, blank=False)

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        db_table = 'usuario'
        ordering = ['nombre']


# Producto modelo
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    rutaIMG = models.CharField(max_length=255, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # cantidad = models.IntegerField()
    categoria = models.CharField(max_length=50)

    # def actualizar_stock(self, cantidad_value):
    #     self.cantidad -= cantidad_value
    #     self.save()

    # def agregar_resena(self, usuario, comentario):
    #     return Reseña.objects.create(usuario=usuario, producto=self, comentario=comentario)

    class Meta:
        db_table = 'Producto'
        ordering = ['nombre']

# Carrito Model
class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CarritoProducto')
    estado = models.BooleanField(default=False, null=False, blank=False)

    def agregar_producto(self, producto, cantidad):
        carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=self, producto=producto)
        carrito_producto.cantidad += cantidad
        carrito_producto.save()

    def quitar_producto(self, producto):
        CarritoProducto.objects.filter(carrito=self, producto=producto).delete()

    def calcular_total(self):
        total = sum(item.producto.precio * item.cantidad for item in self.productos.all())
        return total
    
    class Meta:
        db_table = 'Carrito'
        ordering = ['usuario']


# CarritoProducto Model (Intermediary model for Carrito and Producto)
class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'CarritoProducto'
        ordering = ['carrito']


# Pedido Model
class Pedido(models.Model):
    ESTADOS = [
        ('pendiente_pago', 'Pendiente de Pago'),
        ('pagado', 'Pagado'),
        ('preparacion', 'En Preparación'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente_pago')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_envio = models.CharField(max_length=255)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)


    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.save()

    def calcular_total(self):
        self.total = sum(item.producto.precio * item.cantidad for item in self.producto.all())
        self.save()

    class Meta:
        db_table = 'Pedido'
        ordering = ['usuario']


# # Pago Model
# class Pago(models.Model):
#     TIPOS = [
#         ('tarjeta', 'Tarjeta de Crédito/Débito'),
#         ('transferencia', 'Transferencia Bancaria'),
#         ('paypal', 'PayPal'),
#     ]

#     ESTADOS = [
#         ('pendiente', 'Pendiente'),
#         ('completado', 'Completado'),
#         ('rechazado', 'Rechazado'),
#     ]

#     pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
#     tipo = models.CharField(max_length=20, choices=TIPOS)
#     estado = models.CharField(max_length=20, choices=ESTADOS)
#     monto = models.DecimalField(max_digits=10, decimal_places=2)

#     def procesar_pago(self):
#         if self.estado == 'pendiente':
#             # Lógica para procesar el pago
#             self.estado = 'completado'
#             self.save()


# Reseña Model
# class Reseña(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     comentario = models.TextField()
#     fecha = models.DateTimeField(auto_now_add=True)