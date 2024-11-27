from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import serializers
from . import models
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mercadopago
import json
import logging

# Create your views here.

mp = mercadopago.SDK('TEST-7738649660171797-112101-c2e72c52b14daa7e718b601239c69a7f-286475869')

@api_view(['POST'])
def V_usuario(request):
    serializer = serializers.F_usuario(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class V_productos(APIView):
    model = models.Producto

    def get(self, request, *args, **kwargs):
        productos = self.model.objects.all()
        serializer = serializers.F_producto(productos, many=True)
        print('se realizo')
        return Response(serializer.data, status=status.HTTP_200_OK)
    

logger = logging.getLogger(__name__)

@csrf_exempt  # Deshabilita la protección CSRF para este endpoint
def process_payment(request):
    if request.method == "POST":
        try:
            # Obtener los datos del pago del frontend (cargar el JSON del cuerpo de la solicitud)
            payment_data = json.loads(request.body)
            
            # Registrar los datos recibidos para verificar lo que llega
            logger.debug(f"Datos de pago recibidos: {payment_data}")

            total = payment_data.get("transaction_amount")  # El total del pago
            items = payment_data.get("items")  # Los productos en el carrito
            payer_email = payment_data.get("payer", {}).get("email")

            # Validación básica de los datos
            if not total or not items or not payer_email:
                logger.error("Datos inválidos: faltan campos requeridos")
                return JsonResponse({'error': 'Datos de pago inválidos'}, status=400)

            # Preparar los datos de la preferencia de pago para Mercado Pago
            preference_data = {
                "items": [
                    {
                        "title": item["title"],
                        "quantity": item["quantity"],
                        "unit_price": item["unit_price"]
                    }
                    for item in items
                ],
                "payer": {
                    "email": payer_email,
                },
                "transaction_amount": total,
                "description": "Descripción del pedido",
            }

            # Crear la preferencia de pago en Mercado Pago
            preference_response = mp.preference().create(preference_data)

            # Verificar si la respuesta de Mercado Pago es exitosa
            logger.debug(f"Respuesta de Mercado Pago: {preference_response}")

            if preference_response['status'] == 201:
                init_point = preference_response['response']['init_point']
                return JsonResponse({'init_point': init_point})
            else:
                logger.error(f"Error al crear la preferencia de pago. Respuesta: {preference_response}")
                return JsonResponse({'error': 'Error al crear la preferencia de pago'}, status=500)

        except json.JSONDecodeError:
            # Si hay un error al procesar el JSON
            logger.error("Error al parsear los datos JSON")
            return JsonResponse({'error': 'Error al parsear los datos JSON'}, status=400)

        except Exception as e:
            # Cualquier otro error inesperado
            logger.error(f"Error inesperado: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)