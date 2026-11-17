# labcontrol.py - Laboratorio de Control de Calidad (LabControl)
# Ejecutar con:  python labcontrol.py     (con logo.png y mascota.png en la misma carpeta)
# Instalar el conector una sola vez:  python -m pip install mysql-connector-python
#
# La conexion a MySQL sigue el tutorial de la profe:
#   conexion = conectar()             -> abre la conexion (funcion conectar, mas abajo)
#   cursor = conexion.cursor()        -> crea el cursor
#   cursor.execute(sql, datos)        -> ejecuta el SQL (con %s y una tupla de datos)
#   cursor.fetchall()                 -> recupera los registros (SELECT)
#   conexion.commit()                 -> confirma INSERT / UPDATE / DELETE
#   cursor.close() / conexion.close() -> cierra todo (en el finally)
import tkinter as tk
from tkinter import messagebox, ttk
import sys
print(sys.executable)
import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="LUA",
        database="laboratorio"
    )


error_mostrado = False   



def leer(sql, datos):
    global error_mostrado
    filas = []
    try:
        conexion = conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            registros = cursor.fetchall()
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
        for registro in registros:
            fila = []
            for valor in registro:
                tipo = type(valor).__name__
                if tipo == "Decimal":
                    valor = float(valor)
                elif tipo == "date" or tipo == "datetime":
                    valor = str(valor)
                fila.append(valor)
            filas.append(fila)
    except mysql.connector.Error as error:
        if not error_mostrado:
            error_mostrado = True
            messagebox.showerror("Error de base de datos", str(error))
    return filas


def cargar_lista(lista, sql):
    lista.clear()
    for fila in leer(sql, ()):
        lista.append(fila)


def ejecutar(sql, datos):
    try:
        conexion = conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
        return True
    except mysql.connector.Error as error:
        if error.errno == 1451:
            messagebox.showerror("No se puede eliminar",
                                 "Este registro está relacionado con otros datos (por ejemplo un lote, una muestra o un certificado).")
        else:
            messagebox.showerror("Error de base de datos", str(error))
        return False


# DELETE de un registro por su id
def eliminar_registro(tabla_bd, columna, numero):
    sql = "DELETE FROM " + tabla_bd + " WHERE " + columna + " = %s"
    if ejecutar(sql, (numero,)):
        aviso_eliminado()
        return True
    return False


def eliminar_ensayo(id_ensayo):
    try:
        conexion = conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM mediciones WHERE id_ensayo = %s", (id_ensayo,))
            cursor.execute("DELETE FROM ensayos WHERE id_ensayo = %s", (id_ensayo,))
            conexion.commit()
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
        aviso_eliminado()
        return True
    except mysql.connector.Error as error:
        messagebox.showerror("Error de base de datos", str(error))
        return False


ventana = tk.Tk()
ventana.title("Laboratorio de Control de Calidad")
ventana.geometry("1280x820")
ventana.configure(bg="#f1f6f2")


VERDE = "#2f7d4f"
VERDE_CLARO = "#e0f0e4"
FONDO = "#f1f6f2"
BORDE = "#dfe7e1"


# Variable de control: guarda en que pantalla estamos ("Inicio", "Productos", etc.)
pantalla_actual = tk.StringVar(value="Inicio")


menu = tk.Frame(ventana, bg="white", width=240, height=820)
menu.place(x=0, y=0)



def entrar(e):
    e.widget.config(bg="#9dc166")


def salir(e):
    # Si el boton es el de la pantalla actual vuelve a verde clarito, si no a blanco
    if e.widget["text"] == pantalla_actual.get():
        e.widget.config(bg=VERDE_CLARO)
    else:
        e.widget.config(bg="white")



def ocultar_todas():
    p_inicio.place(x=3000, y=0)
    p_productos.place(x=3000, y=0)
    p_lotes.place(x=3000, y=0)
    p_muestras.place(x=3000, y=0)
    p_tipos.place(x=3000, y=0)
    p_ensayos.place(x=3000, y=0)
    p_certificados.place(x=3000, y=0)
    p_directores.place(x=3000, y=0)


def pintar_menu():
    botones = [boton1, boton2, boton3, boton4, boton5,
               boton6, boton7, boton8]
    for b in botones:
        if b["text"] == pantalla_actual.get():
            b.config(bg=VERDE_CLARO)
        else:
            b.config(bg="white")


def mostrar(nombre, pantalla):
    ocultar_todas()
    pantalla.place(x=240, y=0)
    pantalla_actual.set(nombre)
    pintar_menu()


def ir_inicio():
    recargar_datos()
    actualizar_listas()
    buscar_resultados()
    mostrar("Inicio", p_inicio)


def ir_productos():
    recargar_datos()
    cargar_productos()
    mostrar("Productos", p_productos)


def ir_lotes():
    recargar_datos()
    actualizar_listas()
    cargar_lotes()
    mostrar("Lotes", p_lotes)


def ir_muestras():
    recargar_datos()
    actualizar_listas()
    cargar_muestras()
    mostrar("Muestras", p_muestras)


def ir_tipos():
    recargar_datos()
    actualizar_listas()
    cargar_tipos()
    cargar_criterios()
    mostrar("Tipos de ensayo", p_tipos)


def ir_ensayos():
    recargar_datos()
    actualizar_listas()
    cargar_ensayos()
    mostrar("Registro de ensayos", p_ensayos)


def ir_certificados():
    recargar_datos()
    actualizar_listas()
    cargar_certificados()
    mostrar("Certificados", p_certificados)


def ir_directores():
    recargar_datos()
    cargar_directores()
    mostrar("Directores de laboratorio", p_directores)



boton1 = tk.Button(menu, text="Inicio",
                   font=("Arial", 12, "bold"),
                   relief="flat",
                   bg=VERDE_CLARO,
                   anchor="w",
                   padx=15,
                   command=ir_inicio)
boton1.place(x=12, y=76, width=215, height=40)
boton1.bind("<Enter>", entrar)
boton1.bind("<Leave>", salir)


boton2 = tk.Button(menu, text="Productos",
                   font=("Arial", 12, "bold"),
                   relief="flat",
                   bg="white",
                   anchor="w",
                   padx=15,
                   command=ir_productos)
boton2.place(x=12, y=120, width=215, height=40)
boton2.bind("<Enter>", entrar)
boton2.bind("<Leave>", salir)


boton3 = tk.Button(menu, text="Lotes",
                   font=("Arial", 12, "bold"),
                   relief="flat",
                   bg="white",
                   anchor="w",
                   padx=15,
                   command=ir_lotes)
boton3.place(x=12, y=164, width=215, height=40)
boton3.bind("<Enter>", entrar)
boton3.bind("<Leave>", salir)


boton4 = tk.Button(menu, text="Muestras",
                   font=("Arial", 12, "bold"),
                   relief="flat",
                   bg="white",
                   anchor="w",
                   padx=15,
                   command=ir_muestras)
boton4.place(x=12, y=208, width=215, height=40)
boton4.bind("<Enter>", entrar)
boton4.bind("<Leave>", salir)


boton5 = tk.Button(menu, text="Tipos de ensayo",
                   font=("Arial", 12, "bold"),
                   relief="flat",
                   bg="white",
                   anchor="w",
                   padx=15,
                   command=ir_tipos)
boton5.place(x=12, y=252, width=215, height=40)
boton5.bind("<Enter>", entrar)
boton5.bind("<Leave>", salir)


boton6 = tk.Button(menu, text="Registro de ensayos",
                   font=("Arial", 12, "bold"),
                   relief="flat",
                   bg="white",
                   anchor="w",
                   padx=15,
                   command=ir_ensayos)
boton6.place(x=12, y=296, width=215, height=40)
boton6.bind("<Enter>", entrar)
boton6.bind("<Leave>", salir)


boton7 = tk.Button(menu, text="Certificados",
                   font=("Arial", 12, "bold"),
                   relief="flat",
                   bg="white",
                   anchor="w",
                   padx=15,
                   command=ir_certificados)
boton7.place(x=12, y=340, width=215, height=40)
boton7.bind("<Enter>", entrar)
boton7.bind("<Leave>", salir)


boton8 = tk.Button(menu, text="Directores de laboratorio",
                   font=("Arial", 12, "bold"),
                   relief="flat",
                   bg="white",
                   anchor="w",
                   padx=15,
                   command=ir_directores)
boton8.place(x=12, y=384, width=215, height=40)
boton8.bind("<Enter>", entrar)
boton8.bind("<Leave>", salir)




p_inicio = tk.Frame(ventana, bg=FONDO, width=1040, height=820)
p_inicio.place(x=240, y=0)


banner = tk.Frame(p_inicio, bg="white", width=976, height=252,)
banner.place(x=32, y=28)


lbl_titulo = tk.Label(banner, text="Controlá la calidad de tus productos",
                      bg="white", font=("Arial", 22, "bold"))
lbl_titulo.place(x=29, y=105)
sub_titulo = tk.Label(banner, text="administra y organiza desde un solo lugar ",
                      bg="white", font=("Arial", 11, "bold"))
sub_titulo.place(x=29, y=140)


productos = []
lotes = []
muestras = []
tipos = []
criterios = []
directores = []
ensayos = []
mediciones = []
certificados = []

def recargar_datos():
    global error_mostrado
    error_mostrado = False
    cargar_lista(productos, "SELECT id_producto, nombre, descripcion FROM productos ORDER BY id_producto")
    cargar_lista(lotes, "SELECT id_lote, cod, fechas_relevantes, id_producto FROM lotes ORDER BY id_lote")
    cargar_lista(muestras, "SELECT id_muestra, cod, f_extraccion, id_lote FROM muestras ORDER BY id_muestra")
    cargar_lista(tipos, "SELECT id_tipo, denominacion, descripcion FROM tipo_ensayos ORDER BY id_tipo")
    cargar_lista(criterios, "SELECT id_criterio, nombre, parametros, limites, condiciones, limite_min, limite_max, id_tipo "
                            "FROM criterios_acep ORDER BY id_criterio")
    cargar_lista(directores, "SELECT id_director, nombre, apellido, dni, firma FROM directores_lab ORDER BY id_director")
    cargar_lista(ensayos, "SELECT id_ensayo, responsable, fecha, estado, id_muestra, id_tipo FROM ensayos ORDER BY id_ensayo")
    cargar_lista(mediciones, "SELECT id_medicion, parametro, valor, unidad_m, resultado, id_ensayo "
                             "FROM mediciones ORDER BY id_medicion")
    cargar_lista(certificados, "SELECT id_certificado, fecha_emision, id_lote, id_director "
                               "FROM certific_calidad ORDER BY id_certificado")


def crear_caja(padre, x, y, ancho, alto):
    caja = tk.Frame(padre, bg="white", width=ancho, height=alto)
    caja.place(x=x, y=y)
    return caja


def titulo_pantalla(padre, ruta, texto, subtitulo):
    tk.Label(padre, text=ruta, bg=FONDO, fg="#666",
             font=("Arial", 9)).place(x=32, y=22)
    tk.Label(padre, text=texto, bg=FONDO, fg="#1a2b20",
             font=("Arial", 20, "bold")).place(x=32, y=42)
    tk.Label(padre, text=subtitulo, bg=FONDO, fg="#555",
             font=("Arial", 10)).place(x=32, y=84)

def titulo_caja(caja, texto):
    etiqueta = tk.Label(caja, text=texto, bg="white",
                        font=("Arial", 12, "bold"))
    etiqueta.place(x=21, y=12)
    return etiqueta

def nota_caja(caja, texto, x, y):
    tk.Label(caja, text=texto, bg="white", fg="#666",
             font=("Arial", 9)).place(x=x, y=y)


def etiqueta_campo(caja, texto, x, y):
    tk.Label(caja, text=texto, bg="white", fg="#333",
             font=("Arial", 9, "bold")).place(x=x, y=y)

def cuadro_texto(caja, variable, x, y, ancho):
    cuadro = tk.Entry(caja, textvariable=variable, font=("Arial", 11),
                      relief="solid", bd=1)
    cuadro.place(x=x, y=y, width=ancho, height=34)
    return cuadro


def lista_desplegable(caja, variable, valores, x, y, ancho):
    lista = ttk.Combobox(caja, textvariable=variable, values=valores,
                         state="readonly", font=("Arial", 10))
    lista.place(x=x, y=y, width=ancho, height=34)
    return lista


def boton_verde(caja, texto, x, y, ancho, comando):
    b = tk.Button(caja, text=texto, bg=VERDE, fg="white",
                  font=("Arial", 10, "bold"), relief="flat", command=comando)
    b.place(x=x, y=y, width=ancho, height=38)
    return b


def boton_blanco(caja, texto, x, y, ancho, comando):
    b = tk.Button(caja, text=texto, bg="white", fg=VERDE,
                  font=("Arial", 10, "bold"), relief="solid", bd=1,
                  command=comando)
    b.place(x=x, y=y, width=ancho, height=38)
    return b


def cabecera_tabla(caja, y, textos, posiciones, ancho):
    barra = tk.Frame(caja, bg="#edf3ee", width=ancho, height=32)
    barra.place(x=11, y=y)
    for i in range(len(textos)):
        tk.Label(barra, text=textos[i], bg="#edf3ee",
                 font=("Arial", 10, "bold")).place(x=posiciones[i] - 11, y=6)


def zona_tabla(caja, y, alto):
    zona = tk.Frame(caja, bg="white", width=976, height=alto)
    zona.place(x=0, y=y)
    return zona


def borrar_filas(zona):
    for w in zona.winfo_children():
        w.destroy()


def fila_texto(caja, y, textos, posiciones):
    for i in range(len(textos)):
        tk.Label(caja, text=textos[i], bg="white").place(x=posiciones[i], y=y)


# Línea finita que separa las filas
def linea(caja, y, ancho):
    tk.Frame(caja, bg="#e8eee9", width=ancho, height=1).place(x=11, y=y)


def pintar_estado(etiqueta, texto):
    if texto in ["Satisfactorio", "Completado", "Apto", "Firmado", "Certificado emitido"]:
        etiqueta.config(text=texto, bg="#dff0e3", fg=VERDE)
    elif texto in ["No satisfactorio", "No apto", "Sin firma"]:
        etiqueta.config(text=texto, bg="#fde4e4", fg="#b03030")
    else:
        etiqueta.config(text=texto, bg="#fdf0c8", fg="#8a6100")


def etiqueta_estado(caja, texto, x, y):
    etiqueta = tk.Label(caja, font=("Arial", 9, "bold"), padx=8)
    etiqueta.place(x=x, y=y)
    pintar_estado(etiqueta, texto)
    return etiqueta


def botones_fila(caja, x, y, nombre, comando_editar, comando_borrar):
    def eliminar():
        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que querés eliminar " + nombre + "?")
        if respuesta:
            comando_borrar()


    boton_editar = tk.Button(caja, text="Editar", bg="white", fg=VERDE,
                             font=("Arial", 9, "bold"), relief="solid", bd=1,
                             command=comando_editar)
    boton_editar.place(x=x, y=y, width=63, height=28)


    boton_eliminar = tk.Button(caja, text="Eliminar", bg="white", fg="#b03030",
                               font=("Arial", 9, "bold"), relief="solid", bd=1,
                               command=eliminar)
    boton_eliminar.place(x=x + 69, y=y, width=76, height=28)


def aviso_eliminado():
    messagebox.showinfo("Listo", "Eliminado correctamente")


def txt(valor, largo=100):
    if valor == None:
        return ""
    return str(valor)[0:largo]


def sacar_id(texto):
    return texto.split(" - ")[0]


def buscar(tabla, id_buscado):
    for fila in tabla:
        if str(fila[0]) == str(id_buscado):
            return fila
    return None


def buscar_texto(lista, id_buscado):
    for t in lista:
        if sacar_id(t) == str(id_buscado):
            return t
    return ""

def ultimos(tabla, cantidad):
    resultado = []
    for i in range(len(tabla) - 1, -1, -1):
        if len(resultado) < cantidad:
            resultado.append(tabla[i])
    return resultado


def fecha_ok(texto):
    if len(texto) != 10:
        return False
    if texto[4] != "-" or texto[7] != "-":
        return False
    return (texto[0:4] + texto[5:7] + texto[8:10]).isdigit()


def a_numero(texto):
    try:
        return float(texto.replace(",", "."))
    except ValueError:
        return None


def texto_lote(id_lote, cod, producto):
    return str(id_lote) + " - Lote " + str(cod) + " (" + producto + ")"



lista_productos = []
lista_lotes = []
lista_tipos = []
lista_directores = []
lista_aptos = []       
lista_muestras = []   


def actualizar_listas():
    lista_productos.clear()
    for f in productos:
        lista_productos.append(str(f[0]) + " - " + f[1])


    lista_lotes.clear()
    for f in lotes:
        producto = buscar(productos, f[3])
        lista_lotes.append(texto_lote(f[0], f[1], producto[1]))


    lista_tipos.clear()
    for f in tipos:
        lista_tipos.append(str(f[0]) + " - " + f[1])


    lista_directores.clear()
    for f in directores:
        texto = str(f[0]) + " - " + f[1] + " " + f[2]
        if f[4] != 1:
            texto = texto + " (sin firma)"
        lista_directores.append(texto)


    cb_lote_producto.config(values=lista_productos)
    cb_mue_lote.config(values=lista_lotes)
    cb_ens_lote.config(values=lista_lotes)
    cb_ens_tipo.config(values=lista_tipos)
    cb_crit_tipo.config(values=lista_tipos)
    cb_fil_producto.config(values=["Todos"] + lista_productos)
    cb_fil_lote.config(values=["Todos"] + lista_lotes)
    cb_cert_director.config(values=lista_directores)


    if var_crit_tipo.get() == "" and len(lista_tipos) > 0:
        var_crit_tipo.set(lista_tipos[0])




p_productos = tk.Frame(ventana, bg=FONDO, width=1040, height=820)
p_productos.place(x=3000, y=0)   


titulo_pantalla(p_productos, "Inicio › Productos", "Gestión de productos",
                "Alta, consulta, modificación y baja de los productos que analiza el laboratorio.")

var_prod_nombre = tk.StringVar()
var_prod_desc = tk.StringVar()
var_prod_id = tk.StringVar()    


caja = crear_caja(p_productos, 32, 110, 976, 165)
titulo_caja(caja, "Producto")
etiqueta_campo(caja, "Nombre (hasta 20 letras)", 21, 46)
cuadro_texto(caja, var_prod_nombre, 21, 68, 460)
etiqueta_campo(caja, "Descripción", 495, 46)
cuadro_texto(caja, var_prod_desc, 495, 68, 460)


def limpiar_producto():
    var_prod_id.set("")
    var_prod_nombre.set("")
    var_prod_desc.set("")


def guardar_producto():
    if var_prod_nombre.get() == "" or var_prod_desc.get() == "":
        messagebox.showwarning("Faltan datos", "Completá el nombre y la descripción")
    elif len(var_prod_nombre.get()) > 20:
        messagebox.showwarning("Nombre muy largo", "El nombre puede tener hasta 20 letras")
    else:
        datos = (var_prod_nombre.get(), var_prod_desc.get())
        if var_prod_id.get() == "":
            sql = "INSERT INTO productos (nombre, descripcion) VALUES (%s, %s)"
        else:
            sql = "UPDATE productos SET nombre = %s, descripcion = %s WHERE id_producto = %s"
            datos = datos + (int(var_prod_id.get()),)
        if ejecutar(sql, datos):
            messagebox.showinfo("Listo", "Producto guardado")
            limpiar_producto()
            recargar_datos()
            cargar_productos()


boton_verde(caja, "Guardar producto", 21, 114, 160, guardar_producto)
boton_blanco(caja, "Limpiar", 195, 114, 100, limpiar_producto)


caja_prod = crear_caja(p_productos, 32, 290, 976, 400)
titulo_caja(caja_prod, "Productos registrados (últimos 8)")
cabecera_tabla(caja_prod, 46, ["ID", "Nombre", "Descripción", "Acciones"],
               [33, 274, 516, 757], 954)
zona_prod = zona_tabla(caja_prod, 84, 310)


def fila_producto(ry, dato):
   
    fila_texto(zona_prod, ry + 10, [str(dato[0]), dato[1], txt(dato[2], 35)], [33, 274, 516])


    def editar():
        var_prod_id.set(str(dato[0]))
        var_prod_nombre.set(dato[1])
        var_prod_desc.set(dato[2])


    def borrar():
        if eliminar_registro("productos", "id_producto", dato[0]):
            recargar_datos()
            cargar_productos()


    botones_fila(zona_prod, 757, ry + 5, "el producto " + dato[1], editar, borrar)
    linea(zona_prod, ry + 37, 954)


def cargar_productos():
    borrar_filas(zona_prod)
    # SQL de referencia: SELECT * FROM productos;
    filas = ultimos(productos, 8)
    for i in range(len(filas)):
        fila_producto(38 * i, filas[i])



p_lotes = tk.Frame(ventana, bg=FONDO, width=1040, height=820)
p_lotes.place(x=3000, y=0)


titulo_pantalla(p_lotes, "Inicio › Lotes", "Gestión de lotes",
                "Cada producto puede tener varios lotes, identificados por un código.")


var_lote_producto = tk.StringVar()
var_lote_codigo = tk.StringVar()
var_lote_fecha = tk.StringVar()
var_lote_id = tk.StringVar()


caja = crear_caja(p_lotes, 32, 110, 976, 165)
titulo_caja(caja, "Lote")
etiqueta_campo(caja, "Producto", 21, 46)
cb_lote_producto = lista_desplegable(caja, var_lote_producto, lista_productos, 21, 68, 302)
etiqueta_campo(caja, "Código de lote (número)", 337, 46)
cuadro_texto(caja, var_lote_codigo, 337, 68, 302)
etiqueta_campo(caja, "Fecha de ingreso (AAAA-MM-DD)", 653, 46)
cuadro_texto(caja, var_lote_fecha, 653, 68, 302)


def limpiar_lote():
    var_lote_id.set("")
    var_lote_producto.set("")
    var_lote_codigo.set("")
    var_lote_fecha.set("")


def guardar_lote():
    if var_lote_producto.get() == "" or var_lote_codigo.get() == "" or var_lote_fecha.get() == "":
        messagebox.showwarning("Faltan datos", "Completá todos los campos")
    elif not var_lote_codigo.get().isdigit():
        messagebox.showwarning("Dato incorrecto", "El código de lote tiene que ser un número (ej: 1003)")
    elif not fecha_ok(var_lote_fecha.get()):
        messagebox.showwarning("Fecha incorrecta", "Escribí la fecha así: AAAA-MM-DD (ej: 2026-05-20)")
    else:
        datos = (int(var_lote_codigo.get()), var_lote_fecha.get(), int(sacar_id(var_lote_producto.get())))
        if var_lote_id.get() == "":
            sql = "INSERT INTO lotes (cod, fechas_relevantes, id_producto) VALUES (%s, %s, %s)"
        else:
            sql = "UPDATE lotes SET cod = %s, fechas_relevantes = %s, id_producto = %s WHERE id_lote = %s"
            datos = datos + (int(var_lote_id.get()),)
        if ejecutar(sql, datos):
            messagebox.showinfo("Listo", "Lote guardado")
            limpiar_lote()
            recargar_datos()
            cargar_lotes()


boton_verde(caja, "Guardar lote", 21, 114, 140, guardar_lote)
boton_blanco(caja, "Limpiar", 175, 114, 100, limpiar_lote)


caja_lotes = crear_caja(p_lotes, 32, 290, 976, 400)
titulo_caja(caja_lotes, "Lotes registrados (últimos 8)")
cabecera_tabla(caja_lotes, 46, ["Código de lote", "Producto", "Fecha de ingreso", "Acciones"],
               [33, 274, 516, 757], 954)
zona_lotes = zona_tabla(caja_lotes, 84, 310)


def fila_lote(ry, dato):

    producto = buscar(productos, dato[3])
    fila_texto(zona_lotes, ry + 10, [str(dato[1]), producto[1], dato[2]], [33, 274, 516])


    def editar():
        var_lote_id.set(str(dato[0]))
        var_lote_codigo.set(str(dato[1]))
        var_lote_producto.set(str(producto[0]) + " - " + producto[1])
        var_lote_fecha.set(dato[2])


    def borrar():
        if eliminar_registro("lotes", "id_lote", dato[0]):
            recargar_datos()
            cargar_lotes()


    botones_fila(zona_lotes, 757, ry + 5, "el lote " + str(dato[1]), editar, borrar)
    linea(zona_lotes, ry + 37, 954)


def cargar_lotes():
    borrar_filas(zona_lotes)
    filas = ultimos(lotes, 8)
    for i in range(len(filas)):
        fila_lote(38 * i, filas[i])



p_muestras = tk.Frame(ventana, bg=FONDO, width=1040, height=820)
p_muestras.place(x=3000, y=0)


titulo_pantalla(p_muestras, "Inicio › Muestras", "Registro y consulta de muestras",
                "Cada muestra se extrae de un lote y tiene un código que la identifica.")


var_mue_lote = tk.StringVar()
var_mue_codigo = tk.StringVar()
var_mue_fecha = tk.StringVar()
var_mue_id = tk.StringVar()


caja = crear_caja(p_muestras, 32, 110, 976, 165)
titulo_caja(caja, "Muestra")
etiqueta_campo(caja, "Lote (el producto sale del lote)", 21, 46)
cb_mue_lote = lista_desplegable(caja, var_mue_lote, lista_lotes, 21, 68, 302)
etiqueta_campo(caja, "Código de muestra (número)", 337, 46)
cuadro_texto(caja, var_mue_codigo, 337, 68, 302)
etiqueta_campo(caja, "Fecha de extracción (AAAA-MM-DD)", 653, 46)
cuadro_texto(caja, var_mue_fecha, 653, 68, 302)


def limpiar_muestra():
    var_mue_id.set("")
    var_mue_lote.set("")
    var_mue_codigo.set("")
    var_mue_fecha.set("")


def guardar_muestra():
    if var_mue_lote.get() == "" or var_mue_codigo.get() == "" or var_mue_fecha.get() == "":
        messagebox.showwarning("Faltan datos", "Completá todos los campos")
    elif not var_mue_codigo.get().isdigit():
        messagebox.showwarning("Dato incorrecto", "El código de muestra tiene que ser un número (ej: 513)")
    elif not fecha_ok(var_mue_fecha.get()):
        messagebox.showwarning("Fecha incorrecta", "Escribí la fecha así: AAAA-MM-DD (ej: 2026-05-20)")
    else:
        datos = (int(var_mue_codigo.get()), var_mue_fecha.get(), int(sacar_id(var_mue_lote.get())))
        if var_mue_id.get() == "":
            sql = "INSERT INTO muestras (cod, f_extraccion, id_lote) VALUES (%s, %s, %s)"
        else:
            sql = "UPDATE muestras SET cod = %s, f_extraccion = %s, id_lote = %s WHERE id_muestra = %s"
            datos = datos + (int(var_mue_id.get()),)
        if ejecutar(sql, datos):
            messagebox.showinfo("Listo", "Muestra guardada")
            limpiar_muestra()
            recargar_datos()
            cargar_muestras()


boton_verde(caja, "Guardar muestra", 21, 114, 160, guardar_muestra)
boton_blanco(caja, "Limpiar", 195, 114, 100, limpiar_muestra)


caja_mue = crear_caja(p_muestras, 32, 290, 976, 470)
titulo_caja(caja_mue, "Muestras registradas (últimas 10)")
cabecera_tabla(caja_mue, 46,
               ["Código de muestra", "Lote", "Producto", "Fecha de extracción", "Acciones"],
               [33, 214, 395, 576, 757], 954)
zona_mue = zona_tabla(caja_mue, 84, 380)


def fila_muestra(ry, dato):
    # dato = [id_muestra, cod, f_extraccion, id_lote]
    lote = buscar(lotes, dato[3])
    producto = buscar(productos, lote[3])
    fila_texto(zona_mue, ry + 10, [str(dato[1]), str(lote[1]), producto[1], dato[2]], [33, 214, 395, 576])


    def editar():
        var_mue_id.set(str(dato[0]))
        var_mue_codigo.set(str(dato[1]))
        var_mue_fecha.set(dato[2])
        var_mue_lote.set(texto_lote(lote[0], lote[1], producto[1]))


    def borrar():
        if eliminar_registro("muestras", "id_muestra", dato[0]):
            recargar_datos()
            cargar_muestras()


    botones_fila(zona_mue, 757, ry + 5, "la muestra " + str(dato[1]), editar, borrar)
    linea(zona_mue, ry + 37, 954)


def cargar_muestras():
    borrar_filas(zona_mue)
    filas = ultimos(muestras, 10)
    for i in range(len(filas)):
        fila_muestra(38 * i, filas[i])




p_tipos = tk.Frame(ventana, bg=FONDO, width=1040, height=820)
p_tipos.place(x=3000, y=0)


titulo_pantalla(p_tipos, "Inicio › Tipos de ensayo", "Gestión de tipos de ensayo",
                "Cada tipo de ensayo define los parámetros a medir y los límites que deben cumplir los resultados.")


var_tipo_nombre = tk.StringVar()
var_tipo_desc = tk.StringVar()
var_tipo_id = tk.StringVar()
var_crit_tipo = tk.StringVar()
var_crit_nombre = tk.StringVar()
var_crit_parametro = tk.StringVar()
var_crit_min = tk.StringVar()
var_crit_max = tk.StringVar()
var_crit_id = tk.StringVar()


# ---------- Tipo de ensayo (formulario) ----------
caja = crear_caja(p_tipos, 32, 110, 976, 100)
titulo_caja(caja, "Tipo de ensayo")
etiqueta_campo(caja, "Denominación", 21, 38)
cuadro_texto(caja, var_tipo_nombre, 21, 58, 300)
etiqueta_campo(caja, "Descripción", 337, 38)
cuadro_texto(caja, var_tipo_desc, 337, 58, 330)


def limpiar_tipo():
    var_tipo_id.set("")
    var_tipo_nombre.set("")
    var_tipo_desc.set("")


def guardar_tipo():
    if var_tipo_nombre.get() == "" or var_tipo_desc.get() == "":
        messagebox.showwarning("Faltan datos", "Completá la denominación y la descripción")
    else:
        datos = (var_tipo_nombre.get(), var_tipo_desc.get())
        if var_tipo_id.get() == "":
            sql = "INSERT INTO tipo_ensayos (denominacion, descripcion) VALUES (%s, %s)"
        else:
            sql = "UPDATE tipo_ensayos SET denominacion = %s, descripcion = %s WHERE id_tipo = %s"
            datos = datos + (int(var_tipo_id.get()),)
        if ejecutar(sql, datos):
            messagebox.showinfo("Listo", "Tipo de ensayo guardado")
            limpiar_tipo()
            recargar_datos()
            cargar_tipos()


boton_verde(caja, "Guardar tipo", 681, 56, 160, guardar_tipo)
boton_blanco(caja, "Limpiar", 851, 56, 100, limpiar_tipo)


caja_tipos = crear_caja(p_tipos, 32, 218, 976, 250)
titulo_caja(caja_tipos, "Tipos de ensayo (primeros 5)")
cabecera_tabla(caja_tipos, 44, ["ID", "Denominación", "Descripción", "Acciones"],
               [33, 244, 456, 667], 954)
zona_tipos = zona_tabla(caja_tipos, 80, 165)


def fila_tipo(ry, dato):
    
    fila_texto(zona_tipos, ry + 6, [str(dato[0]), dato[1], txt(dato[2], 32)], [33, 244, 456])


    def ver_criterios():
        var_crit_tipo.set(buscar_texto(lista_tipos, dato[0]))
        cargar_criterios()


    def editar():
        var_tipo_id.set(str(dato[0]))
        var_tipo_nombre.set(dato[1])
        var_tipo_desc.set(dato[2])


    def borrar():
        if eliminar_registro("tipo_ensayos", "id_tipo", dato[0]):
            recargar_datos()
            cargar_tipos()
            cargar_criterios()


    boton_ver = tk.Button(zona_tipos, text="Ver criterios", bg="white", fg=VERDE,
                          font=("Arial", 9, "bold"), relief="solid", bd=1,
                          command=ver_criterios)
    boton_ver.place(x=667, y=ry + 2, width=103, height=28)
    botones_fila(zona_tipos, 776, ry + 2, "el tipo de ensayo " + dato[1], editar, borrar)
    linea(zona_tipos, ry + 31, 954)


def cargar_tipos():
    borrar_filas(zona_tipos)
    for i in range(len(tipos)):
        if i < 5:
            fila_tipo(32 * i, tipos[i])


caja_crit = crear_caja(p_tipos, 32, 476, 976, 218)
titulo_caja(caja_crit, "Criterios de aceptación")
nota_caja(caja_crit, "Tipo de ensayo:", 560, 16)
cb_crit_tipo = lista_desplegable(caja_crit, var_crit_tipo, lista_tipos, 660, 8, 296)
cabecera_tabla(caja_crit, 44,
               ["Nombre", "Parámetro", "Límite mínimo", "Límite máximo", "Acciones"],
               [33, 260, 430, 570, 757], 954)
zona_crit = zona_tabla(caja_crit, 80, 130)


def fila_criterio(ry, dato):
    # dato = [id_criterio, nombre, parametros, limites, condiciones, limite_min, limite_max, id_tipo]
    fila_texto(zona_crit, ry + 6, [txt(dato[1], 36), txt(dato[2], 22), str(dato[5]), str(dato[6])],
               [33, 260, 430, 570])


    def editar():
        var_crit_id.set(str(dato[0]))
        var_crit_nombre.set(dato[1])
        var_crit_parametro.set(dato[2])
        var_crit_min.set(str(dato[5]))
        var_crit_max.set(str(dato[6]))


    def borrar():
        if eliminar_registro("criterios_acep", "id_criterio", dato[0]):
            recargar_datos()
            cargar_criterios()


    botones_fila(zona_crit, 757, ry + 2, "el criterio " + dato[1], editar, borrar)
    linea(zona_crit, ry + 31, 954)


def cargar_criterios(e=None):
    borrar_filas(zona_crit)
    if var_crit_tipo.get() == "":
        return
    posicion = 0
    for c in criterios:
        if str(c[7]) == sacar_id(var_crit_tipo.get()) and posicion < 4:
            fila_criterio(32 * posicion, c)
            posicion = posicion + 1


cb_crit_tipo.bind("<<ComboboxSelected>>", cargar_criterios)


caja = crear_caja(p_tipos, 32, 704, 976, 108)
titulo_caja(caja, "Criterio para el tipo de ensayo elegido arriba")
etiqueta_campo(caja, "Nombre", 21, 40)
cuadro_texto(caja, var_crit_nombre, 21, 60, 230)
etiqueta_campo(caja, "Parámetro", 265, 40)
cuadro_texto(caja, var_crit_parametro, 265, 60, 200)
etiqueta_campo(caja, "Límite mínimo", 479, 40)
cuadro_texto(caja, var_crit_min, 479, 60, 120)
etiqueta_campo(caja, "Límite máximo", 613, 40)
cuadro_texto(caja, var_crit_max, 613, 60, 120)


def limpiar_criterio():
    var_crit_id.set("")
    var_crit_nombre.set("")
    var_crit_parametro.set("")
    var_crit_min.set("")
    var_crit_max.set("")


def guardar_criterio():
    if var_crit_tipo.get() == "":
        messagebox.showwarning("Faltan datos", "Elegí primero el tipo de ensayo")
    elif var_crit_nombre.get() == "" or var_crit_parametro.get() == "":
        messagebox.showwarning("Faltan datos", "Completá el nombre y el parámetro")
    else:
        minimo = a_numero(var_crit_min.get())
        maximo = a_numero(var_crit_max.get())
        if minimo == None or maximo == None:
            messagebox.showwarning("Dato incorrecto", "Los límites tienen que ser números (ej: 6.5)")
        elif minimo > maximo:
            messagebox.showwarning("Dato incorrecto", "El límite mínimo no puede ser mayor que el máximo")
        else:
            limites = "%.2f a %.2f" % (minimo, maximo)
            datos = (var_crit_nombre.get(), var_crit_parametro.get(), limites, "Valor entre minimo y maximo",
                     minimo, maximo, int(sacar_id(var_crit_tipo.get())))
            if var_crit_id.get() == "":
                sql = ("INSERT INTO criterios_acep (nombre, parametros, limites, condiciones, limite_min, limite_max, id_tipo) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            else:
                sql = ("UPDATE criterios_acep SET nombre = %s, parametros = %s, limites = %s, condiciones = %s, "
                       "limite_min = %s, limite_max = %s, id_tipo = %s WHERE id_criterio = %s")
                datos = datos + (int(var_crit_id.get()),)
            if ejecutar(sql, datos):
                messagebox.showinfo("Listo", "Criterio guardado")
                limpiar_criterio()
                recargar_datos()
                cargar_criterios()


boton_verde(caja, "Guardar criterio", 747, 58, 130, guardar_criterio)
boton_blanco(caja, "Limpiar", 887, 58, 70, limpiar_criterio)


p_ensayos = tk.Frame(ventana, bg=FONDO, width=1040, height=820)
p_ensayos.place(x=3000, y=0)


titulo_pantalla(p_ensayos, "Inicio › Registro de ensayos", "Registro de ensayos y sus mediciones",
                "Elegí el lote, la muestra y el tipo de ensayo; después cargá los valores medidos.")


var_ens_lote = tk.StringVar()
var_ens_muestra = tk.StringVar()
var_ens_tipo = tk.StringVar()
var_ens_fecha = tk.StringVar()
var_ens_responsable = tk.StringVar()
var_ens_estado = tk.StringVar(value="Pendiente")
var_ens_id = tk.StringVar()


# ---------- Datos del ensayo ----------
caja = crear_caja(p_ensayos, 32, 110, 976, 125)
titulo_caja(caja, "Datos del ensayo")
etiqueta_campo(caja, "Lote", 15, 40)
cb_ens_lote = lista_desplegable(caja, var_ens_lote, lista_lotes, 15, 60, 230)
etiqueta_campo(caja, "Muestra", 257, 40)
cb_ens_muestra = lista_desplegable(caja, var_ens_muestra, lista_muestras, 257, 60, 140)
etiqueta_campo(caja, "Tipo de ensayo", 409, 40)
cb_ens_tipo = lista_desplegable(caja, var_ens_tipo, lista_tipos, 409, 60, 150)
etiqueta_campo(caja, "Fecha (AAAA-MM-DD)", 521, 40)
cuadro_texto(caja, var_ens_fecha, 521, 60, 130)
etiqueta_campo(caja, "Responsable", 663, 40)
cuadro_texto(caja, var_ens_responsable, 663, 60, 150)
etiqueta_campo(caja, "Estado", 825, 40)
lista_desplegable(caja, var_ens_estado, ["Pendiente", "Completado"], 825, 60, 130)


def cargar_muestras_del_lote():
    lista_muestras.clear()
    if var_ens_lote.get() != "":
        for m in muestras:
            if str(m[3]) == sacar_id(var_ens_lote.get()):
                lista_muestras.append(str(m[0]) + " - Muestra " + str(m[1]))
    cb_ens_muestra.config(values=lista_muestras)


def elegir_lote_ensayo(e=None):
    cargar_muestras_del_lote()
    var_ens_muestra.set("")


cb_ens_lote.bind("<<ComboboxSelected>>", elegir_lote_ensayo)


caja_med = crear_caja(p_ensayos, 32, 245, 976, 318)
titulo_caja(caja_med, "Mediciones del ensayo")
nota_caja(caja_med, "El resultado se calcula solo: se compara cada valor con el criterio de aceptación del tipo de ensayo.", 21, 38)
cabecera_tabla(caja_med, 62,
               ["Parámetro", "Valor obtenido", "Unidad", "Criterio de aceptación", "Resultado"],
               [33, 214, 340, 450, 640], 954)
zona_med = zona_tabla(caja_med, 98, 165)


med_parametro = []
med_valor = []     
med_unidad = []   
med_minimo = []
med_maximo = []
med_resultado = []   


def unidad_sugerida(parametro):
    if parametro == "pH":
        return "pH"
    elif parametro == "Densidad":
        return "g/ml"
    elif parametro == "Temperatura":
        return "C"
    elif parametro == "Actividad de agua":
        return "aw"
    else:
        return "%"


def vaciar_mediciones():
    borrar_filas(zona_med)
    med_parametro.clear()
    med_valor.clear()
    med_unidad.clear()
    med_minimo.clear()
    med_maximo.clear()
    med_resultado.clear()


def fila_medicion(ry, criterio):
    parametro = criterio[2]
    minimo = float(criterio[5])
    maximo = float(criterio[6])
    var_valor = tk.StringVar()
    var_unidad = tk.StringVar(value=unidad_sugerida(parametro))


    tk.Label(zona_med, text=parametro, bg="white").place(x=33, y=ry + 10)
    cuadro_texto(zona_med, var_valor, 214, ry + 3, 110)
    cuadro_texto(zona_med, var_unidad, 340, ry + 3, 80)
    tk.Label(zona_med, text="entre " + str(minimo) + " y " + str(maximo),
             bg="white").place(x=450, y=ry + 10)
    etiqueta = etiqueta_estado(zona_med, "Pendiente", 640, ry + 9)
    linea(zona_med, ry + 39, 954)


    med_parametro.append(parametro)
    med_valor.append(var_valor)
    med_unidad.append(var_unidad)
    med_minimo.append(minimo)
    med_maximo.append(maximo)
    med_resultado.append(etiqueta)


def cargar_mediciones(e=None):
    vaciar_mediciones()
    if var_ens_tipo.get() == "":
        return
    posicion = 0
    for c in criterios:
        if str(c[7]) == sacar_id(var_ens_tipo.get()) and posicion < 4:
            fila_medicion(40 * posicion, c)
            posicion = posicion + 1


cb_ens_tipo.bind("<<ComboboxSelected>>", cargar_mediciones)

def calcular_todo():
    if len(med_valor) == 0:
        messagebox.showwarning("Faltan datos", "Elegí un tipo de ensayo que tenga criterios cargados")
        return False
    todo_bien = True
    for i in range(len(med_valor)):
        numero = a_numero(med_valor[i].get())
        if numero == None:
            todo_bien = False
            pintar_estado(med_resultado[i], "Pendiente")
        elif numero >= med_minimo[i] and numero <= med_maximo[i]:
            pintar_estado(med_resultado[i], "Satisfactorio")
        else:
            pintar_estado(med_resultado[i], "No satisfactorio")
    if not todo_bien:
        messagebox.showwarning("Dato incorrecto", "Escribí un número en cada valor obtenido (ej: 6.5)")
    return todo_bien


def limpiar_ensayo():
    var_ens_id.set("")
    var_ens_lote.set("")
    var_ens_muestra.set("")
    var_ens_tipo.set("")
    var_ens_fecha.set("")
    var_ens_responsable.set("")
    var_ens_estado.set("Pendiente")
    lista_muestras.clear()
    cb_ens_muestra.config(values=lista_muestras)
    vaciar_mediciones()


def guardar_ensayo_nuevo():
    id_existente = 0
    if var_ens_id.get() != "":
        id_existente = int(var_ens_id.get())
    base = ("UPDATE mediciones INNER JOIN ensayos ON mediciones.id_ensayo = ensayos.id_ensayo "
            "INNER JOIN criterios_acep ON criterios_acep.id_tipo = ensayos.id_tipo "
            "AND criterios_acep.parametros = mediciones.parametro ")
    sql_cumple = (base + "SET mediciones.resultado = 'Satisfactorio' "
                  "WHERE mediciones.id_ensayo = %s "
                  "AND mediciones.valor >= criterios_acep.limite_min "
                  "AND mediciones.valor <= criterios_acep.limite_max")
    sql_no_cumple = (base + "SET mediciones.resultado = 'No satisfactorio' "
                     "WHERE mediciones.id_ensayo = %s "
                     "AND (mediciones.valor < criterios_acep.limite_min "
                     "OR mediciones.valor > criterios_acep.limite_max)")
    try:
        conexion = conectar()
        try:
            cursor = conexion.cursor()
            if id_existente == 0:
                sql = ("INSERT INTO ensayos (responsable, fecha, estado, id_muestra, id_tipo) "
                       "VALUES (%s, %s, 'Pendiente', %s, %s)")
                datos = (var_ens_responsable.get(), var_ens_fecha.get(),
                         int(sacar_id(var_ens_muestra.get())), int(sacar_id(var_ens_tipo.get())))
                cursor.execute(sql, datos)
                id_ensayo = cursor.lastrowid
            else:
                sql = ("UPDATE ensayos SET responsable = %s, fecha = %s, id_muestra = %s, id_tipo = %s "
                       "WHERE id_ensayo = %s")
                datos = (var_ens_responsable.get(), var_ens_fecha.get(),
                         int(sacar_id(var_ens_muestra.get())), int(sacar_id(var_ens_tipo.get())), id_existente)
                cursor.execute(sql, datos)
                id_ensayo = id_existente
            sql = ("INSERT INTO mediciones (parametro, valor, unidad_m, resultado, id_ensayo) "
                   "VALUES (%s, %s, %s, 'Pendiente', %s)")
            for i in range(len(med_valor)):
                datos = (med_parametro[i], a_numero(med_valor[i].get()), med_unidad[i].get(), id_ensayo)
                cursor.execute(sql, datos)
            cursor.execute(sql_cumple, (id_ensayo,))
            cursor.execute(sql_no_cumple, (id_ensayo,))
            cursor.execute("UPDATE ensayos SET estado = 'Completado' WHERE id_ensayo = %s", (id_ensayo,))
            conexion.commit()
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    except mysql.connector.Error as error:
        messagebox.showerror("Error de base de datos", str(error))
        return
    resumen = ""
    for i in range(len(med_valor)):
        resumen = resumen + med_parametro[i] + ": " + med_valor[i].get() + " " + med_unidad[i].get() + "  →  " + med_resultado[i]["text"] + "\n"
    messagebox.showinfo("Ensayo guardado", resumen)
    limpiar_ensayo()
    recargar_datos()
    cargar_ensayos()


def guardar_ensayo():
    if (var_ens_muestra.get() == "" or var_ens_tipo.get() == "" or var_ens_fecha.get() == ""
            or var_ens_responsable.get() == ""):
        messagebox.showwarning("Faltan datos", "Completá lote, muestra, tipo de ensayo, fecha y responsable")
    elif not fecha_ok(var_ens_fecha.get()):
        messagebox.showwarning("Fecha incorrecta", "Escribí la fecha así: AAAA-MM-DD (ej: 2026-05-20)")
    elif var_ens_id.get() != "" and len(med_valor) == 0:
        # Se está editando un ensayo que ya tiene sus mediciones: solo se modifican sus datos
        datos = (var_ens_responsable.get(), var_ens_fecha.get(), var_ens_estado.get(),
                 int(sacar_id(var_ens_muestra.get())), int(sacar_id(var_ens_tipo.get())), int(var_ens_id.get()))
        sql = ("UPDATE ensayos SET responsable = %s, fecha = %s, estado = %s, id_muestra = %s, id_tipo = %s "
               "WHERE id_ensayo = %s")
        if ejecutar(sql, datos):
            messagebox.showinfo("Listo", "Ensayo modificado")
            limpiar_ensayo()
            recargar_datos()
            cargar_ensayos()
    elif calcular_todo():
        guardar_ensayo_nuevo()


boton_blanco(caja_med, "Calcular resultado", 21, 272, 170, calcular_todo)
boton_verde(caja_med, "Guardar ensayo", 205, 272, 150, guardar_ensayo)
boton_blanco(caja_med, "Limpiar", 369, 272, 100, limpiar_ensayo)


caja_ens = crear_caja(p_ensayos, 32, 573, 976, 240)
titulo_caja(caja_ens, "Ensayos registrados (últimos 5)")
cabecera_tabla(caja_ens, 44,
               ["N°", "Muestra", "Tipo de ensayo", "Fecha", "Responsable", "Estado", "Acciones"],
               [33, 110, 215, 360, 460, 600, 730], 954)
zona_ens = zona_tabla(caja_ens, 80, 155)


def fila_ensayo(ry, dato):
    muestra = buscar(muestras, dato[4])
    tipo = buscar(tipos, dato[5])
    fila_texto(zona_ens, ry + 6, [str(dato[0]), str(muestra[1]), tipo[1], dato[2], txt(dato[1], 18)],
               [33, 110, 215, 360, 460])
    etiqueta_estado(zona_ens, dato[3], 600, ry + 5)


    def ver_mediciones():
        texto = ""
        for m in mediciones:
            if m[5] == dato[0]:
                texto = texto + m[1] + ": " + str(m[2]) + " " + m[3] + "  →  " + m[4] + "\n"
        if texto == "":
            texto = "Este ensayo todavía no tiene mediciones"
        messagebox.showinfo("Mediciones del ensayo " + str(dato[0]), texto)


    def editar():
        var_ens_id.set(str(dato[0]))
        var_ens_lote.set(buscar_texto(lista_lotes, muestra[3]))
        cargar_muestras_del_lote()
        var_ens_muestra.set(buscar_texto(lista_muestras, muestra[0]))
        var_ens_tipo.set(buscar_texto(lista_tipos, tipo[0]))
        var_ens_fecha.set(dato[2])
        var_ens_responsable.set(dato[1])
        var_ens_estado.set(dato[3])
        vaciar_mediciones()
        tiene = False
        for m in mediciones:
            if m[5] == dato[0]:
                tiene = True
        if not tiene:
            cargar_mediciones()


    def borrar():
        if eliminar_ensayo(dato[0]):
            recargar_datos()
            cargar_ensayos()


    boton_ver = tk.Button(zona_ens, text="Ver", bg="white", fg=VERDE,
                          font=("Arial", 9, "bold"), relief="solid", bd=1,
                          command=ver_mediciones)
    boton_ver.place(x=730, y=ry + 1, width=50, height=28)
    botones_fila(zona_ens, 786, ry + 1, "el ensayo " + str(dato[0]) + " y sus mediciones", editar, borrar)
    linea(zona_ens, ry + 29, 954)


def cargar_ensayos():
    borrar_filas(zona_ens)
    filas = ultimos(ensayos, 5)
    for i in range(len(filas)):
        fila_ensayo(30 * i, filas[i])


var_fil_producto = tk.StringVar(value="Todos")
var_fil_lote = tk.StringVar(value="Todos")
var_fil_resultado = tk.StringVar(value="Todos")
var_fil_desde = tk.StringVar()
var_fil_hasta = tk.StringVar()


caja = crear_caja(p_inicio, 32, 290, 976, 105)
titulo_caja(caja, "Consulta de resultados")
nota_caja(caja, "Las fechas se escriben así: AAAA-MM-DD (ej: 2026-03-15). Si las dejás vacías no se filtra por fecha.", 210, 15)
etiqueta_campo(caja, "Producto", 21, 42)
cb_fil_producto = lista_desplegable(caja, var_fil_producto, ["Todos"], 21, 62, 170)
etiqueta_campo(caja, "Lote", 203, 42)
cb_fil_lote = lista_desplegable(caja, var_fil_lote, ["Todos"], 203, 62, 230)
etiqueta_campo(caja, "Resultado", 445, 42)
lista_desplegable(caja, var_fil_resultado, ["Todos", "Satisfactorio", "No satisfactorio"], 445, 62, 150)
etiqueta_campo(caja, "Desde", 607, 42)
cuadro_texto(caja, var_fil_desde, 607, 62, 105)
etiqueta_campo(caja, "Hasta", 724, 42)
cuadro_texto(caja, var_fil_hasta, 724, 62, 105)


caja_res = crear_caja(p_inicio, 32, 405, 976, 405)
titulo_caja(caja_res, "Resultados encontrados")
lbl_cantidad = tk.Label(caja_res, text="", bg="white", fg="#666", font=("Arial", 9))
lbl_cantidad.place(x=640, y=16)
cabecera_tabla(caja_res, 44,
               ["Producto", "Lote", "Ensayo", "Parámetro", "Valor", "Unidad", "Criterio", "Resultado", "Fecha"],
               [33, 165, 235, 345, 475, 535, 610, 740, 880], 954)
zona_res = zona_tabla(caja_res, 80, 320)


def fila_resultado(ry, dato):
    fila_texto(zona_res, ry + 9,
               [txt(dato[2], 18), str(dato[3]), txt(dato[4], 13), txt(dato[5], 18), str(dato[6]), dato[7], txt(dato[8], 15)],
               [33, 165, 235, 345, 475, 535, 610])
    etiqueta_estado(zona_res, dato[9], 740, ry + 9)
    fila_texto(zona_res, ry + 9, [dato[0]], [880])
    linea(zona_res, ry + 37, 954)


def buscar_resultados():
    if var_fil_desde.get() != "" and not fecha_ok(var_fil_desde.get()):
        messagebox.showwarning("Fecha incorrecta", "En 'Desde' escribí la fecha así: AAAA-MM-DD")
        return
    if var_fil_hasta.get() != "" and not fecha_ok(var_fil_hasta.get()):
        messagebox.showwarning("Fecha incorrecta", "En 'Hasta' escribí la fecha así: AAAA-MM-DD")
        return

    encontrados = []
    for m in mediciones:
        ensayo = buscar(ensayos, m[5])
        muestra = buscar(muestras, ensayo[4])
        lote = buscar(lotes, muestra[3])
        producto = buscar(productos, lote[3])
        tipo = buscar(tipos, ensayo[5])


        mostrar_fila = True
        if var_fil_producto.get() != "Todos" and var_fil_producto.get() != "":
            if str(producto[0]) != sacar_id(var_fil_producto.get()):
                mostrar_fila = False
        if var_fil_lote.get() != "Todos" and var_fil_lote.get() != "":
            if str(lote[0]) != sacar_id(var_fil_lote.get()):
                mostrar_fila = False
        if var_fil_resultado.get() != "Todos" and var_fil_resultado.get() != "":
            if m[4] != var_fil_resultado.get():
                mostrar_fila = False
        if var_fil_desde.get() != "" and ensayo[2] < var_fil_desde.get():
            mostrar_fila = False
        if var_fil_hasta.get() != "" and ensayo[2] > var_fil_hasta.get():
            mostrar_fila = False


        if mostrar_fila:
            limites = ""
            for c in criterios:
                if c[7] == ensayo[5] and c[2] == m[1]:
                    limites = c[3]
            encontrados.append([ensayo[2], m[0], producto[1], lote[1], tipo[1], m[1], m[2], m[3], limites, m[4]])


    encontrados.sort(reverse=True)   
    borrar_filas(zona_res)
    for i in range(len(encontrados)):
        if i < 8:
            fila_resultado(38 * i, encontrados[i])
    lbl_cantidad.config(text="Encontrados: " + str(len(encontrados)) + "  ·  se muestran hasta 8")


def limpiar_filtros():
    var_fil_producto.set("Todos")
    var_fil_lote.set("Todos")
    var_fil_resultado.set("Todos")
    var_fil_desde.set("")
    var_fil_hasta.set("")
    buscar_resultados()


boton_verde(caja, "Buscar", 841, 60, 100, buscar_resultados)
boton_blanco(caja, "Limpiar", 841, 14, 100, limpiar_filtros)


p_certificados = tk.Frame(ventana, bg=FONDO, width=1040, height=820)
p_certificados.place(x=3000, y=0)


titulo_pantalla(p_certificados, "Inicio › Certificados", "Gestión y consulta de certificados",
                "Un lote solo recibe certificado si completó sus ensayos y no tiene resultados no satisfactorios. Vale con la firma del director.")


var_cert_lote = tk.StringVar()
var_cert_director = tk.StringVar()
var_cert_fecha = tk.StringVar()

caja_emit = crear_caja(p_certificados, 32, 110, 976, 186)
titulo_caja(caja_emit, "Certificados emitidos (últimos 3)")
cabecera_tabla(caja_emit, 44,
               ["N° certificado", "Producto", "Lote", "Fecha de emisión", "Director", "Firma", "Acciones"],
               [33, 154, 275, 395, 516, 700, 800], 954)
zona_emit = zona_tabla(caja_emit, 80, 100)


def fila_certificado(ry, dato):
    # dato = [id_certificado, fecha_emision, id_lote, id_director]
    lote = buscar(lotes, dato[2])
    producto = buscar(productos, lote[3])
    director = buscar(directores, dato[3])
    fila_texto(zona_emit, ry + 6,
               [str(dato[0]), txt(producto[1], 18), str(lote[1]), dato[1][0:10], director[1] + " " + director[2]],
               [33, 154, 275, 395, 516])
    if director[4] == 1:
        etiqueta_estado(zona_emit, "Firmado", 700, ry + 5)
    else:
        etiqueta_estado(zona_emit, "Sin firma", 700, ry + 5)


    def ver_certificado():
        texto = ("Certificado N° " + str(dato[0]) + "\nProducto: " + producto[1] + "\nLote: " + str(lote[1])
                 + "\nFecha de emisión: " + dato[1][0:10] + "\nDirector: " + director[1] + " " + director[2])
        if director[4] == 1:
            texto = texto + "\nFirma: Firmado por el director"
        else:
            texto = texto + "\nFirma: SIN FIRMA (el certificado no es válido sin la firma del director)"
        messagebox.showinfo("Certificado", texto)


    def borrar():
        if eliminar_registro("certific_calidad", "id_certificado", dato[0]):
            recargar_datos()
            cargar_certificados()


    def pedir_borrar():
        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que querés eliminar el certificado " + str(dato[0]) + "?")
        if respuesta:
            borrar()


    boton_ver = tk.Button(zona_emit, text="Ver", bg="white", fg=VERDE,
                          font=("Arial", 9, "bold"), relief="solid", bd=1,
                          command=ver_certificado)
    boton_ver.place(x=800, y=ry + 1, width=55, height=28)
    boton_eliminar = tk.Button(zona_emit, text="Eliminar", bg="white", fg="#b03030",
                               font=("Arial", 9, "bold"), relief="solid", bd=1,
                               command=pedir_borrar)
    boton_eliminar.place(x=861, y=ry + 1, width=76, height=28)
    linea(zona_emit, ry + 31, 954)


# ---------- Control previo por lote ----------
caja_ctrl = crear_caja(p_certificados, 32, 306, 976, 340)
titulo_caja(caja_ctrl, "Control previo por lote (primeros 8)")
nota_caja(caja_ctrl, "Apto = tiene ensayos, todos están Completados y ninguna medición es no satisfactoria.", 21, 34)
cabecera_tabla(caja_ctrl, 56,
               ["Lote", "Producto", "Ensayos", "Resultados", "Estado", "Acciones"],
               [33, 178, 322, 468, 650, 790], 954)
zona_ctrl = zona_tabla(caja_ctrl, 90, 245)

def estado_del_lote(id_lote):
    cantidad = 0
    pendientes = 0
    no_satisfactorias = 0
    for e in ensayos:
        muestra = buscar(muestras, e[4])
        if muestra[3] == id_lote:
            cantidad = cantidad + 1
            if e[3] != "Completado":
                pendientes = pendientes + 1
            for m in mediciones:
                if m[5] == e[0] and m[4] == "No satisfactorio":
                    no_satisfactorias = no_satisfactorias + 1
    con_certificado = 0
    for c in certificados:
        if c[2] == id_lote:
            con_certificado = con_certificado + 1


    if cantidad == 0:
        resultados = "Sin ensayos"
        estado = "Incompleto"
    elif pendientes > 0:
        resultados = str(pendientes) + " ensayo(s) pendiente(s)"
        estado = "Incompleto"
    elif no_satisfactorias > 0:
        resultados = str(no_satisfactorias) + " no satisfactoria(s)"
        estado = "No apto"
    else:
        resultados = "Todos satisfactorios"
        estado = "Apto"
    if con_certificado > 0 and estado == "Apto":
        estado = "Certificado emitido"
    return [cantidad, resultados, estado]


def fila_control(ry, dato):
    producto = buscar(productos, dato[3])
    datos_lote = estado_del_lote(dato[0])
    fila_texto(zona_ctrl, ry + 7,
               [str(dato[1]), txt(producto[1], 20), str(datos_lote[0]), datos_lote[1]],
               [33, 178, 322, 468])
    etiqueta_estado(zona_ctrl, datos_lote[2], 650, ry + 6)


    def preparar_certificado():
        var_cert_lote.set(texto_lote(dato[0], dato[1], producto[1]))

    if datos_lote[2] == "Apto":
        lista_aptos.append(texto_lote(dato[0], dato[1], producto[1]))
        boton = tk.Button(zona_ctrl, text="Generar certificado", bg="white", fg=VERDE,
                          font=("Arial", 9, "bold"), relief="solid", bd=1,
                          command=preparar_certificado)
    elif datos_lote[2] == "Certificado emitido":
        boton = tk.Button(zona_ctrl, text="Ya emitido", font=("Arial", 9, "bold"),
                          state=tk.DISABLED)
    else:
        boton = tk.Button(zona_ctrl, text="Generar certificado", font=("Arial", 9, "bold"),
                          state=tk.DISABLED)
    boton.place(x=790, y=ry + 1, width=150, height=28)
    linea(zona_ctrl, ry + 29, 954)

caja = crear_caja(p_certificados, 32, 656, 976, 150)
titulo_caja(caja, "Generar certificado")
etiqueta_campo(caja, "Lote (solo lotes aptos)", 21, 42)
cb_cert_lote = lista_desplegable(caja, var_cert_lote, lista_aptos, 21, 62, 302)
etiqueta_campo(caja, "Director de laboratorio", 337, 42)
cb_cert_director = lista_desplegable(caja, var_cert_director, lista_directores, 337, 62, 302)
etiqueta_campo(caja, "Fecha de emisión (AAAA-MM-DD)", 653, 42)
cuadro_texto(caja, var_cert_fecha, 653, 62, 302)


def limpiar_certificado():
    var_cert_lote.set("")
    var_cert_director.set("")
    var_cert_fecha.set("")


def generar_certificado():
    if var_cert_lote.get() == "" or var_cert_director.get() == "" or var_cert_fecha.get() == "":
        messagebox.showwarning("Faltan datos", "Elegí el lote, el director y escribí la fecha")
    elif not fecha_ok(var_cert_fecha.get()):
        messagebox.showwarning("Fecha incorrecta", "Escribí la fecha así: AAAA-MM-DD (ej: 2026-05-20)")
    elif "sin firma" in var_cert_director.get():
        messagebox.showwarning("Director sin firma",
                               "Este director no tiene la firma habilitada, así que no puede firmar certificados.")
    else:
        sql = "INSERT INTO certific_calidad (fecha_emision, id_lote, id_director) VALUES (%s, %s, %s)"
        datos = (var_cert_fecha.get(), int(sacar_id(var_cert_lote.get())), int(sacar_id(var_cert_director.get())))
        if ejecutar(sql, datos):
            messagebox.showinfo("Listo", "Certificado generado")
            limpiar_certificado()
            recargar_datos()
            cargar_certificados()


boton_verde(caja, "Generar certificado", 21, 110, 170, generar_certificado)
boton_blanco(caja, "Limpiar", 205, 110, 100, limpiar_certificado)


def cargar_certificados():
    borrar_filas(zona_emit)
    filas = ultimos(certificados, 3)
    for i in range(len(filas)):
        fila_certificado(32 * i, filas[i])


    # Control previo por lote
    borrar_filas(zona_ctrl)
    lista_aptos.clear()
    for i in range(len(lotes)):
        if i < 8:
            fila_control(30 * i, lotes[i])
    cb_cert_lote.config(values=lista_aptos)

p_directores = tk.Frame(ventana, bg=FONDO, width=1040, height=820)
p_directores.place(x=3000, y=0)


titulo_pantalla(p_directores, "Inicio › Directores de laboratorio", "Directores de laboratorio",
                "Son quienes firman los certificados de calidad.")


var_dir_id = tk.StringVar()
var_dir_nombre = tk.StringVar()
var_dir_apellido = tk.StringVar()
var_dir_dni = tk.StringVar()
var_dir_firma = tk.StringVar()


caja = crear_caja(p_directores, 32, 110, 976, 165)
titulo_caja(caja, "Director")
etiqueta_campo(caja, "Nombre", 21, 46)
cuadro_texto(caja, var_dir_nombre, 21, 68, 220)
etiqueta_campo(caja, "Apellido", 255, 46)
cuadro_texto(caja, var_dir_apellido, 255, 68, 220)
etiqueta_campo(caja, "DNI (solo números)", 489, 46)
cuadro_texto(caja, var_dir_dni, 489, 68, 220)
etiqueta_campo(caja, "Firma", 723, 46)
lista_desplegable(caja, var_dir_firma, ["Con firma", "Sin firma"], 723, 68, 232)


def limpiar_director():
    var_dir_id.set("")
    var_dir_nombre.set("")
    var_dir_apellido.set("")
    var_dir_dni.set("")
    var_dir_firma.set("")


def guardar_director():
    if (var_dir_nombre.get() == "" or var_dir_apellido.get() == "" or var_dir_dni.get() == ""
            or var_dir_firma.get() == ""):
        messagebox.showwarning("Faltan datos", "Completá todos los campos")
    elif not var_dir_dni.get().isdigit():
        messagebox.showwarning("Dato incorrecto", "El DNI tiene que ser un número (sin puntos)")
    else:
        firma = 0
        if var_dir_firma.get() == "Con firma":
            firma = 1
        datos = (var_dir_nombre.get(), var_dir_apellido.get(), int(var_dir_dni.get()), firma)
        if var_dir_id.get() == "":
            sql = "INSERT INTO directores_lab (nombre, apellido, dni, firma) VALUES (%s, %s, %s, %s)"
        else:
            sql = "UPDATE directores_lab SET nombre = %s, apellido = %s, dni = %s, firma = %s WHERE id_director = %s"
            datos = datos + (int(var_dir_id.get()),)
        if ejecutar(sql, datos):
            messagebox.showinfo("Listo", "Director guardado")
            limpiar_director()
            recargar_datos()
            cargar_directores()


boton_verde(caja, "Guardar director", 21, 114, 160, guardar_director)
boton_blanco(caja, "Limpiar", 195, 114, 100, limpiar_director)


caja_dir = crear_caja(p_directores, 32, 290, 976, 400)
titulo_caja(caja_dir, "Directores registrados (últimos 8)")
cabecera_tabla(caja_dir, 46, ["ID", "Nombre", "Apellido", "DNI", "Firma", "Acciones"],
               [33, 110, 290, 470, 640, 757], 954)
zona_dir = zona_tabla(caja_dir, 84, 310)


def fila_director(ry, dato):
    fila_texto(zona_dir, ry + 10, [str(dato[0]), dato[1], dato[2], str(dato[3])], [33, 110, 290, 470])
    if dato[4] == 1:
        etiqueta_estado(zona_dir, "Firmado", 640, ry + 9)
    else:
        etiqueta_estado(zona_dir, "Sin firma", 640, ry + 9)


    def editar():
        var_dir_id.set(str(dato[0]))
        var_dir_nombre.set(dato[1])
        var_dir_apellido.set(dato[2])
        var_dir_dni.set(str(dato[3]))
        if dato[4] == 1:
            var_dir_firma.set("Con firma")
        else:
            var_dir_firma.set("Sin firma")


    def borrar():
        if eliminar_registro("directores_lab", "id_director", dato[0]):
            recargar_datos()
            cargar_directores()


    botones_fila(zona_dir, 757, ry + 5, "al director " + dato[1] + " " + dato[2], editar, borrar)
    linea(zona_dir, ry + 37, 954)


def cargar_directores():
    borrar_filas(zona_dir)
    filas = ultimos(directores, 8)
    for i in range(len(filas)):
        fila_director(38 * i, filas[i])



ir_inicio()
ventana.mainloop()

