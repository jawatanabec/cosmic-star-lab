[app]

# Nombre que aparecerá en Android
title = Cosmic Star Lab

# Identificador interno de la aplicación
package.name = cosmicstarlab
package.domain = org.jorwatanabe

# Carpeta que contiene main.py
source.dir = .

# Archivos que se incluirán
source.include_exts = py,png,jpg,jpeg,kv,atlas

# Versión
version = 2.7

# Dependencia necesaria
requirements = python3,kivy

# Pantalla vertical
orientation = portrait

# Aplicación a pantalla completa
fullscreen = 1


[buildozer]

# Nivel normal de información durante la compilación
log_level = 2

# Aviso si se ejecuta como administrador/root
warn_on_root = 1
