
# Nueva versión: Menú profesional para todos los módulos
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
import os


# Usar rutas absolutas basadas en la ubicación de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULOS = {
    "Evidencias": os.path.join(BASE_DIR, "..", "backend", "modulos", "evidencias", "configuracion", "config.json"),
    "PQR": os.path.join(BASE_DIR, "..", "backend", "modulos", "pqr", "configuracion", "config.json"),
    "Profesional": os.path.join(BASE_DIR, "..", "backend", "modulos", "profesional", "configuracion", "config.json"),
    "Solicitudes": os.path.join(BASE_DIR, "..", "backend", "modulos", "solicitudes", "configuracion", "config.json"),
    "Usuarios": os.path.join(BASE_DIR, "..", "backend", "modulos", "usuarios", "configuracion", "config.json")
}

MODULOS_CAMPOS = {
    "Evidencias": ["id_evidencia", "id_solicitud", "id_usuario", "id_profesional", "tipo_actor", "archivo_contenido", "descripcion", "estado", "fecha_subida" ],
    "PQR": ["id_pqrs", "id_solicitud", "id_usuario", "id_profesional", "tipo", "descripcion", "estado", "fecha_creacion"],
    "Profesional": ["id_profesional", "nombre", "apellido", "correo", "telefono", "contrasena", "profesion", "habilidades", "zona_trabajo"],
    "Solicitudes": ["id_solicitud", "id_usuario", "id_profesional", "id_servicio", "descripcion", "direccion_servicio", "telefono_contacto", "fecha_servicio", "hora_servicio", "presupuesto", "estado", "fecha_creacion"],
    "Usuarios": ["id_usuario", "nombre", "apellido", "correo", "telefono", "direccion", "contrasena", "fecha_registro"]
}

class ModuloCRUD:
    def __init__(self, root, modulo):
        self.root = root
        self.modulo = modulo
        self.config = self.cargar_configuracion()
        self.api = self.config["api_base"]
        self.endpoints = self.config["endpoints"]
        self.campos = MODULOS_CAMPOS[modulo]
        self.frame = tk.Frame(root)
        self.crear_interfaz()

    def cargar_configuracion(self):
        with open(MODULOS[self.modulo], encoding="utf-8") as f:
            return json.load(f)

    def crear_interfaz(self):
        self.frame.pack(fill="both", expand=True)
        cols = tuple(self.campos)
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        botonera = tk.Frame(self.frame)
        botonera.pack(pady=10)
        tk.Button(botonera, text="Registrar", command=self.crear_registro).pack(side="left", padx=5)
        tk.Button(botonera, text="Actualizar", command=self.editar_registro).pack(side="left", padx=5)
        tk.Button(botonera, text="Eliminar", command=self.eliminar_registro).pack(side="left", padx=5)
        tk.Button(botonera, text="Buscar por ID", command=self.buscar_por_id).pack(side="left", padx=5)
        tk.Button(botonera, text="Recargar", command=self.recargar_datos).pack(side="left", padx=5)
        self.recargar_datos()

    def limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def recargar_datos(self):
        self.limpiar_tabla()
        try:
            r = requests.get(self.api + self.endpoints["read_all"])
            if r.status_code == 200:
                for p in r.json():
                    fila = tuple(p.get(c, "") for c in self.campos)
                    self.tree.insert("", "end", values=fila)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def crear_registro(self):
        self.dialogo_registro("Registrar nuevo")

    def editar_registro(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Seleccionar", "Seleccione un registro.")
            return
        valores = self.tree.item(seleccionado, "values")
        self.dialogo_registro("Actualizar registro", valores)

    def eliminar_registro(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Seleccionar", "Seleccione un registro.")
            return
        id_reg = self.tree.item(seleccionado, "values")[0]
        if messagebox.askyesno("Eliminar", "¿Seguro que desea eliminar este registro?"):
            try:
                r = requests.delete(self.api + self.endpoints["delete"].replace("{id}", str(id_reg)))
                if r.status_code == 200:
                    self.recargar_datos()
                    messagebox.showinfo("Éxito", "Registro eliminado.")
                else:
                    messagebox.showerror("Error", r.text)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def buscar_por_id(self):
        id_buscar = simpledialog.askstring("Buscar por ID", f"Ingrese el ID de {self.modulo.lower()} a buscar:")
        if not id_buscar:
            return
        try:
            r = requests.get(self.api + self.endpoints["read_one"].replace("{id}", str(id_buscar)))
            if r.status_code == 200:
                self.limpiar_tabla()
                p = r.json()
                fila = tuple(p.get(c, "") for c in self.campos)
                self.tree.insert("", "end", values=fila)
            else:
                messagebox.showinfo("Sin resultados", f"No se encontró {self.modulo.lower()} con ID {id_buscar}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def dialogo_registro(self, titulo, datos=None):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo + f" {self.modulo}")
        entradas = {}
        for idx, campo in enumerate(self.campos[1:]):  # omitir id
            tk.Label(ventana, text=f"{campo.capitalize()}:").grid(row=idx, column=0)
            entrada = tk.Entry(ventana)
            entrada.grid(row=idx, column=1)
            entradas[campo] = entrada
        if datos:
            for idx, campo in enumerate(self.campos[1:]):
                entradas[campo].insert(0, datos[idx+1])

        def guardar():
            payload = {campo: entradas[campo].get() for campo in self.campos[1:]}
            try:
                if datos:
                    id_reg = datos[0]
                    r = requests.put(self.api + self.endpoints["update"].replace("{id}", str(id_reg)), json=payload)
                else:
                    r = requests.post(self.api + self.endpoints["create"], json=payload)
                if r.status_code in [200, 201]:
                    self.recargar_datos()
                    ventana.destroy()
                    messagebox.showinfo("Éxito", "Operación exitosa.")
                else:
                    messagebox.showerror("Error", r.text)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar).grid(row=len(self.campos), columnspan=2)

    def ocultar(self):
        self.frame.pack_forget()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Profesional - Gestión de Módulos")
        self.modulo_actual = None
        self.crud_actual = None
        self.menu_modulos()

    def menu_modulos(self):
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(fill="both", expand=True)
        tk.Label(self.frame_menu, text="Seleccione el módulo a gestionar:", font=("Arial", 14)).pack(pady=20)
        for modulo in MODULOS.keys():
            tk.Button(self.frame_menu, text=modulo, width=20, font=("Arial", 12),
                      command=lambda m=modulo: self.seleccionar_modulo(m)).pack(pady=5)

    def seleccionar_modulo(self, modulo):
        if self.crud_actual:
            self.crud_actual.ocultar()
        self.frame_menu.pack_forget()
        self.modulo_actual = modulo
        self.crud_actual = ModuloCRUD(self.root, modulo)
        tk.Button(self.root, text="Volver al menú", command=self.volver_menu).pack(pady=10)

    def volver_menu(self):
        if self.crud_actual:
            self.crud_actual.ocultar()
            self.crud_actual = None
        for widget in self.root.pack_slaves():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Volver al menú":
                widget.pack_forget()
        self.menu_modulos()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
