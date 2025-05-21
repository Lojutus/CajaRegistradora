import json
import os
from datetime import datetime
def buscarExistenciaProducto(productoE):
    try:
        productoE = str(productoE)
        with open("productos.json", "r", encoding='utf-8') as archivo:
            productos = json.load(archivo)
            
        for producto in productos:
            
            if producto["Codigo"] == productoE:
                
                return True
        return False 
    except FileNotFoundError:
        return False
def buscarInformacionProducto(productoE):
    if buscarExistenciaProducto(productoE):
        try:
            productoE = str(productoE)
            with open("productos.json", "r", encoding='utf-8') as archivo:
                productos = json.load(archivo)
            for producto in productos:
                if producto["Codigo"] == productoE:
                    return producto
        except FileNotFoundError:
                    return False
    else:
        return False
def Cambiar_Producto( nombre = None):
    if nombre is None:
            nombre = input("Ingrese el codigo del producto a modificar: ").strip()
    if buscarExistenciaProducto(nombre):

            with open("productos.json", "r", encoding='utf-8') as archivo:
                productos = json.load(archivo)
            for producto in productos:
                if producto["Codigo"] == nombre:
                    print(f"Modificando el producto '{nombre}'...")
                    # Solicita el nuevo precio
                    while True:
                        try:
                            precioC = float(input("Ingrese el nuevo precio de compra : "))
                            Ganancia = float(input("Ingrese la ganancia ( en pesos): "))
                            nombreP = input("Ingrese el nuevo nombre ")

                            if precioC <= 0 or Ganancia <= 0:
                                print("El precio debe ser un número positivo.")
                            else:
                                break
                        except ValueError:
                            print("Por favor, ingrese un valor numérico válido.")
                producto["Precio de compra"] = str(precioC)
                producto["Ganancia"] = str(Ganancia)
                producto["Nombre"] = str(nombreP) # Esto es lo que posee cada producto ademas de su codigo 



                            
    else:
        print("El producto no existe")
def Agregar_Producto(Codigo,precioC, Ganancia, nombreP):
  
    Producto = {}  #PRODUCTO = diccionario con 5 valores 
    Precio = 0
    cantidad = 0

    #Se solicitan los valores de los productos al usuario
    Producto["Codigo"] = Codigo
    producto_existe = buscarExistenciaProducto(Producto["Codigo"])
     # Devuelve True si el elemento existe en el diccionario, False de lo contrario.
    if producto_existe == False:
        
        Producto["Precio de compra"] = str(precioC)
        Producto["Ganancia"] = str(Ganancia)
        Producto["Nombre"] = str(nombreP)
        print("Item listo para agregar")  
    else:
      return False
    try:
        with open("productos.json", "r", encoding='utf-8') as archivo:
            productos = json.load(archivo)
            productos.append(Producto)
          # Guardar nuevamente en el archivo
        with open("productos.json", "w", encoding="utf-8") as f:
            json.dump(productos, f, indent=4, ensure_ascii=False)
            return True
    except FileNotFoundError:
        print("El producto no se agrego al carrito, archivo para guardar  no existe ")
        return False
    
def Quitar_Producto(producto_a_eliminar):
    try:
        with open("productos.json", "r", encoding='utf-8') as archivo:
            productos = json.load(archivo)
        for i in range(len(productos)):
            if productos[i]["Codigo"] == producto_a_eliminar:
                del productos[i]
                break
        else:
            print("El producto no existe")
            return False
        # Guardar nuevamente en el archivo
        with open("productos.json", "w", encoding="utf-8") as f:
            json.dump(productos, f, indent=4, ensure_ascii=False)
            return True
    except FileNotFoundError:
        print("El producto no se elimino del carrito, archivo para guardar  no existe ")
        return False
    

def analizar_ventas_por_fecha( fecha_inicio_str, fecha_fin_str):
    """
    Analiza los datos de ventas dentro de un rango de fechas específico.

    Args:
        datos_ventas (list): Lista de diccionarios con los datos de las ventas.
        fecha_inicio_str (str): Fecha de inicio para el filtro (formato YYYY-MM-DD).
        fecha_fin_str (str): Fecha de fin para el filtro (formato YYYY-MM-DD).

    Returns:
        dict: Un diccionario con los datos agregados por fecha.
              Ejemplo:
              {
                  "YYYY-MM-DD": {
                      "ganancias_totales": float,
                      "cantidad_productos_vendidos_total": int,
                      "cantidad_por_producto": {
                          "nombre_producto1": int,
                          "nombre_producto2": int
                      },
                      "ventas_netas_totales": float
                  }
              }
    """
    resultados_por_fecha = {}
    try:
        with open("dinero.json", "r", encoding='utf-8') as archivo:
            datos_ventas = json.load(archivo)

    except FileNotFoundError:
        return False
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")
        return {}

    for venta in datos_ventas:
        try:
            fecha_venta_dt = datetime.strptime(venta["Fecha"], "%Y-%m-%d %H:%M:%S")
            fecha_venta_date = fecha_venta_dt.date() # Solo la parte de la fecha para agrupar por día
        except (ValueError, KeyError) as e:
            print(f"Advertencia: Registro omitido debido a error en la fecha o estructura: {venta}. Error: {e}")
            continue

        if fecha_inicio <= fecha_venta_date <= fecha_fin:
            fecha_str = fecha_venta_date.strftime("%Y-%m-%d")

            if fecha_str not in resultados_por_fecha:
                resultados_por_fecha[fecha_str] = {
                    "ganancias_totales": 0.0,
                    "cantidad_productos_vendidos_total": 0,
                    "cantidad_por_producto": {},
                    "ventas_netas_totales": 0.0
                }

            # Acumular Ganancia Venta
            try:
                resultados_por_fecha[fecha_str]["ganancias_totales"] += float(venta.get("Ganancia Venta", 0.0))
            except ValueError:
                print(f"Advertencia: Valor no numérico para 'Ganancia Venta' en el registro con fecha {venta['Fecha']}.")


            # Acumular Total Venta (Ventas Netas)
            try:
                resultados_por_fecha[fecha_str]["ventas_netas_totales"] += float(venta.get("Total Venta", 0.0))
            except ValueError:
                 print(f"Advertencia: Valor no numérico para 'Total Venta' en el registro con fecha {venta['Fecha']}.")


            # Procesar productos
            productos_vendidos = venta.get("Productos", [])
            resultados_por_fecha[fecha_str]["cantidad_productos_vendidos_total"] += len(productos_vendidos)

            for producto in productos_vendidos:
                nombre_producto = producto.get("Nombre Producto")
                if nombre_producto:
                    resultados_por_fecha[fecha_str]["cantidad_por_producto"][nombre_producto] = \
                        resultados_por_fecha[fecha_str]["cantidad_por_producto"].get(nombre_producto, 0) + 1
    
    return resultados_por_fecha
print(Agregar_Producto(123, 100, 20, "Producto A"))