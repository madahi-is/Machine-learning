# Subir y compartir desde cero

1. Descarga y descomprime el ZIP. Entra a la carpeta `ml-vinos-covid`.
2. En GitHub, crea un repositorio llamado `ml-vinos-covid`. Decide la visibilidad según las condiciones de uso de los datos. Para Colab sin autenticación adicional, el flujo de este notebook usa repositorio público. Déjalo vacío: no marques README, licencia ni .gitignore, porque ya tenemos archivos.
3. En la terminal, dentro de la carpeta descomprimida, ejecuta (reemplaza TU_USUARIO):

```bash
git init
git add .
git commit -m "feat: experimento reproducible de vinos y base para covid"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/ml-vinos-covid.git
git push -u origin main
```

GitHub puede solicitar autenticación. Usa el mecanismo de credenciales de tu equipo; no guardes tokens en archivos o notebooks. Si ya existe un repositorio con commits, clónalo y copia estos archivos dentro en lugar de forzar un push.

4. Modifica REPO_URL en el notebook con la URL real y sube ese cambio. Así tus compañeros no tendrán que editarla.
5. En Settings → Collaborators (o el apartado equivalente de acceso), invita a tus compañeros para que puedan subir cambios. Leer/ejecutar un repo público no requiere ser colaborador.
6. Comparte la URL del repositorio. Cada compañero puede abrir el notebook en Colab desde GitHub o ejecutar:

```bash
git clone https://github.com/TU_USUARIO/ml-vinos-covid.git
cd ml-vinos-covid
```

## Colaboración
Cada persona trabaja en una rama, por ejemplo:

```bash
git switch main
git pull origin main
git switch -c feature/analisis-vinos
# editar archivos
git add .
git commit -m "docs: interpretar resultados de vinos"
git push -u origin feature/analisis-vinos
```

Después abrir un Pull Request. Eviten editar simultáneamente el mismo notebook. Colab no guarda los cambios automáticamente en GitHub: usar Guardar una copia en GitHub o descargar el notebook y subirlo en una rama. Antes de subir notebooks, limpiar salidas innecesarias. No subir .venv, credenciales ni datos privados.

Este paquete está listo para subir, pero no crea por sí mismo un repositorio remoto.
