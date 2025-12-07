"""
Renombrador de Archivos Secuencial
Permite seleccionar archivos de un directorio y renombrarlos secuencialmente
con opciones de prefijo, sufijo, numeración con ceros, etc.
"""

import os
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime


class RenombradorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Renombrador de Archivos Secuencial")
        self.root.geometry("1000x700")
        
        # Variables
        self.directorio_actual = tk.StringVar()
        self.archivos_originales = []
        self.archivos_ordenados = []
        
        # Opciones de renombrado
        self.prefijo = tk.StringVar()
        self.sufijo = tk.StringVar()
        self.numero_inicio = tk.IntVar(value=1)
        self.numero_fin = tk.IntVar(value=100)
        self.ceros = tk.IntVar(value=3)
        self.usar_ceros = tk.BooleanVar(value=True)
        self.orden_aleatorio = tk.BooleanVar(value=False)
        self.convertir_jpeg_jpg = tk.BooleanVar(value=False)
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Frame superior - Selección de directorio
        frame_dir = ttk.Frame(self.root, padding="10")
        frame_dir.pack(fill=tk.X)
        
        ttk.Label(frame_dir, text="Directorio:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(frame_dir, textvariable=self.directorio_actual, width=60).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_dir, text="Seleccionar", command=self.seleccionar_directorio).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_dir, text="Recargar", command=self.recargar).pack(side=tk.LEFT, padx=5)
        
        # Frame principal con dos columnas
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda - Archivos originales
        frame_izq = ttk.Frame(frame_principal)
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(frame_izq, text="Archivos Actuales", font=("Arial", 10, "bold")).pack()
        
        # Treeview con scrollbar para archivos originales
        scroll_izq = ttk.Scrollbar(frame_izq)
        scroll_izq.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_original = ttk.Treeview(frame_izq, yscrollcommand=scroll_izq.set, 
                                          selectmode="extended", height=15)
        self.tree_original["columns"] = ("tamanio", "tipo", "fecha")
        self.tree_original.column("#0", width=300, minwidth=200)
        self.tree_original.column("tamanio", width=80, minwidth=60)
        self.tree_original.column("tipo", width=80, minwidth=60)
        self.tree_original.column("fecha", width=130, minwidth=100)
        
        self.tree_original.heading("#0", text="Nombre", anchor=tk.W)
        self.tree_original.heading("tamanio", text="Tamaño", anchor=tk.W)
        self.tree_original.heading("tipo", text="Tipo", anchor=tk.W)
        self.tree_original.heading("fecha", text="Fecha", anchor=tk.W)
        
        self.tree_original.pack(fill=tk.BOTH, expand=True)
        scroll_izq.config(command=self.tree_original.yview)
        
        # Botones para reordenar
        frame_botones = ttk.Frame(frame_izq)
        frame_botones.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame_botones, text="↑ Subir", command=self.mover_arriba).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="↓ Bajar", command=self.mover_abajo).pack(side=tk.LEFT, padx=2)
        
        # Columna derecha - Vista previa
        frame_der = ttk.Frame(frame_principal)
        frame_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(frame_der, text="Nombres Nuevos (Vista Previa)", font=("Arial", 10, "bold")).pack()
        
        # Treeview con scrollbar para vista previa
        scroll_der = ttk.Scrollbar(frame_der)
        scroll_der.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_preview = ttk.Treeview(frame_der, yscrollcommand=scroll_der.set, 
                                         selectmode="extended", height=15)
        self.tree_preview["columns"] = ("tamanio", "tipo", "fecha")
        self.tree_preview.column("#0", width=300, minwidth=200)
        self.tree_preview.column("tamanio", width=80, minwidth=60)
        self.tree_preview.column("tipo", width=80, minwidth=60)
        self.tree_preview.column("fecha", width=130, minwidth=100)
        
        self.tree_preview.heading("#0", text="Nombre Nuevo", anchor=tk.W)
        self.tree_preview.heading("tamanio", text="Tamaño", anchor=tk.W)
        self.tree_preview.heading("tipo", text="Tipo", anchor=tk.W)
        self.tree_preview.heading("fecha", text="Fecha", anchor=tk.W)
        
        self.tree_preview.pack(fill=tk.BOTH, expand=True)
        scroll_der.config(command=self.tree_preview.yview)
        
        # Configurar colores para vista previa
        self.tree_preview.tag_configure('preview', foreground='blue')
        
        # Frame inferior - Opciones
        frame_opciones = ttk.LabelFrame(self.root, text="Opciones de Renombrado", padding="10")
        frame_opciones.pack(fill=tk.X, padx=10, pady=10)
        
        # Fila 1 - Prefijo y Sufijo
        row1 = ttk.Frame(frame_opciones)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="Prefijo:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row1, textvariable=self.prefijo, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="Sufijo:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row1, textvariable=self.sufijo, width=20).pack(side=tk.LEFT, padx=5)
        
        # Fila 2 - Numeración
        row2 = ttk.Frame(frame_opciones)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Número desde:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(row2, from_=0, to=9999, textvariable=self.numero_inicio, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="hasta:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(row2, from_=0, to=9999, textvariable=self.numero_fin, width=10).pack(side=tk.LEFT, padx=5)
        
        # Fila 3 - Opciones de ceros y orden aleatorio
        row3 = ttk.Frame(frame_opciones)
        row3.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(row3, text="Rellenar con ceros", variable=self.usar_ceros).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row3, text="Cantidad de dígitos:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(row3, from_=1, to=10, textvariable=self.ceros, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Checkbutton(row3, text="Orden aleatorio", variable=self.orden_aleatorio, 
                       command=self.aplicar_orden_aleatorio).pack(side=tk.LEFT, padx=20)
        
        # Fila 4 - Opciones adicionales
        row4 = ttk.Frame(frame_opciones)
        row4.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(row4, text="Convertir .jpeg a .jpg", variable=self.convertir_jpeg_jpg).pack(side=tk.LEFT, padx=5)
        
        # Botón de actualizar vista previa
        ttk.Button(frame_opciones, text="Actualizar Vista Previa", 
                  command=self.actualizar_preview).pack(pady=5)
        
        # Frame botones de acción
        frame_accion = ttk.Frame(self.root, padding="10")
        frame_accion.pack(fill=tk.X)
        
        ttk.Button(frame_accion, text="APLICAR RENOMBRADO", 
                  command=self.aplicar_renombrado, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_accion, text="RECARGAR TODO", 
                  command=self.recargar).pack(side=tk.LEFT, padx=5)
        
        # Configurar estilo
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="green", font=("Arial", 10, "bold"))
        
        # Sincronizar selección entre treeviews
        self.tree_original.bind("<<TreeviewSelect>>", self.sincronizar_seleccion)
        
        # Actualizar preview cuando cambian las opciones
        self.prefijo.trace_add("write", lambda *args: self.actualizar_preview())
        self.sufijo.trace_add("write", lambda *args: self.actualizar_preview())
        self.numero_inicio.trace_add("write", lambda *args: self.actualizar_preview())
        self.usar_ceros.trace_add("write", lambda *args: self.actualizar_preview())
        self.ceros.trace_add("write", lambda *args: self.actualizar_preview())
        self.convertir_jpeg_jpg.trace_add("write", lambda *args: self.actualizar_preview())
        
    def seleccionar_directorio(self):
        """Abre un diálogo para seleccionar el directorio"""
        directorio = filedialog.askdirectory(title="Seleccionar directorio con archivos")
        if directorio:
            self.directorio_actual.set(directorio)
            self.cargar_archivos()
            
    def cargar_archivos(self):
        """Carga los archivos del directorio seleccionado"""
        directorio = self.directorio_actual.get()
        if not directorio or not os.path.isdir(directorio):
            return
            
        try:
            # Obtener todos los archivos (no directorios)
            archivos = [f for f in os.listdir(directorio) 
                       if os.path.isfile(os.path.join(directorio, f))]
            archivos.sort()
            
            self.archivos_originales = archivos.copy()
            self.archivos_ordenados = archivos.copy()
            
            self.actualizar_listbox_original()
            self.actualizar_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivos: {str(e)}")
            
    def actualizar_listbox_original(self):
        """Actualiza el treeview de archivos originales"""
        # Limpiar treeview
        for item in self.tree_original.get_children():
            self.tree_original.delete(item)
        
        directorio = self.directorio_actual.get()
        if not directorio:
            return
        
        # Insertar archivos con información
        for archivo in self.archivos_ordenados:
            ruta_completa = os.path.join(directorio, archivo)
            
            # Obtener información del archivo
            tamanio = os.path.getsize(ruta_completa)
            tamanio_str = self.formatear_tamanio(tamanio)
            
            # Obtener tipo de archivo
            _, extension = os.path.splitext(archivo)
            tipo = extension[1:].upper() if extension else "Archivo"
            
            # Obtener fecha de modificación
            timestamp = os.path.getmtime(ruta_completa)
            fecha = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")
            
            # Insertar en treeview
            self.tree_original.insert("", "end", text=archivo, 
                                     values=(tamanio_str, tipo, fecha))
    
    def formatear_tamanio(self, tamanio_bytes):
        """Formatea el tamaño en bytes a formato legible"""
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if tamanio_bytes < 1024.0:
                return f"{tamanio_bytes:.1f} {unidad}"
            tamanio_bytes /= 1024.0
        return f"{tamanio_bytes:.1f} TB"
            
    def generar_nuevo_nombre(self, indice):
        """Genera el nuevo nombre para un archivo según las opciones"""
        # Obtener el archivo original
        archivo = self.archivos_ordenados[indice]
        nombre, extension = os.path.splitext(archivo)
        
        # Convertir .jpeg a .jpg si está activado
        if self.convertir_jpeg_jpg.get() and extension.lower() == '.jpeg':
            extension = '.jpg'
        
        # Calcular el número
        numero = self.numero_inicio.get() + indice
        
        # Formatear el número con ceros si está activado
        if self.usar_ceros.get():
            numero_str = str(numero).zfill(self.ceros.get())
        else:
            numero_str = str(numero)
        
        # Construir el nuevo nombre
        prefijo = self.prefijo.get()
        sufijo = self.sufijo.get()
        
        nuevo_nombre = f"{prefijo}{numero_str}{sufijo}{extension}"
        
        return nuevo_nombre
        
    def actualizar_preview(self):
        """Actualiza la vista previa de los nuevos nombres"""
        # Limpiar treeview
        for item in self.tree_preview.get_children():
            self.tree_preview.delete(item)
        
        directorio = self.directorio_actual.get()
        if not directorio:
            return
        
        # Insertar vista previa con información
        for i in range(len(self.archivos_ordenados)):
            nuevo_nombre = self.generar_nuevo_nombre(i)
            archivo_original = self.archivos_ordenados[i]
            ruta_completa = os.path.join(directorio, archivo_original)
            
            # Obtener información del archivo original
            tamanio = os.path.getsize(ruta_completa)
            tamanio_str = self.formatear_tamanio(tamanio)
            
            # Obtener tipo de archivo del nuevo nombre
            _, extension = os.path.splitext(nuevo_nombre)
            tipo = extension[1:].upper() if extension else "Archivo"
            
            # Obtener fecha de modificación
            timestamp = os.path.getmtime(ruta_completa)
            fecha = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")
            
            # Insertar en treeview con tag para color
            self.tree_preview.insert("", "end", text=nuevo_nombre, 
                                    values=(tamanio_str, tipo, fecha),
                                    tags=('preview',))
            
    def sincronizar_seleccion(self, event):
        """Sincroniza la selección entre ambos treeviews"""
        seleccion = self.tree_original.selection()
        
        # Limpiar selección en preview
        for item in self.tree_preview.get_children():
            self.tree_preview.selection_remove(item)
        
        # Seleccionar items correspondientes en preview
        if seleccion:
            items_originales = self.tree_original.get_children()
            items_preview = self.tree_preview.get_children()
            
            for item_sel in seleccion:
                idx = items_originales.index(item_sel)
                if idx < len(items_preview):
                    self.tree_preview.selection_add(items_preview[idx])
            
    def mover_arriba(self):
        """Mueve los archivos seleccionados hacia arriba"""
        seleccion = self.tree_original.selection()
        if not seleccion:
            return
        
        items = self.tree_original.get_children()
        indices = [items.index(item) for item in seleccion]
        indices.sort()
        
        if indices[0] == 0:
            return
            
        for idx in indices:
            if idx > 0:
                # Intercambiar en la lista
                self.archivos_ordenados[idx], self.archivos_ordenados[idx-1] = \
                    self.archivos_ordenados[idx-1], self.archivos_ordenados[idx]
                    
        # Actualizar interfaz
        self.actualizar_listbox_original()
        self.actualizar_preview()
        
        # Mantener la selección
        items_nuevos = self.tree_original.get_children()
        for idx in indices:
            if idx > 0:
                self.tree_original.selection_add(items_nuevos[idx-1])
                
    def mover_abajo(self):
        """Mueve los archivos seleccionados hacia abajo"""
        seleccion = self.tree_original.selection()
        if not seleccion:
            return
        
        items = self.tree_original.get_children()
        indices = [items.index(item) for item in seleccion]
        indices.sort()
        
        if indices[-1] == len(self.archivos_ordenados) - 1:
            return
            
        # Procesar en orden inverso para mover correctamente
        for idx in reversed(indices):
            if idx < len(self.archivos_ordenados) - 1:
                # Intercambiar en la lista
                self.archivos_ordenados[idx], self.archivos_ordenados[idx+1] = \
                    self.archivos_ordenados[idx+1], self.archivos_ordenados[idx]
                    
        # Actualizar interfaz
        self.actualizar_listbox_original()
        self.actualizar_preview()
        
        # Mantener la selección
        items_nuevos = self.tree_original.get_children()
        for idx in indices:
            if idx < len(self.archivos_ordenados) - 1:
                self.tree_original.selection_add(items_nuevos[idx+1])
                
    def aplicar_orden_aleatorio(self):
        """Reordena los archivos de forma aleatoria"""
        if self.orden_aleatorio.get():
            random.shuffle(self.archivos_ordenados)
            self.actualizar_listbox_original()
            self.actualizar_preview()
        else:
            # Restaurar orden original
            self.archivos_ordenados = self.archivos_originales.copy()
            self.actualizar_listbox_original()
            self.actualizar_preview()
            
    def aplicar_renombrado(self):
        """Aplica el renombrado de archivos"""
        directorio = self.directorio_actual.get()
        if not directorio or not os.path.isdir(directorio):
            messagebox.showwarning("Advertencia", "Selecciona un directorio válido primero")
            return
            
        if not self.archivos_ordenados:
            messagebox.showwarning("Advertencia", "No hay archivos para renombrar")
            return
            
        # Confirmar con el usuario
        respuesta = messagebox.askyesno(
            "Confirmar Renombrado",
            f"¿Estás seguro de renombrar {len(self.archivos_ordenados)} archivos?\n\n"
            "Esta acción no se puede deshacer fácilmente."
        )
        
        if not respuesta:
            return
            
        try:
            # Crear un diccionario de mapeo: nombre_original -> nombre_nuevo
            mapeo = {}
            for i, archivo in enumerate(self.archivos_ordenados):
                nuevo_nombre = self.generar_nuevo_nombre(i)
                mapeo[archivo] = nuevo_nombre
                
            # Verificar si hay nombres duplicados
            nuevos_nombres = list(mapeo.values())
            if len(nuevos_nombres) != len(set(nuevos_nombres)):
                messagebox.showerror("Error", "Hay nombres duplicados en la vista previa. Ajusta las opciones.")
                return
                
            # Renombrar en dos fases para evitar conflictos
            # Fase 1: Renombrar a nombres temporales
            temp_mapeo = {}
            for i, (original, nuevo) in enumerate(mapeo.items()):
                ruta_original = os.path.join(directorio, original)
                ruta_temp = os.path.join(directorio, f"__temp_rename_{i}__")
                os.rename(ruta_original, ruta_temp)
                temp_mapeo[ruta_temp] = os.path.join(directorio, nuevo)
                
            # Fase 2: Renombrar de temporal a nombre final
            for temp, final in temp_mapeo.items():
                os.rename(temp, final)
                
            messagebox.showinfo("Éxito", f"Se renombraron {len(mapeo)} archivos correctamente")
            
            # Recargar el directorio
            self.cargar_archivos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al renombrar archivos: {str(e)}")
            
    def recargar(self):
        """Recarga los archivos y resetea las opciones"""
        self.prefijo.set("")
        self.sufijo.set("")
        self.numero_inicio.set(1)
        self.numero_fin.set(100)
        self.ceros.set(3)
        self.usar_ceros.set(True)
        self.orden_aleatorio.set(False)
        self.convertir_jpeg_jpg.set(False)
        
        if self.directorio_actual.get():
            self.cargar_archivos()


def main():
    root = tk.Tk()
    app = RenombradorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
