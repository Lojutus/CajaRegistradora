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
        ttk.Label(frame, text="Vista de Productos (en construcción)").pack(pady=20)
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
    import json

    def agregar_items_prueba_rendimiento(self):
        # Eliminar widgets previos
        for widget in self.historial_container.winfo_children():
            widget.destroy()
        try:
            with open("dinero.json", "r", encoding="utf-8") as f:
                transacciones = json.load(f)

            for i, transaccion in enumerate(transacciones):
                fecha = transaccion.get("Fecha", "Fecha desconocida")
                total_venta = transaccion.get("Total Venta", "0.0")

                btn = ttk.Button(
                    self.historial_container,
                    text=f"TRANSACCIÓN #{i + 1}\n${total_venta} - {fecha.split()[0]}",
                    command=lambda idx=i: self.mostrar_detalle_transaccion(idx),
                )
                btn.pack(fill=tk.X,expand=True, pady=2, padx=5  )

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

if __name__ == "__main__":
    app = FacturacionUI()
    app.mainloop()
