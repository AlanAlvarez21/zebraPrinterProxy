import requests
from rest_framework.views import APIView
from rest_framework.response import Response

class PrintersAPIView(APIView):
    def post(self, request):

        lote = 'FE-C-311023124-12'
        clave_producto = 'BOPP TRANS 35 /143'
        peso_bruto = '12.01'
        peso_neto = '11.5'
        metros_lineales = '100'
        cliente = 'don luis'
        name = 'CACA'
        longitudName = len(name)
        longitudClave = len(clave_producto)

        def setName():
            if (longitudName > 13):
                return 10
            else:
                return 100

        # Generar el código ZPL utilizando un f-string
        zpl_code = f"""
        ^XA
        ^CI28
        ^MMT
        ^PW400
        ^LL0500
        ^LS0
        ^FO{setName()},20^A0N,30,30^FD{name}^FS
        ^FO10,60^A0N,35,35^FD     {clave_producto}^FS
        ^FO10,100^A0N,30,30^FDPB: {peso_bruto}kg^FS
        ^FO10,135^A0N,30,30^FDPN: {peso_neto}kg ^FS
        ^FO10,165^A0N,30,30^FDML: {metros_lineales}m ^FS
       
        ^FO10,200^BY2,2
        ^BCN,80,Y,N,N
        ^FD{lote}^FS

        ^PQ1,0,1,Y
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
