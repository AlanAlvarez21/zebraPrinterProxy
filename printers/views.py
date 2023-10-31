import requests
from rest_framework.views import APIView
from rest_framework.response import Response

class PrintersAPIView(APIView):
    def post(self, request):
        # Generar el código ZPL
        zpl_code = """
        ^XA
        ^FO50,50^A0N,50,50^FDHola^FS
        ^XZ
        """

        # Definir la URL de la API de Zebra y los encabezados
        url = 'https://api.zebra.com/v2/devices/printers/send'
        headers = {
            'accept': 'text/plain',
            'apikey': '31mA0UIAbKTGUMXm21ktVFAAf3emWyEQ',
            'tenant': '490b6deb9f9691080a640daada7d91e9',
        }

        # Crear un archivo temporal con el código ZPL
        with open('temp.zpl', 'w') as zpl_file:
            zpl_file.write(zpl_code)

        # Enviar el archivo ZPL a la API de Zebra
        files = {
            'sn': (None, 'D8N230701799'),
            'zpl_file': ('temp.zpl', open('temp.zpl', 'rb'), 'application/octet-stream')
        }

        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            return Response({'message': 'Archivo ZPL enviado con éxito'})
        else:
            return Response({'message': 'Error al enviar el archivo ZPL. Código de respuesta:', 'status_code': response.status_code})
