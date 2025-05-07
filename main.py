#Samuel Mejia Chavarriaga / samuel1022007@gmail.com
#Jose David Hurtado / lojutuselmejor@gmail.com
#Oscar Andres Rengifo Bustos / 
Carrito = []  #MATRIZ CARRITO
"""
Cambios necesesarios:
0 : Con el Codigo de varras identificar los productos 
1 : Colocar un json que contenga los productos que alguna vez fueron agregados ( Que contenga  los precios el margen de ganancia y el inventario), un inventario
2 : Colocar un archivo json que contenga el historial de productos vendidos que contenga el total de ventas y su precio acumulado, las ganancias 
3 : Poder restar productos ( no fueron comprados pero si consumidos, es decir se le resta el precio sin la ganancia a la ganancia total)
4 : Poder hacer un recibo que calcule los precios automaticamente y le reste de inventario y le sume a las ganancias y costos ( asi como un recibo )




"""
#FUNCIONES
def Agregar_Producto():
  while (True):
    Producto = []  #PRODUCTO = ARRAY CON 3 VALORES
    Precio = 0
    cantidad = 0

    #Se solicitan los valores de los productos al usuario
    Producto.append(str(input("Ingrese el nombre del producto: ")))

    producto_existe = any(
        Producto == item[0] for item in Carrito
    )  # Devuelve True si el elemento existe en la lista, False de lo contrario.
    if producto_existe == False:
      Precio = float(input("Ingrese el precio del producto: "))
      while (Precio <= 0):  #COMPRUEBA QUE EL PRECIO SEA POSITIVO
        print("El valor del producto no puede ser negativo")
        Precio = float(input("Ingrese el precio del producto: "))

      Producto.append(Precio)
      cantidad = int(input("Ingrese la cantidad del producto: "))
      while (cantidad < 0):
        print("La cantidad del producto no puede ser negativa")
        cantidad = int(input("Ingrese la cantidad del producto: "))
      Producto.append(cantidad)

    else:
      print(
          "El producto ya existe en el carrito , ¿Desea modificar el producto?"
      )
      print("1. Si")

      print("2. No")
      if (int(input()) == 1):
        Cambiar_Producto()
      else:
        print("El producto no se agregara al carrito")
        break

    Carrito.append(
        Producto)  # AÑADIR PRODUCTO A CARRITO (LO CONVIERTE EN UNA MATRIZ)
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


def Quitar_Producto():

  producto_a_eliminar = input("¿Que producto desea quitar?")
  for i, item in enumerate(Carrito):
    if item[
        0] == producto_a_eliminar:  # Compara con el primer valor de la sublista
      Carrito.pop(i)  # Elimina la sublista encontrada
      return True  # Retorna True si se eliminó
  return False  # Retorna False si no se encontró


def Cambiar_Producto(nombre=None):
  if nombre is None:
    nombre = input("Ingrese el nombre del producto a modificar: ").strip()

  for item in Carrito:
    if item[0].lower() == nombre.lower():
      print(f"Modificando el producto '{nombre}'...")

      # Solicita el nuevo precio
      while True:
        try:
          precio = float(input("Ingrese el nuevo precio: "))
          if precio <= 0:
            print("El precio debe ser un número positivo.")
          else:
            break
        except ValueError:
          print("Por favor, ingrese un valor numérico válido.")

      # Solicita la nueva cantidad
      while True:
        try:
          cantidad = int(input("Ingrese la nueva cantidad: "))
          if cantidad < 0:
            print("La cantidad no puede ser negativa.")
          else:
            break
        except ValueError:
          print("Por favor, ingrese un número entero válido.")

      # Actualiza los valores
      item[1] = precio
      item[2] = cantidad

      print("Producto actualizado correctamente.")
      return
  print("El producto no se encontró en el carrito.")


def Ver_Carrito():
  #Funcion para ver el carrito
  if not Carrito:
    print("El carrito esta vacio")
    return

  print("\n🛍️  Productos en el carrito:")
  print("=" * 35)

  total = 0
  for producto in Carrito:
    nombre = producto[0]
    precio = producto[1]
    cantidad = int(producto[2])
    subtotal = precio * cantidad
    total += subtotal
    print(
        f"📌 {nombre:<15} | 💲{precio:>5} x {cantidad:>2} unidades | 🏷️ Subtotal: ${subtotal}"
    )

  print("=" * 35)
  print(f"🧾 Total a pagar: 💰 ${total}")


def Generar_Ticket():
  if not Carrito:
    print("\n🛒 El carrito está vacío. ¡Agrega productos!")
    return

  print("\n" + "=" * 35)
  print("        🛍️  TICKET DE COMPRA       ")
  print("=" * 35)

  total = 0
  cantidad_total = 0

  for producto in Carrito:
    nombre, precio, cantidad = producto
    subtotal = precio * cantidad
    cantidad_total += cantidad
    total += subtotal
    print(
        f"📌 {nombre:<15} | {cantidad:>2} x 💲{precio:>5.2f} | 🏷️ Subtotal: ${subtotal:>7.2f}"
    )

  # Aplicar descuento si hay más de 10 unidades en total
  if cantidad_total > 10:
    descuento = total * 0.10
    total -= descuento
    print("\n🎉 Descuento aplicado: -💰${:.2f} (10% por más de 10 unidades)".
          format(descuento))

  print("=" * 35)
  print(f"🧾 TOTAL A PAGAR: 💰 ${total:.2f}")
  print("=" * 35)


def Salir():
  #Funcion para salir del programa

  Generar_Ticket()
  print("Gracias por usar nuestro servicio")


while True:
  print("""
  =========================
        🛒 MENÚ CARRITO     
  =========================
  1️⃣  Agregar Producto
  2️⃣  Quitar Producto
  3️⃣  Ver Carrito
  4️⃣  Salir
  5️⃣  Cambiar Producto
  =========================
  """)

  opcion = input("Seleccione una opción: ")

  #Menu Principal
  if opcion == "1":
    try: 
      Agregar_Producto()
    except:
      print("Errores en el ingreso de datos, Intente de nuevo")
  elif opcion == "2":
    try: 
      Quitar_Producto()
    except:
      print("Errores en el ingreso de datos, Intente de nuevo")
  elif opcion == "3":
    try: 
      Ver_Carrito()
    except:
      print("Errores en el ingreso de datos, Intente de nuevo")
  elif opcion == "4":
    try:
      Salir()
    except:
      print("Errores en el ingreso de datos, Intente de nuevo")
    break
  elif opcion == "5":
    try:
      Cambiar_Producto()
    except:
      print("Errores en el ingreso de datos, Intente de nuevo")
  else:
    print("Opción inválida, intente de nuevo.")
