
# 🛒 Sistema de Gestión para Tiendas - Control de Productos y Ventas

Este proyecto es una aplicación de escritorio desarrollada en **Python con Tkinter**. Está diseñada para ofrecer una solución integral y sencilla a **pequeños negocios o tiendas**, permitiendo llevar el control de productos, registrar ventas y analizar el rendimiento económico del negocio.

---

## 🚀 ¿Qué puedes hacer con esta aplicación?

-   🧾 **Registrar ventas** detalladas de productos.
-   📦 **Agregar, editar y eliminar productos** de forma intuitiva.
-   📊 **Consultar estadísticas y rendimiento económico** en un rango de fechas.
-   📚 **Visualizar historial completo de transacciones.**
-   ✅ **Guardar toda la información en archivos JSON**, lo que facilita el almacenamiento y exportación.

---

## 🧩 Estructura de la Interfaz

### 🪟 Ventana Principal

La ventana principal está dividida en varias secciones clave:

-   **Menú de navegación izquierdo**: Permite cambiar entre las secciones de _Rendimiento_ y _Productos_.
-   **Panel derecho**: Muestra formularios, detalles y opciones específicas de la sección seleccionada.

---

## 🔧 Funcionalidades por Módulo

### 1. 📈 Módulo de Rendimiento (Ventas)

Este módulo permite visualizar el rendimiento de ventas y analizar las estadísticas generadas por las transacciones.

**Funcionalidades:**
-   Muestra la **ganancia total** generada.
-   Indica las **ventas netas** acumuladas.
-   Resume la **cantidad total de productos vendidos**.
-   Lista los **productos vendidos por nombre y cantidad**.
-   Permite la **visualización detallada por transacción individual**.
-   Ofrece un **resumen filtrado por rango de fechas**. El usuario ingresa una fecha de inicio y fin, y al presionar "Consultar", se muestran los datos correspondientes.
    -   Llama internamente a la función: `analizar_ventas_por_fecha(fecha_inicio_str, fecha_fin_str)`.

**Interfaz:**
-   `self.lbl_ganancia`: Muestra la ganancia acumulada.
-   `self.lbl_venta_total`: Muestra la venta neta total.
-   Contenedor dinámico que genera un botón por transacción (`TRANSACCIÓN #N`), permitiendo ver los detalles completos de cada una.
-   Dos campos de entrada para fechas (inicio y fin) para la consulta por rango.
-   Al consultar por rango, se muestran los días con:
    -   Total vendido.
    -   Total de ganancias.
    -   Productos más vendidos.

**Validaciones:**
-   Si las fechas son inválidas o mal ingresadas para la consulta por rango, se muestra un error vía `messagebox`.

**Datos Utilizados:**
-   Fuente de información principal: `dinero.json`.
-   También consulta `transacciones.json` para detalles.

### 2. 📦 Módulo de Productos

Este módulo permite gestionar el inventario de productos de forma manual y visual. Todas las operaciones se reflejan en el archivo `productos.json`.

**Funcionalidades Incluidas:**
-   📄 Mostrar lista de productos existentes como botones.
-   🔍 Ver detalles individuales de un producto al hacer clic.
-   ✏️ Editar productos ya existentes (eliminando el antiguo y creando uno nuevo con los cambios).
-   ➕ Agregar nuevos productos, validando los campos:
    -   Código (único por producto).
    -   Precio de compra (número).
    -   Ganancia (número).
    -   Nombre (cadena).
-   🗑️ Eliminar un producto tras confirmar con el usuario.

**Interfaz:**
-   📋 Panel izquierdo: lista de productos como botones grandes y legibles.
-   🧾 Panel derecho: formulario para añadir o editar productos.
-   🔁 Botón "Nuevo producto" para resetear el formulario.

**Validaciones (Generales en el módulo):**
-   Impide guardar si faltan campos o hay datos inválidos.
-   Permite modificar productos existentes sin duplicar códigos.
-   Utiliza funciones `Agregar_Producto()` y `Quitar_Producto()` para persistencia.
-   Verificación de que todos los campos obligatorios estén completos.
-   Validación de que los campos numéricos contengan datos válidos.
-   Comprobación de códigos duplicados.
-   Confirmación de eliminación mediante `messagebox.askyesno`.

**Archivo Afectado:**
-   `productos.json`

---

### 1. 📦 Módulo de Caja
REadme en organizacion...

## 📂 Estructura de los Archivos de Datos

La aplicación trabaja con archivos `.json` como base de persistencia. Esto permite que todos los datos sean almacenados localmente, sin necesidad de bases de datos externas.

### 1. `productos.json`

Este archivo contiene todos los productos que se han registrado. Cada producto es un diccionario con la siguiente estructura:

```json
{
  "Codigo": "001",
  "PrecioCompra": 1000,
  "Ganancia": 30,
  "Nombre": "Producto Ejemplo"
}
```
-   **Codigo**: Identificador único del producto.
-   **PrecioCompra**: Precio de adquisición del producto.
-   **Ganancia**: Porcentaje de ganancia que se aplicará al precio.
-   **Nombre**: Nombre o descripción del producto.

Se utiliza para mostrar la lista de productos disponibles, así como para editar y eliminar productos existentes.

### 2. `transacciones.json`

Registra todas las ventas realizadas por el sistema. Cada entrada representa una transacción con los siguientes datos:

```json
{
  "fecha": "2025-05-20",
  "productos": [
    {
      "codigo": "001",
      "nombre": "Producto Ejemplo",
      "cantidad": 2,
      "precio_unitario": 1300
    }
  ],
  "total": 2600
}
```
-   **fecha**: Día en que se hizo la transacción.
-   **productos**: Lista de productos vendidos con su código, nombre, cantidad y precio unitario en el momento de la venta.
-   **total**: Suma total de la venta.

Se utiliza para consultas históricas, auditoría y para la visualización detallada en el módulo de rendimiento.

### 3. `dinero.json`

Este archivo almacena un resumen diario del rendimiento del negocio. Se genera o actualiza a partir de las transacciones para analizar ventas y ganancias por fecha. Su estructura es:

```json
{
  "YYYY-MM-DD": {
    "ganancias_totales": 600.0,
    "cantidad_productos_vendidos_total": 4,
    "cantidad_por_producto": {
      "Producto Ejemplo": 2
    },
    "ventas_netas_totales": 2600.0
  }
}
```
-   La **clave principal** es la fecha (formato `YYYY-MM-DD`).
-   **ganancias_totales**: Beneficio neto obtenido ese día.
-   **cantidad_productos_vendidos_total**: Suma total de unidades vendidas ese día.
-   **cantidad_por_producto**: Diccionario que detalla cuántas unidades de cada producto se vendieron ese día.
-   **ventas_netas_totales**: Ingreso bruto antes de descontar costos de ese día.

Este archivo es fundamental para el módulo de rendimiento, que permite al usuario hacer análisis entre rangos de fechas.

---

## 🖼️ Diseño y Usabilidad

La interfaz fue mejorada progresivamente:

-   Aumento del tamaño de fuentes.
-   Uso de `fill=tk.X` y `expand=True` para mejor distribución de los widgets.
-   Botones visualmente más atractivos con `padding` y estilos.
-   Organización en `frames` para mantener todo limpio y responsive.
-   Separación clara de funcionalidades por paneles:
    -   Izquierda: navegación/listas.
    -   Derecha: formularios/detalles.

---

## 🛠️ Tecnologías y Librerías Utilizadas

-   **Lenguaje:** Python 3.11
-   **Interfaz gráfica:** Tkinter (`ttk`, `Canvas`, `Frame`, `Entry`, `Button`, etc.)
-   **Persistencia de datos:** Archivos `.json`
-   **Manejo de sistema de archivos:** `os`
-   **Empaquetado (opcional):** PyInstaller (para convertirlo en `.exe`)

---

## 💻 Cómo Ejecutar el Proyecto

### 🔸 Requisitos

-   Python 3.10 o superior.
-   Dependencias estándar de Python (Tkinter, json, os, datetime, etc., que usualmente vienen con Python).

### 🔸 Para ejecutarlo como script

Asegúrate de tener Python instalado y navega hasta el directorio del proyecto en tu terminal. Luego ejecuta:
```bash
python main.py
```



---

## 📋 Notas Finales

-   El sistema **no depende de bases de datos externas**. Todo se guarda de forma local en archivos `.json`.
-   Pensado para ser **liviano, portable y funcional** en cualquier máquina con Windows y Python instalado.

### 🚀 Futuras Versiones Podrían Incluir:

-   Exportación de reportes a PDF.
-   Gráficas de rendimiento más visuales.
-   Autoguardado con respaldo automático de los archivos JSON.
-   Posibilidad de conexión con sistemas de inventario en la nube (esto requeriría un cambio significativo en la persistencia de datos).

```
