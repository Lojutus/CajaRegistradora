import json
import os

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
def Cambiar_Producto(nombre=None):
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
            

def Agregar_Producto():
  while (True):
    Producto = {}  #PRODUCTO = diccionario con 5 valores 
    Precio = 0
    cantidad = 0

    #Se solicitan los valores de los productos al usuario
    Producto["Codigo"] = input("Ingrese el codigo de barras del producto")
    producto_existe = buscarExistenciaProducto(Producto["Codigo"])
     # Devuelve True si el elemento existe en el diccionario, False de lo contrario.
    if producto_existe == False:
        while True:
            try:
                precioC = float(input("Ingrese el precio de compra : "))
                Ganancia = float(input("Ingrese la ganancia ( en pesos): "))
                nombreP = input("Ingrese el nombre ")

                if precioC <= 0 or Ganancia <= 0:
                    print("El precio debe ser un número positivo.")
                else:
                    break
            except ValueError:
                print("Por favor, ingrese un valor numérico válido.")
        Producto["Precio de compra"] = str(precioC)
        Producto["Ganancia"] = str(Ganancia)
        Producto["Nombre"] = str(nombreP)
        print("Item listo para agregar")  
    else:
      print(
          "El producto ya existe en el Inventario , ¿Desea modificar el producto?"
      )
      print("1. Si")

      print("2. No")
      if (int(input()) == 1):
        Cambiar_Producto()
      else:
        print("El producto no se agregara al carrito")
        break
    try:
        with open("productos.json", "r", encoding='utf-8') as archivo:
            productos = json.load(archivo)
            productos.append(Producto)
          # Guardar nuevamente en el archivo
        with open("productos.json", "w", encoding="utf-8") as f:
            json.dump(productos, f, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print("El producto no se agrego al carrito, archivo para guardar  no existe ")
    
    print("Producto agregado")
    print("¿Desea agregar otro producto?")
    print("1. Si")
    print("2. No")
    Opcion = (int(input("Ingrese una opcion: ")))
    if (Opcion == 1):
      Agregar_Producto()
      break
    elif Opcion == 2:
      break
    else:
      print("la opcion ingresada no es válida")
      break

