# Instrucciones para Subir Pyner a GitHub

## Estado Actual del Repositorio

✅ **Archivos de test excluidos**:
- `test_results/` está en `.gitignore`
- `test_run.py` fue eliminado
- Ningún archivo con credenciales está trackeado

✅ **Repositorio limpio**:
```bash
3 commits realizados:
- 182ad03 Fix QueryBuilder + Spanish translation
- aabd10c Implement NCBI fetchers and parsers
- 44fa5f8 Initial commit: PRISMA structure
```

---

## Opción 1: Crear Repositorio desde GitHub Web (Recomendado)

### Paso 1: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Configura el repositorio:
   - **Repository name**: `Pyner`
   - **Description**: `PRISMA-compliant bioinformatics data mining for plant transcriptomics`
   - **Visibility**: ✅ Public
   - **NO** inicialices con README, .gitignore o license (ya los tenemos)
3. Click en **"Create repository"**

### Paso 2: Conectar tu repositorio local

GitHub te mostrará instrucciones. Usa estas (reemplaza `TU_USERNAME`):

```bash
cd /mnt/64274670-793f-4763-b132-b5c7b1178bb0/nmuller/Documents/Minero/Pyner

# Agregar remote
git remote add origin https://github.com/TU_USERNAME/Pyner.git

# Renombrar rama a main (opcional pero recomendado)
git branch -M main

# Subir todo
git push -u origin main
```

---

## Opción 2: Usar GitHub CLI (Si tienes gh instalado)

### Paso 1: Autenticarte

```bash
gh auth login
```

Sigue las instrucciones en pantalla.

### Paso 2: Crear y subir repositorio

```bash
cd /mnt/64274670-793f-4763-b132-b5c7b1178bb0/nmuller/Documents/Minero/Pyner

# Crear repo público y hacer push
gh repo create Pyner --public --source=. --remote=origin --push

# Ver el repositorio en el navegador
gh repo view --web
```

---

## Verificación Post-Upload

Después de subir, verifica que todo esté correcto:

### En GitHub Web:

1. ✅ Archivo `README.md` se muestra correctamente
2. ✅ Enlace a `README_ES.md` funciona
3. ✅ No hay carpeta `test_results/`
4. ✅ No hay archivo `test_run.py`
5. ✅ Estructura de directorios correcta:
   ```
   Pyner/
   ├── pyner/          (código fuente)
   ├── docs/           (documentación)
   ├── examples/       (ejemplos)
   ├── protocols/      (templates)
   ├── data/           (solo .gitkeep)
   ├── logs/           (solo .gitkeep)
   ├── README.md
   ├── README_ES.md
   ├── LICENSE
   └── setup.py
   ```

### Localmente:

```bash
# Verificar remote configurado
git remote -v

# Verificar que estás sincronizado
git status

# Ver archivos ignorados (no deberían estar en GitHub)
git status --ignored
```

---

## Opcional: Configurar GitHub Pages

Si quieres documentación web automática:

1. Ve a tu repositorio en GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `main` / `docs`
5. Save

---

## Opcional: Agregar Topics/Tags

Para mejor descubribilidad:

1. Ve a tu repositorio en GitHub
2. Click en el ⚙️ junto a "About"
3. Agregar topics:
   - `bioinformatics`
   - `rna-seq`
   - `transcriptomics`
   - `prisma`
   - `ncbi`
   - `data-mining`
   - `plant-biology`
   - `arabidopsis`
   - `python`

---

## Solución de Problemas

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU_USERNAME/Pyner.git
```

### Error: "Authentication failed"

Si usas HTTPS y tienes 2FA:
1. Ve a https://github.com/settings/tokens
2. Generate new token (classic)
3. Scopes: `repo`
4. Usa el token como contraseña

O configura SSH:
```bash
ssh-keygen -t ed25519 -C "tu.email@gmail.com"
cat ~/.ssh/id_ed25519.pub  # Agregar en GitHub Settings → SSH keys
git remote set-url origin git@github.com:TU_USERNAME/Pyner.git
```

### Archivos de test aparecen en GitHub

Si accidentalmente están trackeados:
```bash
git rm -r --cached test_results/
git rm --cached test_run.py
git commit -m "Remove test files from tracking"
git push
```

---

## Configuración Post-Upload Recomendada

### 1. Agregar badges al README

Agrega al inicio de `README.md`:

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRISMA](https://img.shields.io/badge/PRISMA-2020-green.svg)](http://www.prisma-statement.org/)
```

### 2. Configurar GitHub Actions (CI/CD)

Crear `.github/workflows/python-tests.yml` para tests automáticos.

### 3. Agregar CONTRIBUTING.md

Guía para contribuidores.

---

## Próximos Pasos

Una vez subido:

1. ✅ Compartir el link del repositorio
2. ✅ Crear un release (v0.1.0-beta)
3. ✅ Considerar publicar en PyPI
4. ✅ Escribir artículo/blog post
5. ✅ Compartir en comunidades relevantes

---

## Contacto

Si tienes problemas subiendo el repositorio, puedes:
- Revisar la documentación de GitHub: https://docs.github.com/en/get-started
- Buscar ayuda en: https://github.community/
