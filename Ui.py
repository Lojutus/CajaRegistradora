import tkinter as tk
from tkinter import ttk, messagebox
from main import *
from manejoProductos import *
import json
    
from collections import Counter
class FacturacionUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caja Registradora - Facturación")
        self.geometry("800x600")
        self._create_widgets()
        self.style = ttk.Style(self)
        self.style.configure(
            'Producto.TButton',
            font=(None, 12, 'bold'),    # tamaño de fuente 12pt en negrita
            padding=(10, 8),            # padding interno: 10px horizontal, 8px vertical
            anchor='w'                  # texto alineado a la izquierda
        )

    def _create_widgets(self):
        # Top menu buttons
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_facturacion = ttk.Button(top_frame, text="Facturación", command=lambda: self.mostrar_vista('facturacion'))
        self.btn_productos = ttk.Button(top_frame, text="Productos", command=lambda: self.mostrar_vista('productos'))
        self.btn_rendimiento = ttk.Button(top_frame, text="Rendimiento", command=lambda: self.mostrar_vista('rendimiento'))

        for btn in (self.btn_facturacion, self.btn_productos, self.btn_rendimiento):
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Contenedor principal para vistas
        self.content_container = ttk.Frame(self)
        self.content_container.pack(fill=tk.BOTH, expand=True)

        # Crear vistas
        self.vistas = {
            'facturacion': self._crear_vista_facturacion(),
            'productos': self._crear_vista_productos(),
            'rendimiento': self._crear_vista_rendimiento()
        }

        # Mostrar vista inicial
        self.mostrar_vista('facturacion')

    def mostrar_vista(self, nombre):
        # Ocultar todas las vistas
        for vista in self.vistas.values():
            vista.pack_forget()
        
        if nombre == "rendimiento":
            self.agregar_items_prueba_rendimiento()
        # Mostrar la solicitada
        self.vistas[nombre].pack(fill=tk.BOTH, expand=True)
    def _crear_vista_facturacion(self):
        frame = ttk.Frame(self.content_container)

        # Izquierda: lista de items scrollable
        list_frame = ttk.Frame(frame, borderwidth=1, relief=tk.SOLID)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,2), pady=5 )

        canvas = tk.Canvas(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.items_container = ttk.Frame(canvas)

        self.items_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.items_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Derecha: área de facturación
        billing_frame = ttk.Frame(frame, borderwidth=1, relief=tk.SOLID)
        billing_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2,5), pady=5)

        # Total
        subtotal_frame = ttk.Frame(billing_frame, height=50)
        subtotal_frame.pack(fill=tk.X, pady=(10,5))
        ttk.Label(subtotal_frame, text="TOTAL", font=(None, 16, 'bold')).pack(side=tk.LEFT, padx=10)
        self.lbl_dinero = ttk.Label(subtotal_frame, text="0", font=(None, 16, 'bold'))
        self.lbl_dinero.pack(side=tk.RIGHT, padx=10)

        # Entrada de código
        entry_frame = ttk.Frame(billing_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        ttk.Label(entry_frame, text="Ingresar código:").pack(side=tk.LEFT, padx=10)
        self.code_entry = ttk.Entry(entry_frame)
        self.code_entry.pack(fill=tk.X, padx=10, expand=True)
        self.code_entry.bind("<Return>", self._add_item_placeholder)

        # Botón terminar
        finish_frame = ttk.Frame(billing_frame)
        finish_frame.pack(fill=tk.BOTH, expand=True, pady=(5,10))
        ttk.Button(finish_frame, text="Terminar", command=self.facturar).pack(pady=20)

        return frame

    def _crear_vista_productos(self):
        frame = ttk.Frame(self.content_container)

        # ── Izquierda: lista scrollable de productos ─────────────────────────
        left_frame = ttk.Frame(frame, borderwidth=1, relief=tk.SOLID)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,2), pady=5)

        canvas = tk.Canvas(left_frame)
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.productos_container = ttk.Frame(canvas)

        self.productos_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.productos_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ── Derecha: formulario de producto (nuevo/editar) ──────────────────
        right_frame = ttk.Frame(frame, borderwidth=1, relief=tk.SOLID)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2,5), pady=5)

        # Título de sección más grande
        self.btn_producto_titulo = ttk.Button(
            right_frame,
            text="Nuevo producto",
            style="TButton",
            compound=tk.CENTER,
            padding=10,
            command=lambda: self.reiniciar_formulario_producto()
        )
        
        self.btn_producto_titulo.pack(pady=(15, 10))
        # Título de sección
        self.lbl_producto_titulo = ttk.Label(
            right_frame,
            text="Informacion del producto",
            font=(None, 14, 'bold')
        )
        self.lbl_producto_titulo.pack(pady=(10, 5))
        # ── Formulario de producto dentro de un Labelframe ────────────────────
        lf = ttk.Labelframe(right_frame, text="Datos del producto", padding=12)
        lf.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        form_frame = ttk.Frame(lf)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar separación entre filas/columnas
        for r in range(3):
            form_frame.rowconfigure(r, weight=1, pad=8)
        form_frame.columnconfigure(1, weight=1, pad=12)
        form_frame.columnconfigure(3, weight=1, pad=12)

        # Definir estilos locales
        lbl_kw = dict(font=(None, 12))
        entry_kw = dict(font=(None, 12))

        # Fila 0: Precio de compra / Precio de fábrica
        ttk.Label(form_frame, text="Precio de venta:", **lbl_kw)\
            .grid(row=0, column=0, sticky="w", padx=(0,10), pady=6)
        self.label_precio_compra = ttk.Label(form_frame, text="Precio de venta", **lbl_kw)
        self.label_precio_compra.grid(row=0, column=1, sticky="ew", padx=(0,20), pady=6, ipady=4)
        

        ttk.Label(form_frame, text="Precio de fábrica:", **lbl_kw)\
            .grid(row=0, column=2, sticky="w", padx=(0,10), pady=6)
        self.entry_precio_fabrica = ttk.Entry(form_frame, **entry_kw)
        self.entry_precio_fabrica.grid(row=0, column=3, sticky="ew", pady=6, ipady=4)

        # Fila 1: Código / Ganancia
        ttk.Label(form_frame, text="Código:", **lbl_kw)\
            .grid(row=1, column=0, sticky="w", padx=(0,10), pady=6)
        self.entry_codigo_prod = ttk.Entry(form_frame, **entry_kw)
        self.entry_codigo_prod.grid(row=1, column=1, sticky="ew", padx=(0,20), pady=6, ipady=4)

        ttk.Label(form_frame, text="Ganancia:", **lbl_kw)\
            .grid(row=1, column=2, sticky="w", padx=(0,10), pady=6)
        self.entry_ganancia_prod = ttk.Entry(form_frame, **entry_kw)
        self.entry_ganancia_prod.grid(row=1, column=3, sticky="ew", pady=6, ipady=4)

        # Fila 2: Nombre
        ttk.Label(form_frame, text="Nombre:", **lbl_kw)\
            .grid(row=2, column=0, sticky="w", padx=(0,10), pady=6)
        self.entry_nombre_prod = ttk.Entry(form_frame, **entry_kw)
        self.entry_nombre_prod.grid(row=2, column=1, columnspan=3, sticky="ew", padx=(0,0), pady=6, ipady=4)

        

        # ── Botones de acción al fondo ───────────────────────────────────────
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)

        self.btn_guardar_producto = ttk.Button(
            btn_frame,
            text="Guardar cambios",
            command=self.guardar_producto
        )
        self.btn_guardar_producto.pack(side=tk.LEFT, fill=tk.X, expand=True, ipadx=10, ipady=5, padx=(0,5))

        self.btn_eliminar_producto = ttk.Button(
            btn_frame,
            text="Eliminar producto",
            command=lambda: self.eliminar_producto_seleccionado()
        )
        self.btn_eliminar_producto.pack(side=tk.RIGHT, fill=tk.X, expand=True, ipadx=10, ipady=5, padx=(5,0))
        self.agregar_items_prueba_productos()
        return frame



    def _crear_vista_rendimiento(self):
        # Marco principal para rendimiento
        rendimiento_frame = ttk.Frame(self.content_container)
        
        # Marco izquierdo con historial de transacciones (scrollable)
        left_frame = ttk.Frame(rendimiento_frame, borderwidth=1, relief=tk.SOLID)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,2), pady=5)

        canvas = tk.Canvas(left_frame)
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.historial_container = ttk.Frame(canvas)

        self.historial_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.historial_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Marco derecho para detalle de transacción
        right_frame = ttk.Frame(rendimiento_frame, borderwidth=1, relief=tk.SOLID)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2,5), pady=5)

        # Ganancia y venta total
        top_info = ttk.Frame(right_frame)
        top_info.pack(fill=tk.X, pady=5)
        self.lbl_ganancia = ttk.Label(top_info, text="Ganancia: $0", font=(None, 12, 'bold'))
        self.lbl_venta_total = ttk.Label(top_info, text="Venta total: $0", font=(None, 12, 'bold'))
        self.lbl_ganancia.pack(side=tk.LEFT, padx=10)
        self.lbl_venta_total.pack(side=tk.RIGHT, padx=10)

        # Fecha
        self.lbl_fecha = ttk.Label(right_frame, text="Fecha: -- / -- / ----", font=(None, 11))
        self.lbl_fecha.pack(pady=(10, 5))

        # Lista de productos vendidos
        ttk.Label(right_frame, text="Productos vendidos:", font=(None, 11, 'bold')).pack(anchor="w", padx=10)
        self.lista_productos_vendidos = tk.Text(right_frame, height=10, wrap="word", state="disabled")
        self.lista_productos_vendidos.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,5))

        # Sección inferior: Fecha inicial, final y botón
        bottom_frame = ttk.Frame(right_frame)
        bottom_frame.pack(fill=tk.X, pady=10)

        ttk.Label(bottom_frame, text="Desde:").pack(side=tk.LEFT, padx=(10, 2))
        self.entry_fecha_inicio = ttk.Entry(bottom_frame, width=12)
        self.entry_fecha_inicio.pack(side=tk.LEFT)

        ttk.Label(bottom_frame, text="Hasta:").pack(side=tk.LEFT, padx=(10, 2))
        self.entry_fecha_fin = ttk.Entry(bottom_frame, width=12)
        self.entry_fecha_fin.pack(side=tk.LEFT)

        resumen_btn = ttk.Button(bottom_frame, text="GENERAR RESUMEN POR FECHA", command=self.generar_resumen_por_fecha)
        resumen_btn.pack(side=tk.RIGHT, padx=10)
        
        
        return rendimiento_frame

    # Funciones de facturación
    def _eliminar_item(self, item):
        dineroActual = float(self.lbl_dinero.cget("text"))
        dineroActual -= item.price
        self.lbl_dinero.config(text=str(dineroActual))
        print(Quitar_Producto(item.codigo))
        item.destroy()
    def _duplicar_item(self, item):
        self.code_entry.delete(0, tk.END)
        self.code_entry.insert(0, item.codigo)
        self.code_entry.focus_set()
        self.code_entry.event_generate("<Return>")
    def _add_item_placeholder(self, event):
        codigo = self.code_entry.get()
        item_frame = ttk.Frame(self.items_container, borderwidth=1, relief=tk.RIDGE, padding=5)
        item_frame.pack(fill=tk.X,  expand=True, pady=2, padx=2)
        producto = buscarInformacionProducto(codigo)
        if producto:
            price = float(producto["Ganancia"]) + float(producto["Precio de compra"])
            ttk.Label(item_frame, text=producto["Nombre"], font=(None, 12, 'bold')).pack(side=tk.LEFT)
            ttk.Label(item_frame, text=str(price), font=(None, 12)).pack(side=tk.RIGHT, padx=(0, 10))
            item_frame.codigo = codigo
            item_frame.price = price
            ttk.Button(item_frame, text="Duplicar", command=lambda: self._duplicar_item(item_frame)).pack(side=tk.RIGHT, padx=5)
            ttk.Button(item_frame, text="Quitar", command=lambda: self._eliminar_item(item_frame)).pack(side=tk.RIGHT)
            dineroActual = float(self.lbl_dinero.cget("text")) + price
            self.lbl_dinero.config(text=str(dineroActual))
            AgregarProducto(codigo)
        else:
            ttk.Label(item_frame, text="No encontrado", font=(None, 12)).pack(side=tk.LEFT)
            ttk.Button(item_frame, text="Quitar", command=lambda: self._eliminar_item(item_frame)).pack(side=tk.RIGHT)
        self.code_entry.delete(0, tk.END)     
    def facturar(self):
        total = Generar_Ticket()
        # Limpiar items
        for widget in self.items_container.winfo_children():
            widget.destroy()
        self.lbl_dinero.config(text="0")
        messagebox.showinfo("Factura generada", f"Total a pagar: ${total}")   
    
    # Funciones de Rendimiento 
    def agregar_items_prueba_rendimiento(self):
        # Eliminar widgets previos
        for widget in self.historial_container.winfo_children():
            widget.destroy()
        try:
            with open("dinero.json", "r", encoding="utf-8") as f:
                transacciones = json.load(f)

            for i in reversed(range(len(transacciones))):
                transaccion = transacciones[i]
                fecha = transaccion.get("Fecha", "Fecha desconocida")
                total_venta = transaccion.get("Total Venta", "0.0")

                btn = ttk.Button(
                    self.historial_container,
                    text=f"TRANSACCIÓN #{i + 1}\n${total_venta} - {fecha.split()[0]}",
                    command=lambda idx=i: self.mostrar_detalle_transaccion(idx),
                )
                btn.pack(fill=tk.X, expand=True, pady=2, padx=5)


        except FileNotFoundError:
            print("El archivo 'dinero.json' no fue encontrado.")
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON.")
    def mostrar_detalle_transaccion(self, idx):
        try:
            with open("dinero.json", "r", encoding="utf-8") as f:
                transacciones = json.load(f)

            # Obtener la transacción elegida
            transaccion = transacciones[idx]

            # Extraer datos básicos
            ganancia = float(transaccion.get("Ganancia Venta", 0))
            total_venta = float(transaccion.get("Total Venta", 0))
            fecha = transaccion.get("Fecha", "-- / -- / ----")
            productos = transaccion.get("Productos", [])

            # 1) Actualizar labels
            self.lbl_ganancia.config(text=f"Ganancia: ${ganancia:.2f}")
            self.lbl_venta_total.config(text=f"Venta total: ${total_venta:.2f}")
            self.lbl_fecha.config(text=f"Fecha: {fecha}")

            # 2) Contar cuántas veces aparece cada producto
            nombres = [p["Nombre Producto"] for p in productos]
            counter = Counter(nombres)

            # 3) Limpiar y rellenar el Text widget
            self.lista_productos_vendidos.config(state="normal")
            self.lista_productos_vendidos.delete("1.0", tk.END)

            self.lista_productos_vendidos.insert(
                tk.END,
                f"Total de productos vendidos: {len(productos)}\n\n"
            )
            self.lista_productos_vendidos.insert(tk.END, "Detalle:\n")
            for nombre, cant in counter.items():
                self.lista_productos_vendidos.insert(
                    tk.END,
                    f"  • {nombre}: {cant} unidad(es)\n"
                )

            self.lista_productos_vendidos.config(state="disabled")

        except FileNotFoundError:
            print("El archivo 'dinero.json' no fue encontrado.")
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON.")
        except IndexError:
            print(f"No existe la transacción con índice {idx}.")
    def generar_resumen_por_fecha(self):

        # 1) Leer fechas de los Entry
        inicio = self.entry_fecha_inicio.get().strip()
        fin    = self.entry_fecha_fin.get().strip()

        # 2) Llamar a la función de análisis
        resumen = analizar_ventas_por_fecha(inicio, fin)

        # 3) Si no hay datos, avisar al usuario
        if not resumen:
            messagebox.showwarning(
                "Resumen vacío",
                "No se encontraron ventas en ese rango de fechas.\n"
                "Verifica el formato YYYY-MM-DD e inténtalo de nuevo."
            )
            return

        # 4) Agregar todos los totales y productos en un solo “resumen global”
        total_ganancias = 0.0
        total_ventas_netas = 0.0
        contador_prod = Counter()

        for fecha, datos in resumen.items():
            total_ganancias    += float(datos.get("ganancias_totales", 0))
            total_ventas_netas += float(datos.get("ventas_netas_totales", 0))

            # datos["cantidad_por_producto"] es un dict {nombre: cantidad}
            for nombre, cant in datos.get("cantidad_por_producto", {}).items():
                contador_prod[nombre] += int(cant)

        # 5) Actualizar los Labels de la derecha
        self.lbl_ganancia.config(text=f"Ganancia: ${total_ganancias:.2f}")
        self.lbl_venta_total.config(text=f"Venta total: ${total_ventas_netas:.2f}")
        self.lbl_fecha.config(text=f"Resumen {inicio} → {fin}")

        # 6) Mostrar el detalle de productos en el Text
        self.lista_productos_vendidos.config(state="normal")
        self.lista_productos_vendidos.delete("1.0", tk.END)

        total_items = sum(contador_prod.values())
        self.lista_productos_vendidos.insert(
            tk.END,
            f"Total de productos vendidos: {total_items}\n\n"
        )
        self.lista_productos_vendidos.insert(tk.END, "Desglose por producto:\n")
        for nombre, cant in contador_prod.items():
            self.lista_productos_vendidos.insert(
                tk.END,
                f"  • {nombre}: {cant} unidad(es)\n"
            )

        self.lista_productos_vendidos.config(state="disabled")
    
    #Funciones de productos
    def agregar_items_prueba_productos(self):
        # 1) Limpiar botones previos
        for widget in self.productos_container.winfo_children():
            widget.destroy()

        # 2) Cargar lista de productos desde JSON
        try:
            with open("productos.json", "r", encoding="utf-8") as f:
                productos = json.load(f)
        except FileNotFoundError:
            print("El archivo 'productos.json' no fue encontrado.")
            return
        except json.JSONDecodeError:
            print("Error al parsear 'productos.json'.")
            return

        # 3) Crear un botón por producto
        for i, prod in enumerate(productos):
            codigo = prod.get("Codigo", "—")
            nombre = prod.get("Nombre", "Sin nombre")
            nombre = nombre.upper()
            btn = ttk.Button(
                self.productos_container,
                text=f"{nombre}   (Código: {codigo})",
                style='Producto.TButton',
                command=lambda idx=i: self.mostrar_detalle_producto(idx)
            )
            # Empacado más “espacioso”
            btn.pack(
                fill=tk.X,
                expand=True,
                padx=10,   # más espacio a los lados
                pady=6,    # separación vertical
                ipady=4    # padding extra interior vertical
            )
    def mostrar_detalle_producto(self, idx):
        try:
            # 1) Leer JSON de productos
            with open("productos.json", "r", encoding="utf-8") as f:
                productos = json.load(f)

            prod = productos[idx]

            # 2) Actualizar título de la sección
            nombre = prod.get("Nombre", "Sin nombre")
            self.lbl_producto_titulo.config(text=f"Editar producto: {nombre}")

            # 3) Rellenar campos
            # Precio de compra
            texto = float(prod.get("Precio de compra", 0)) + float(prod.get("Ganancia", 0))
            self.label_precio_compra.config(text=str(texto))

            # Precio de fábrica
            self.entry_precio_fabrica.delete(0, tk.END)
            self.entry_precio_fabrica.insert(0, prod.get("Precio de compra", ""))

            # Código
            self.entry_codigo_prod.delete(0, tk.END)
            self.entry_codigo_prod.insert(0, prod.get("Codigo", ""))

            # Ganancia
            self.entry_ganancia_prod.delete(0, tk.END)
            self.entry_ganancia_prod.insert(0, prod.get("Ganancia", ""))

            # Nombre
            self.entry_nombre_prod.delete(0, tk.END)
            self.entry_nombre_prod.insert(0, prod.get("Nombre", ""))

            # Guardar el índice actual para usarlo en la función de guardado/eliminación
            self.producto_actual_idx = idx

        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'productos.json'.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo 'productos.json' está corrupto.")
        except IndexError:
            messagebox.showerror("Error", f"No existe un producto con índice {idx}.")
    def guardar_producto(self):
        
        try:
            # Obtener datos desde los cuadros de entrada
            
            precioF = self.entry_precio_fabrica.get().strip()
            codigo = self.entry_codigo_prod.get().strip()
            ganancia = self.entry_ganancia_prod.get().strip()
            nombre = self.entry_nombre_prod.get().strip()

            # Validación básica
            if not ( precioF and codigo and ganancia and nombre):
                messagebox.showerror("Error", "Todos los campos deben estar llenos.")
                return

            # Validación de tipos numéricos
            try:
                
                precioF = float(precioF)
                ganancia = float(ganancia)
                codigo_int = int(codigo)  # para validar que es un número entero como código
            except ValueError:
                messagebox.showerror("Error de formato", "Precio de compra, precio de fábrica, ganancia y código deben ser numéricos.")
                return

            # Si hay un producto seleccionado anteriormente (modo edición)
            
            if buscarExistenciaProducto(codigo):
                # Si estamos editando un producto actual, permitimos usar el mismo código eliminándolo primero
                if hasattr(self, 'producto_actual_idx') and self.producto_actual_idx is not None:
                    Quitar_Producto(codigo)  # Elimina el producto que tiene ese código antes de sobrescribirlo
                else:
                    # Si no estamos editando (es un producto nuevo), no podemos permitir códigos repetidos
                    messagebox.showerror("Error", f"Ya existe un producto con el código {codigo}. Usa otro.")
                    return

                    
            # Llamar a la función que guarda
            resultado = Agregar_Producto(codigo, precioF, ganancia, nombre)
            print(resultado)
            if resultado:
                messagebox.showinfo("Éxito", "Producto guardado correctamente.")
                self.agregar_items_prueba_productos()  # recargar vista
                #self.reset_formulario()  # opcional: limpiar campos
            else:
                messagebox.showerror("Error", "No se pudo guardar el producto. Verifica los datos.")
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))
    def reiniciar_formulario_producto(self):
        
        # Eliminar selección
        self.producto_actual_idx = None

        # Limpiar entradas
        self.label_precio_compra.config(text="Pendiente por calcular ...")
        self.entry_precio_fabrica.delete(0, tk.END)
        self.entry_codigo_prod.delete(0, tk.END)
        self.entry_ganancia_prod.delete(0, tk.END)
        self.entry_nombre_prod.delete(0, tk.END)

        # Cambiar el título del panel derecho
        if hasattr(self, 'lbl_producto_titulo'):
            self.lbl_producto_titulo.config(text="Agregando nuevo producto")
    def eliminar_producto_seleccionado(self):
        # Verifica si hay un producto seleccionado
        if not hasattr(self, "producto_actual_idx") or self.producto_actual_idx is None:
            messagebox.showwarning("Advertencia", "No hay ningún producto seleccionado para eliminar.")
            return

        # Obtener el producto actual
        try:
            with open("productos.json", "r", encoding="utf-8") as f:
                productos = json.load(f)
            producto = productos[self.producto_actual_idx]
            codigo = producto["Codigo"]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el producto seleccionado.\n{e}")
            return

        # Confirmación del usuario
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el producto con código '{codigo}'?"
        )

        if confirmacion:
            resultado = Quitar_Producto(codigo)
            if resultado:
                messagebox.showinfo("Producto eliminado", f"El producto con código '{codigo}' fue eliminado.")
                self.reiniciar_formulario_producto()  # Limpia el formulario y la selección
                self.agregar_items_prueba_productos() #Organiza los indidces
                
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el producto con código '{codigo}'.")

if __name__ == "__main__":
    app = FacturacionUI()
    app.mainloop()
