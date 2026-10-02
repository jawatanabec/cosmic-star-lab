[app]

# ============================================================
# COSMIC STAR LAB
# CLASIFICADOR DE ESTRELLAS
# ============================================================

# Nombre de la aplicación
title = Cosmic Star Lab

# Identificador interno
package.name = cosmicstarlab

# Identificador del desarrollador
package.domain = org.jorwatanabe

# Carpeta donde está main.py
source.dir = .

# Archivos que se incluirán en la aplicación
source.include_exts = py,png,jpg,jpeg,kv,atlas

# Archivos y carpetas que no necesitamos incluir
source.exclude_exts = spec
source.exclude_dirs = bin, __pycache__

# Versión de la aplicación
version = 2.7

# Dependencias necesarias
requirements = python3,kivy

# Orientación vertical
orientation = portrait

# Pantalla completa
fullscreen = 1

# ============================================================
# ANDROID
# ============================================================

# Aceptar automáticamente las licencias del Android SDK
# necesario para la compilación automática en GitHub
android.accept_sdk_license = True

# API mínima de Android
android.minapi = 21

# API objetivo
android.api = 35

# Usar almacenamiento privado de la aplicación
android.private_storage = True

# Entrada estándar de Kivy
android.entrypoint = org.kivy.android.PythonActivity

# ============================================================
# CONFIGURACIÓN DE PYTHON-FOR-ANDROID
# ============================================================

# Rama estable de python-for-android
p4a.branch = master

# ============================================================
# CONFIGURACIÓN DE BUILD
# ============================================================

[buildozer]

# Nivel de información del proceso de compilación
log_level = 2

# Mostrar advertencia si Buildozer se ejecuta como root
warn_on_root = 1
