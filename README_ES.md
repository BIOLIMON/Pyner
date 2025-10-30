# Pyner

**Minería de datos bioinformáticos compatible con PRISMA para investigación en transcriptómica vegetal**

Nico no sigas

Pyner es una herramienta sistemática para extraer datos de bases de datos NCBI (BioProject, SRA, GEO, PubMed) y analizar datasets de RNA-seq. Construido siguiendo las [guías PRISMA 2020](http://www.prisma-statement.org/), proporciona documentación completa del proceso de búsqueda y selección para meta-análisis reproducibles.

## Características

- 🔍 **Búsqueda Multi-base de datos**: Consulta 6+ bases de datos simultáneamente
  - **NCBI**: BioProject, SRA, GEO, PubMed
  - **EBI**: ENA, BioStudies (planeado)
  - **Específicas de plantas**: PlantExp, Ensembl Plants (planeado)
- 📊 **Cumplimiento PRISMA**: Generación automática de diagramas de flujo, logs de screening y reportes de calidad
- ✅ **Evaluación de Calidad**: Evalúa completitud y confiabilidad de metadatos (puntuación 0-100 con grados A-F)
- 🌱 **Enfoque en Plantas**: Diseñado para transcriptómica vegetal pero funciona con cualquier organismo
- 🧬 **Inferencia de Tejidos**: Detección automática de tipos de tejido con niveles de confianza
- 📝 **Documentación Completa**: Rastrea cada decisión desde identificación hasta inclusión
- 🔄 **Reproducible**: Protocolos versionados y logging detallado
- 🚀 **Extensible**: Arquitectura modular para agregar nuevas bases de datos

## Instalación

### Desde código fuente

```bash
git clone https://github.com/BIOLIMON/pyner.git
cd pyner
pip install -e .
```

### Instalación para desarrollo

```bash
pip install -e ".[dev]"  # Incluye herramientas de testing y linting
pip install -e ".[viz]"  # Incluye librerías de visualización
```

## Inicio Rápido

### 1. Configurar credenciales NCBI

Pyner requiere una dirección de email para acceso a la API de NCBI. Una API key es opcional pero fuertemente recomendada para límites de tasa más altos.

```bash
# Opción A: Variables de entorno (recomendado)
export NCBI_EMAIL="tu.email@institucion.edu"
export NCBI_API_KEY="tu_api_key_aqui"

# Opción B: Archivo de configuración
cat > config_local.py <<EOF
NCBI_EMAIL = "tu.email@institucion.edu"
NCBI_API_KEY = "tu_api_key_aqui"
EOF
```

**Obtén tu API key de NCBI**: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

### 2. Ejecutar una búsqueda

```bash
pyner --organism "Arabidopsis thaliana" \
      --condition "salt stress" \
      --experiment "RNA-seq" \
      --label salt
```

### 3. Revisar los resultados

```
data/
├── processed/          # Dataset final incluido
│   └── salt_20241030_processed.csv
├── excluded/           # Registros excluidos con razones
│   └── salt_20241030_excluded.csv
└── prisma_flows/       # Datos del diagrama de flujo PRISMA
    ├── salt_20241030_prisma_flow.json
    └── salt_report.txt

logs/
├── salt_20241030_screening.log         # Decisiones detalladas de screening
└── salt_20241030_screening_summary.txt # Estadísticas resumidas
```

## Uso

### Interfaz de Línea de Comandos

```bash
# Uso básico
pyner --organism "ORGANISMO" \
      --condition "CONDICION" \
      --experiment "TIPO_EXPERIMENTO" \
      --label ETIQUETA

# Con directorio de salida personalizado
pyner --organism "Solanum lycopersicum" \
      --condition "sequía" \
      --experiment "transcriptoma" \
      --label tomate_sequia \
      --output-dir ./mis_resultados

# Con filtrado de calidad
pyner --organism "Oryza sativa" \
      --condition "estrés por calor" \
      --experiment "RNA-seq" \
      --label arroz_calor \
      --min-quality 70  # Solo incluir registros con puntuación de calidad >= 70

# Deshabilitar filtrado de calidad
pyner --organism "Zea mays" \
      --condition "deficiencia de nitrógeno" \
      --experiment "RNA-seq" \
      --label maiz_nitrogeno \
      --no-quality-filter
```

### API de Python

```python
from pyner import DataMiner, Config

# Configurar acceso a NCBI
config = Config.from_env()  # Usar variables de entorno
# O
config = Config(email="tu.email@edu", api_key="TU_KEY")

# Inicializar minero
miner = DataMiner(config)

# Ejecutar búsqueda
results = miner.run(
    organism="Arabidopsis thaliana",
    condition="estrés salino",
    experiment="RNA-seq",
    label="sal",
    enable_quality_filter=True,
    min_quality_score=60.0
)

# Acceder a resultados
print(f"Identificados: {results['summary']['total_identified']} registros")
print(f"Incluidos: {results['summary']['total_included']} registros")

# DataFrames
included_data = results['data']['included']
excluded_data = results['data']['excluded']

# Rutas de archivos
print(results['files'])
```

## Cumplimiento PRISMA

Pyner implementa las guías PRISMA 2020 para revisiones sistemáticas y meta-análisis:

### 1. Documentación del Protocolo

Documenta tu estrategia de búsqueda antes de comenzar:

```bash
cp protocols/search_protocol_template.md protocols/mi_protocolo_busqueda_v1.md
# Edita el protocolo con tus criterios específicos
```

Ver [docs/PRISMA_CHECKLIST.md](docs/PRISMA_CHECKLIST.md) para el checklist completo.

### 2. Diagrama de Flujo PRISMA

Archivo JSON generado automáticamente rastreando:
- **Identificación**: Registros recuperados de cada base de datos
- **Screening**: Registros después de extracción de metadatos
- **Exclusión**: Registros removidos (con razones)
- **Inclusión**: Dataset final

```python
from pyner.prisma import PRISMAFlow

# Cargar y visualizar
flow = PRISMAFlow.load("data/prisma_flows/salt_20241030_prisma_flow.json")
print(flow.generate_text_report())
```

### 3. Log de Screening

Rastro de auditoría detallado de cada decisión de inclusión/exclusión:

```python
from pyner.prisma import ScreeningLog

log = ScreeningLog.load("logs/salt_20241030_screening.log")
stats = log.get_statistics()
print(f"Tasa de inclusión: {stats['inclusion_rate']:.1f}%")
```

### 4. Evaluación de Calidad

Puntuaciones de calidad de metadatos basadas en:
- **Completitud** (30%): Proporción de campos poblados
- **Calidad del título** (20%): Informatividad del título
- **Calidad de la descripción** (20%): Riqueza de la descripción
- **Anotación de tejido** (20%): Presencia y confianza de información de tejido
- **Especificidad del organismo** (10%): Precisión del nombre del organismo

Grados: A (≥90), B (≥80), C (≥70), D (≥60), F (<60)

## Estructura del Proyecto

```
Pyner/
├── pyner/                  # Paquete principal
│   ├── core.py             # Orquestación del pipeline
│   ├── config.py           # Gestión de configuración
│   ├── cli.py              # Interfaz de línea de comandos
│   ├── fetchers/           # Módulos de consulta a bases de datos
│   ├── parsers/            # Extracción de metadatos
│   ├── prisma/             # Herramientas de cumplimiento PRISMA
│   │   ├── flow_diagram.py
│   │   ├── screening_log.py
│   │   └── quality_assessment.py
│   └── utils/              # Funciones auxiliares
├── data/                   # Salidas de datos
│   ├── raw/                # Datos crudos recuperados
│   ├── processed/          # Datasets finales incluidos
│   ├── excluded/           # Registros excluidos
│   └── prisma_flows/       # Documentación PRISMA
├── logs/                   # Logs de screening y ejecución
├── docs/                   # Documentación
│   └── PRISMA_CHECKLIST.md
├── protocols/              # Protocolos de búsqueda
│   └── search_protocol_template.md
├── tests/                  # Tests unitarios
└── examples/               # Scripts de ejemplo
```

## Uso Avanzado

### Pesos de Calidad Personalizados

```python
from pyner.prisma import QualityAssessor

assessor = QualityAssessor()
assessor.weights = {
    "completeness": 0.40,      # Aumentar peso de completitud
    "title_quality": 0.15,
    "description_quality": 0.15,
    "tissue_quality": 0.25,
    "organism_specificity": 0.05
}

# Usar en evaluación
scores = assessor.assess_record(record_dict)
```

### Procesamiento por Lotes de Múltiples Condiciones

```bash
#!/bin/bash
CONDITIONS=("sal" "sequia" "frio" "calor")
TERMS=("estrés salino" "sequía" "estrés por frío" "estrés por calor")

for i in "${!CONDITIONS[@]}"; do
    pyner --organism "Arabidopsis thaliana" \
          --condition "${TERMS[$i]}" \
          --experiment "RNA-seq" \
          --label "${CONDITIONS[$i]}" \
          --output-dir "./resultados"
done
```

### Comparando Múltiples Condiciones

Usa los scripts de visualización incluidos (heredados del Minero original):

```bash
# Después de ejecutar búsquedas para múltiples condiciones
Rscript plot_condiciones.R  # Comparar condiciones
Rscript plot_tejidos.R      # Analizar distribución de tejidos
```

## Esquema de Datos

Los archivos CSV de salida siguen este esquema:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `Fuente` | Base de datos de origen | BioProject, SRA, GEO, PubMed |
| `Condicion` | Etiqueta de condición definida por usuario | sal, sequía |
| `ID` | Número de acceso de base de datos | PRJNA123456 |
| `Title` | Título del registro | Salt stress response in Arabidopsis |
| `Description` | Descripción detallada | RNA-seq analysis of... |
| `Organism` | Nombre científico | Arabidopsis thaliana |
| `Tissue` | Tipo de tejido (si disponible) | root, leaf, shoot |
| `Tissue_confidence` | Nivel de confianza | explicit, inferred, unknown |
| `Extra` | Metadatos adicionales | Cadena JSON |
| `quality_score` | Evaluación de calidad (0-100) | 85.3 |
| `grade` | Grado de calidad | A, B, C, D, F |

## Opciones de Configuración

### Variables de Entorno

- `NCBI_EMAIL`: Email para E-utilities de NCBI (requerido)
- `NCBI_API_KEY`: API key para límites de tasa incrementados (recomendado)

### Archivo de Configuración

Crear `config_local.py`:

```python
NCBI_EMAIL = "tu.email@institucion.edu"
NCBI_API_KEY = "tu_api_key_aqui"
```

Luego usar:

```bash
pyner --config config_local.py --organism ... --condition ...
```

## Desarrollo

### Ejecutar Tests

```bash
pytest
pytest --cov=pyner --cov-report=html
```

### Formateo de Código

```bash
black pyner/
flake8 pyner/
mypy pyner/
```

### Contribuir

1. Haz fork del repositorio
2. Crea una rama de característica (`git checkout -b feature/caracteristica-increible`)
3. Haz tus cambios y agrega tests
4. Asegúrate que los tests pasen y el código esté formateado
5. Commit tus cambios (sigue conventional commits)
6. Push a la rama (`git push origin feature/caracteristica-increible`)
7. Abre un Pull Request

## Solución de Problemas

### Error HTTP 429 (Demasiadas Solicitudes)

**Problema**: Limitación de tasa de NCBI

**Solución**:
1. Agrega una API key: https://www.ncbi.nlm.nih.gov/account/settings/
2. Revisa `rate_limit` en Config (default: 0.34s sin key, 0.11s con key)

### Información de Tejido Faltante

**Problema**: Muchos registros tienen `Tissue: unknown`

**Solución**:
- Para registros SRA, la inferencia de tejido está en desarrollo
- La versión actual hace coincidencia básica de palabras clave
- Considera curación manual para registros críticos

### Puntuaciones de Calidad Muy Bajas

**Problema**: Muchos registros excluidos por baja calidad

**Solución**:
1. Bajar umbral: `--min-quality 40`
2. Deshabilitar filtrado: `--no-quality-filter`
3. Personalizar pesos de calidad (ver Uso Avanzado)

## Citación

Si usas Pyner en tu investigación, por favor cita:

```bibtex
@software{pyner2024,
  title = {Pyner: Minería de datos bioinformáticos compatible con PRISMA},
  author = {Tu Laboratorio},
  year = {2024},
  url = {https://github.com/yourlab/pyner}
}
```

Por favor también cita la declaración PRISMA 2020:

> Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ* 2021;372:n71. doi:10.1136/bmj.n71

## Licencia

Licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.

## Agradecimientos

- Construido sobre la implementación R original de Minero
- Guías PRISMA: http://www.prisma-statement.org/
- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- BioPython: https://biopython.org/

## Contacto

- **Issues**: https://github.com/yourlab/pyner/issues
- **Email**: contact@lab.org
- **Documentación**: https://github.com/yourlab/pyner/wiki

---

**Estado**: Beta - Funcionalidad core NCBI implementada

**Completado**:
- [x] Fetchers NCBI (BioProject, SRA, GEO, PubMed)
- [x] Parsers NCBI con salida estandarizada
- [x] Tracking de flujo PRISMA
- [x] Sistema de evaluación de calidad
- [x] Generación de log de screening
- [x] Constructor de queries con expansión de sinónimos
- [x] Inferencia de tejidos (basada en palabras clave)

**Hoja de Ruta**:
- [ ] Fetchers EBI (ENA, BioStudies)
- [ ] Inferencia mejorada de tejidos vía parsing XML de BioSample
- [ ] Implementar módulo de visualización
- [ ] Agregar soporte para PlantExp y Ensembl Plants
- [ ] Crear interfaz web
- [ ] Agregar machine learning para predicción de calidad
- [ ] Detección de duplicados entre bases de datos
