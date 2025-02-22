import tkinter as tk
from tkinter import ttk, messagebox
import time

Carrito = []

def agregar_producto():
    nombre = entry_nombre.get().strip()
    if not nombre:
        messagebox.showerror("❌ Error", "El nombre del producto no puede estar vacío.")
        return

    for item in Carrito:
        if item[0].lower() == nombre.lower():
            messagebox.showerror("⚠️ Error", "El producto ya existe en el carrito.")
            return

    try:
        precio = float(entry_precio.get())
        cantidad = int(entry_cantidad.get())
        if precio <= 0 or cantidad < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("⚠️ Error", "Ingrese valores válidos para precio y cantidad.")
        return

    Carrito.append([nombre, precio, cantidad])
    animar_actualizacion()
    messagebox.showinfo("✅ Éxito", "Producto agregado al carrito 🛒")

def quitar_producto():
    seleccionado = listbox.selection()
    if seleccionado:
        index = int(seleccionado[0])
        Carrito.pop(index)
        animar_actualizacion()
        messagebox.showinfo("🗑️ Éxito", "Producto eliminado del carrito.")
    else:
        messagebox.showerror("⚠️ Error", "Seleccione un producto para eliminar.")

def cambiar_producto():
    seleccionado = listbox.selection()
    if not seleccionado:
        messagebox.showerror("⚠️ Error", "Seleccione un producto para modificar.")
        return

    try:
        precio = float(entry_precio.get())
        cantidad = int(entry_cantidad.get())
        if precio <= 0 or cantidad < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("⚠️ Error", "Ingrese valores válidos para precio y cantidad.")
        return

    index = int(seleccionado[0])
    Carrito[index][1] = precio
    Carrito[index][2] = cantidad
    animar_actualizacion()
    messagebox.showinfo("✅ Éxito", "Producto modificado correctamente ✨")

def generar_ticket():
    if not Carrito:
        messagebox.showwarning("⚠️ Advertencia", "El carrito está vacío. Agregue productos antes de generar el ticket.")
        return

    total = sum(item[1] * item[2] for item in Carrito)
    cantidad_total = sum(item[2] for item in Carrito)
    detalles = "\n".join(f"🛍️ {item[0]} - ${item[1]:.2f} x {item[2]} unidades" for item in Carrito)

    if cantidad_total > 10:
        descuento = total * 0.10
        total -= descuento
        detalles += f"\n\n🎉 Descuento aplicado: -${descuento:.2f} (10% por más de 10 unidades)"

    messagebox.showinfo("🧾 Ticket de Compra", f"Productos en el carrito:\n{detalles}\n\n💰 Total: ${total:.2f}")

def animar_actualizacion():
    for _ in range(5):
        listbox.tag_configure("highlight", background="#d9f7be")
        root.update()
        time.sleep(0.1)
        listbox.tag_configure("highlight", background="#ffffff")
        root.update()
        time.sleep(0.1)
    actualizar_lista()

def actualizar_lista():
    listbox.delete(*listbox.get_children())
    for i, item in enumerate(Carrito):
        listbox.insert("", "end", iid=i, values=(item[0], f"💲{item[1]:.2f}", f"📦 {item[2]}"))

root = tk.Tk()
root.title("🛒 Carrito de Compras")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Entradas
entry_nombre = ttk.Entry(frame, width=20)
entry_precio = ttk.Entry(frame, width=10)
entry_cantidad = ttk.Entry(frame, width=10)
entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
entry_precio.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
entry_cantidad.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Etiquetas
ttk.Label(frame, text="📦 Nombre:").grid(row=0, column=0)
ttk.Label(frame, text="💲 Precio:").grid(row=1, column=0)
ttk.Label(frame, text="🔢 Cantidad:").grid(row=2, column=0)

# Botones
ttk.Button(frame, text="➕ Agregar", command=agregar_producto).grid(row=3, column=0, pady=5, sticky="ew")
ttk.Button(frame, text="🗑️ Quitar", command=quitar_producto).grid(row=3, column=1, pady=5, sticky="ew")
ttk.Button(frame, text="✏️ Modificar", command=cambiar_producto).grid(row=3, column=2, pady=5, sticky="ew")
ttk.Button(frame, text="🧾 Generar Ticket", command=generar_ticket).grid(row=4, column=1, pady=5, sticky="ew")

# Lista estilo Treeview
listbox = ttk.Treeview(root, columns=("Nombre", "Precio", "Cantidad"), show="headings")
listbox.heading("Nombre", text="📦 Nombre")
listbox.heading("Precio", text="💲 Precio")
listbox.heading("Cantidad", text="🔢 Cantidad")
listbox.column("Nombre", width=200, anchor="center")
listbox.column("Precio", width=100, anchor="center")
listbox.column("Cantidad", width=100, anchor="center")
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
