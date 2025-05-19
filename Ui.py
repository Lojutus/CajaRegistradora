from main import *
from manejoProductos import * 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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

        self.btn_facturacion = ttk.Button(top_frame, text="Facturación")
        self.btn_rendimiento = ttk.Button(top_frame, text="Rendimiento")
        self.btn_productos = ttk.Button(top_frame, text="Productos")

        self.btn_facturacion.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.btn_rendimiento.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.btn_productos.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Main content
        content_frame = ttk.Frame(self)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left: scrollable list of items
        list_frame = ttk.Frame(content_frame, borderwidth=1, relief=tk.SOLID)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,2), pady=5)

        canvas = tk.Canvas(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.items_container = ttk.Frame(canvas)

        self.items_container.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.items_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

       
        

        # Right: billing area
        billing_frame = ttk.Frame(content_frame, borderwidth=1, relief=tk.SOLID)
        billing_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2,5), pady=5)

        # Subtotal display
        subtotal_frame = ttk.Frame(billing_frame, height=50)
        subtotal_frame.pack(fill=tk.X, pady=(10,5))
        ttk.Label(subtotal_frame, text="TOTAL", font=(None, 16, 'bold')).pack(side=tk.LEFT, padx=10)


        self.lbl_dinero = ttk.Label(subtotal_frame, text="0", font=(None, 16, 'bold')) # Aqui es dodne se guarda la plata
        self.lbl_dinero.pack(side=tk.RIGHT, padx=10)
        # Code entry
        entry_frame = ttk.Frame(billing_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        ttk.Label(entry_frame, text="Ingresar código:").pack(side=tk.LEFT, padx=10)

        self.code_entry = ttk.Entry(entry_frame) # Nombre de la entrada 
        self.code_entry.pack(fill=tk.X, padx=10, expand=True)

        # Finish button
        finish_frame = ttk.Frame(billing_frame)
        finish_frame.pack(fill=tk.BOTH, expand=True, pady=(5,10)) # Boton de facturar 
        self.btn_terminar = ttk.Button(finish_frame, text="Terminar", command=self.facturar)
        self.btn_terminar.pack(pady=20)


        #Cuando el entry reciva el enter llama a la funcion
        self.code_entry.bind("<Return>", self._add_item_placeholder)

       
        
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
        # Example of a single product item row
        item_frame = ttk.Frame(self.items_container, borderwidth=1, relief=tk.RIDGE, padding=5)
        item_frame.pack(fill=tk.X, pady=2, padx=2)
        if(buscarInformacionProducto(codigo)!=False):
            producto = buscarInformacionProducto(codigo)
            price = float(producto["Ganancia"]) + float(producto["Precio de compra"])
            lbl_product = ttk.Label(item_frame, text=producto["Nombre"], font=(None, 12, 'bold'))
            lbl_price = ttk.Label(item_frame, text=str(price), font=(None, 12))
            item_frame.codigo = codigo
            item_frame.price = price
            btn_dup = ttk.Button(item_frame, text="Duplicar", command=lambda: self._duplicar_item(item_frame))
            btn_remove = ttk.Button(item_frame, text="Quitar", command=lambda: self._eliminar_item(item_frame))
            dineroActual = float(self.lbl_dinero.cget("text"))
            dineroActual += price
            self.lbl_dinero.config(text=str(dineroActual))
            AgregarProducto(codigo)
        else:
            lbl_product = ttk.Label(item_frame, text="No encontrado", font=(None, 12))
            lbl_price = ttk.Label(item_frame, text="", font=(None, 12))
            btn_dup = ttk.Button(item_frame, text="Duplicar", command=lambda: self._duplicar_item(item_frame))
            btn_remove = ttk.Button(item_frame, text="Quitar", command=lambda: self._eliminar_item(item_frame))
                                                                            
        lbl_product.pack(side=tk.LEFT)
        lbl_price.pack(side=tk.RIGHT, padx=(0, 10))
        btn_dup.pack(side=tk.RIGHT, padx=5)
        btn_remove.pack(side=tk.RIGHT)
        self.code_entry.delete(0, tk.END)
    from tkinter import messagebox

    def facturar(self):
        total = Generar_Ticket()

        # 1. Borrar todos los elementos dentro de items_container
        for widget in self.items_container.winfo_children():
            widget.destroy()
        self.lbl_dinero.config(text=str("0"))
        # 2. Mostrar mensaje emergente con el total
        messagebox.showinfo("Factura generada", f"Total a pagar: ${total}")

if __name__ == "__main__":
    app = FacturacionUI()
    app.mainloop()