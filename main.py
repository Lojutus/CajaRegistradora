
#Jose David Hurtado / lojutuselmejor@gmail.com
from datetime import datetime
from manejoProductos import * 
"""
Cambios necesesarios:
0 : Con el Codigo de varras identificar los productos # Completado (mediadamente , funciona pero no se conecta a ninguna API )
1 : Colocar un json que contenga los productos que alguna vez fueron agregados ( Que contenga  los precios el margen de ganancia y el inventario), un inventario # HECHO
2 : Colocar un archivo json que contenga el historial de productos vendidos que contenga el total de ventas y su precio acumulado, las ganancias #Hecho
3 : Poder restar productos ( no fueron comprados pero si consumidos, es decir se le resta el precio sin la ganancia a la ganancia total) # No es necesario dado que ya no vamos a ahcer el inventario
4 : Poder hacer un recibo que calcule los precios automaticamente y le reste de inventario y le sume a las ganancias y costos ( asi como un recibo ) #hecho
5: Ui, ( quitar productos, Agregar  a la base de datos , ver el historial de ventas , moder modificar la base de datos )



"""

Carrito = [] #Lista con los productos
#FUNCIONES
def conseguirFecha():
  now = datetime.now()
  now_sin_segundos = now.replace(second=0, microsecond=0)
  return now_sin_segundos
 

def AgregarProducto(codigo):
    
    Producto = []  #PRODUCTO = diccionario CON 4 VALORES  
    #Se solicitan los valores de los productos al usuario  
    if(buscarExistenciaProducto(codigo)):
      Producto.append(buscarInformacionProducto(codigo))
      Carrito.append(Producto)  # AÑADIR PRODUCTO A CARRITO (LO CONVIERTE EN UNA MATRIZ)
    




def Quitar_Producto(producto_a_eliminar):
  for i in range(len(Carrito)):
    for j in Carrito[i]: 
      if j["Codigo"] == producto_a_eliminar:  # Compara con el primer valor de la sublista
        Carrito.pop(i)  # Elimina la sublista encontrada
        return True  # Retorna True si se eliminó
  return False  # Retorna False si no se encontró


def Generar_Ticket():
  global Carrito
  total = 0
  gananciaVenta= 0
  try:
      with open("dinero.json", "r", encoding='utf-8') as archivo:
            historialVentas = json.load(archivo)
  except:
      historialVentas = []
  Productos = []
  historial = {}
  for producto in Carrito:
    data = producto[0]
    
    nombre = data["Nombre"]
    precio = float(data["Precio de compra"]) + float(data["Ganancia"])
    ganancia = float(data["Ganancia"])
    subtotal = precio 
    total += subtotal
    gananciaVenta += ganancia

    #GUARDAR EL ITEM EN UN DICCIONARIO QUE QUEDE MAS FACIL MANIPULARLO
    acumuladorProductos = {}
    acumuladorProductos["Nombre Producto"] = str(nombre) 
    acumuladorProductos["Precio de Compra"] = str(data["Precio de compra"])
    acumuladorProductos["Ganancia"] = str(ganancia)
    Productos.append(acumuladorProductos)
  historial["Ganancia Venta"] = str(gananciaVenta)
  historial["Productos"] = Productos
  historial["Total Venta"] = total
  historial["Fecha"] = str(conseguirFecha())
  historialVentas.append(historial)
          
  try:  
        # Guardar nuevamente en el archivo
        with open("dinero.json", "w", encoding="utf-8") as f:
            json.dump(historialVentas, f, indent=4, ensure_ascii=False)
  except FileNotFoundError:
        print("El producto no se agrego al historial, archivo para guardar  no existe ")
  Carrito = []  #MATRIZ CARRITO VACIA
  return total
  
