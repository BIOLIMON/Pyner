# Plan de Generalización de Pyner
## De "Plant RNA-seq" a "Bioinformática General"

---

## 🔍 Sesgos Identificados

### 1. **Descripción del Proyecto**
- ❌ "plant transcriptomics research"
- ✅ "bioinformatics research" (general)

### 2. **Esquema de Datos**
- ❌ `Tissue` → demasiado específico a organismos multicelulares
- ✅ `Sample_Type` o `Biological_Material` (más general)
- ❌ `Tissue_confidence` → solo para tejidos
- ✅ `Sample_Annotation_Confidence` (general)

### 3. **Query Builder - Sinónimos Sesgados**
**Actual** (solo plantas):
```python
synonyms = {
    "salt": ["salt stress", "NaCl", "salinity"],
    "drought": ["water deficit", "dehydration"],
    "cold": ["cold stress", "chilling"]
}
```

**Debería incluir**:
- Enfermedades humanas: cancer, diabetes, alzheimer
- Condiciones bacterianas: antibiotic resistance, biofilm
- Tratamientos: drug treatment, knockout, overexpression
- Ambientes: marine, soil, gut microbiome

### 4. **Tissue Keywords (SRA Parser)**
**Actual** (solo plantas):
```python
tissue_keywords = [
    'root', 'leaf', 'shoot', 'flower', 'seed', 'fruit'
]
```

**Debería incluir**:
- Humanos/animales: blood, brain, liver, muscle, tumor
- Bacterias: culture, biofilm, colony
- Cell lines: HeLa, HEK293, CHO
- Otros: tissue culture, organoid, spheroid

### 5. **Experiment Type - Solo RNA-seq**
**Actual**:
```python
if "rna" in experiment.lower():
    terms = ["RNA-seq", "RNAseq", "transcriptome"]
```

**Debería incluir**:
- DNA sequencing: WGS, WES, targeted sequencing
- Epigenomics: ChIP-seq, ATAC-seq, bisulfite-seq
- Metagenomics: 16S, shotgun metagenomics
- Proteomics: mass spectrometry
- Otros: Hi-C, CLIP-seq, ribosome profiling

### 6. **Quality Assessment Keywords**
**Actual** (sesgado):
```python
keywords = [
    "stress", "response", "tissue", "development",
    "expression", "transcriptome"
]
```

**Debería ser configurable** por dominio

### 7. **Organism Keywords**
**Actual** (solo plantas modelo):
```python
organisms = [
    'Arabidopsis thaliana', 'Oryza sativa', 'Zea mays'
]
```

**Debería incluir**:
- Humanos: Homo sapiens
- Ratón: Mus musculus
- Bacterias: Escherichia coli, Bacillus subtilis
- Levadura: Saccharomyces cerevisiae
- Pez cebra: Danio rerio
- Drosophila: Drosophila melanogaster

---

## 🎯 Plan de Cambios

### FASE 1: Generalizar Esquema de Datos ⭐ (CRÍTICO)

#### 1.1 Cambiar Nombres de Campos
```python
# Antes
{
    "Tissue": "root",
    "Tissue_confidence": "inferred"
}

# Después
{
    "Sample_Type": "root tissue",
    "Sample_Annotation": "inferred",
    "Material_Type": "tissue"  # tissue | cell_line | culture | whole_organism | environmental
}
```

#### 1.2 Agregar Campos Generales
```python
{
    "Sample_Type": str,           # Reemplaza "Tissue"
    "Sample_Annotation": str,     # explicit | inferred | unknown
    "Material_Type": str,         # tissue | cell_line | culture | whole_organism
    "Cell_Type": str,             # Para single-cell
    "Cell_Line": str,             # HeLa, HEK293, etc.
    "Developmental_Stage": str,   # embryo, adult, larva, etc.
    "Disease": str,               # cancer, diabetes, etc.
    "Treatment": str,             # drug name, knockout gene, etc.
    "Strain": str,                # Para bacterias/levaduras
    "Sex": str,                   # male | female | hermaphrodite
    "Age": str,                   # embryonic day 10, adult
}
```

---

### FASE 2: Query Builder Configurable por Dominio

#### 2.1 Crear Diccionarios de Sinónimos por Dominio

**Archivo**: `pyner/domain_vocabularies.py`

```python
CONDITION_SYNONYMS = {
    # Plantas
    "salt_stress": ["salt stress", "NaCl", "salinity", "sodium chloride"],
    "drought": ["drought", "water deficit", "dehydration", "water stress"],

    # Humanos
    "cancer": ["cancer", "tumor", "malignancy", "neoplasm", "carcinoma"],
    "diabetes": ["diabetes", "diabetic", "hyperglycemia", "insulin resistance"],
    "alzheimer": ["Alzheimer", "dementia", "neurodegeneration"],

    # Bacterias
    "antibiotic_resistance": ["antibiotic resistance", "drug resistance", "AMR"],
    "biofilm": ["biofilm", "bacterial biofilm", "surface attachment"],

    # General
    "infection": ["infection", "pathogen", "disease", "infected"],
    "inflammation": ["inflammation", "inflammatory", "immune response"]
}

EXPERIMENT_SYNONYMS = {
    # Transcriptomics
    "rna_seq": ["RNA-seq", "RNAseq", "RNA seq", "transcriptome", "transcriptomic"],
    "single_cell": ["single-cell", "scRNA-seq", "droplet-based", "10x"],

    # Genomics
    "wgs": ["whole genome sequencing", "WGS", "genome sequencing"],
    "wes": ["whole exome sequencing", "WES", "exome"],
    "targeted_seq": ["targeted sequencing", "amplicon", "panel"],

    # Epigenomics
    "chip_seq": ["ChIP-seq", "ChIPseq", "chromatin immunoprecipitation"],
    "atac_seq": ["ATAC-seq", "ATACseq", "chromatin accessibility"],
    "bisulfite": ["bisulfite", "WGBS", "methylation", "BS-seq"],

    # Metagenomics
    "16s": ["16S", "16S rRNA", "bacterial profiling"],
    "metagenome": ["metagenome", "shotgun metagenomics", "microbiome"],

    # Proteomics
    "proteomics": ["proteomics", "mass spectrometry", "LC-MS"],
}

SAMPLE_TYPE_KEYWORDS = {
    # Plantas
    "plant": ["root", "leaf", "shoot", "flower", "seed", "fruit", "stem"],

    # Humanos/Mamíferos
    "human": ["blood", "plasma", "serum", "PBMC", "brain", "liver", "kidney",
              "lung", "heart", "muscle", "adipose", "tumor", "normal"],

    # Líneas celulares
    "cell_line": ["HeLa", "HEK293", "CHO", "Jurkat", "K562", "A549"],

    # Bacterias
    "bacteria": ["culture", "biofilm", "colony", "planktonic", "stationary phase"],

    # Otros
    "other": ["organoid", "spheroid", "iPSC", "ESC", "primary culture"]
}
```

#### 2.2 Modificar QueryBuilder

```python
class QueryBuilder:
    def __init__(self, domain: str = "general"):
        """
        Args:
            domain: 'general' | 'plant' | 'human' | 'bacteria' | 'custom'
        """
        self.domain = domain
        self.load_vocabularies(domain)

    def load_vocabularies(self, domain: str):
        """Cargar vocabularios específicos del dominio"""
        if domain == "plant":
            self.condition_vocab = filter_by_domain(CONDITION_SYNONYMS, ["plant"])
            self.sample_vocab = SAMPLE_TYPE_KEYWORDS["plant"]
        elif domain == "human":
            self.condition_vocab = filter_by_domain(CONDITION_SYNONYMS, ["human"])
            self.sample_vocab = SAMPLE_TYPE_KEYWORDS["human"]
        else:  # general
            self.condition_vocab = CONDITION_SYNONYMS
            self.sample_vocab = all_sample_keywords()
```

---

### FASE 3: Parsers Generalizados

#### 3.1 Actualizar Esquema de Parsers

**Todos los parsers deben devolver**:
```python
{
    "Fuente": str,
    "Condicion": str,
    "ID": str,
    "Title": str,
    "Description": str,
    "Organism": str,

    # NUEVOS campos generalizados
    "Sample_Type": str,           # Reemplaza Tissue
    "Sample_Annotation": str,     # Reemplaza Tissue_confidence
    "Material_Type": str,         # tissue | cell_line | culture | whole_organism
    "Cell_Type": str,
    "Cell_Line": str,
    "Developmental_Stage": str,
    "Disease": str,
    "Treatment": str,
    "Strain": str,

    "Extra": str  # JSON con campos adicionales
}
```

#### 3.2 Crear Inferencia de Sample_Type Multi-dominio

**Archivo**: `pyner/parsers/sample_inference.py`

```python
class SampleTypeInferencer:
    """
    Infiere tipo de muestra (sample type) para cualquier organismo.
    """

    def __init__(self):
        self.keywords = SAMPLE_TYPE_KEYWORDS

    def infer_sample_type(self, text: str, organism: str = "") -> dict:
        """
        Retorna:
        {
            "sample_type": str,
            "confidence": "explicit" | "inferred" | "unknown",
            "material_type": "tissue" | "cell_line" | "culture" | etc
        }
        """
        # Auto-detectar dominio basado en organismo
        domain = self._detect_domain(organism)

        # Buscar keywords relevantes
        for keyword in self.keywords[domain]:
            if keyword in text.lower():
                return {
                    "sample_type": keyword,
                    "confidence": "inferred",
                    "material_type": self._classify_material(keyword)
                }

        return {
            "sample_type": None,
            "confidence": "unknown",
            "material_type": None
        }

    def _detect_domain(self, organism: str) -> str:
        """Detectar dominio biológico"""
        organism_lower = organism.lower()

        if any(x in organism_lower for x in ["arabidopsis", "oryza", "zea", "solanum"]):
            return "plant"
        elif "homo sapiens" in organism_lower or "human" in organism_lower:
            return "human"
        elif any(x in organism_lower for x in ["escherichia", "bacillus", "pseudomonas"]):
            return "bacteria"
        else:
            return "general"
```

---

### FASE 4: Quality Assessment Configurable

#### 4.1 Keywords por Dominio

```python
class QualityAssessor:
    def __init__(self, domain: str = "general"):
        self.domain = domain
        self.load_domain_keywords()

    def load_domain_keywords(self):
        """Cargar keywords relevantes según dominio"""

        self.title_keywords = {
            "general": [
                "response", "expression", "analysis", "study", "effect",
                "regulation", "function", "mechanism", "pathway"
            ],
            "plant": [
                "stress", "development", "tissue", "root", "leaf",
                "transcriptome", "gene expression"
            ],
            "human": [
                "patient", "disease", "clinical", "treatment", "cancer",
                "tumor", "therapy", "diagnosis"
            ],
            "bacteria": [
                "strain", "growth", "culture", "resistance", "biofilm",
                "metabolism", "pathway"
            ]
        }

        self.method_keywords = {
            "rna_seq": ["RNA", "sequencing", "library", "reads", "transcript"],
            "wgs": ["genome", "variant", "SNP", "mutation", "coverage"],
            "chip_seq": ["ChIP", "binding", "peak", "chromatin", "histone"],
            "proteomics": ["protein", "peptide", "mass spec", "LC-MS"]
        }
```

---

### FASE 5: Ejemplos Diversos

#### 5.1 Crear Ejemplos por Dominio

**Humanos - Cancer**:
```python
# examples/human_cancer_example.py
miner.run(
    organism="Homo sapiens",
    condition="breast cancer",
    experiment="RNA-seq",
    label="breast_cancer"
)
```

**Bacterias - Resistencia a Antibióticos**:
```python
# examples/bacteria_resistance_example.py
miner.run(
    organism="Escherichia coli",
    condition="antibiotic resistance",
    experiment="WGS",
    label="ecoli_amr"
)
```

**Levadura - Estrés Osmótico**:
```python
# examples/yeast_stress_example.py
miner.run(
    organism="Saccharomyces cerevisiae",
    condition="osmotic stress",
    experiment="RNA-seq",
    label="yeast_osmotic"
)
```

---

### FASE 6: Configuración Flexible

#### 6.1 Archivo de Configuración de Dominio

**Archivo**: `domain_config.yaml`

```yaml
# Configuración para plantas
plant:
  sample_field_name: "Tissue"
  sample_keywords:
    - root
    - leaf
    - shoot
  quality_keywords:
    - stress
    - development

# Configuración para humanos
human:
  sample_field_name: "Sample_Type"
  sample_keywords:
    - blood
    - tumor
    - brain
  quality_keywords:
    - patient
    - disease
    - clinical

# Configuración general (default)
general:
  sample_field_name: "Sample_Type"
  use_all_keywords: true
```

#### 6.2 CLI con Opción de Dominio

```bash
pyner --organism "Homo sapiens" \
      --condition "breast cancer" \
      --experiment "RNA-seq" \
      --label breast_cancer \
      --domain human  # <-- NUEVO
```

---

## 📋 Orden de Implementación

### ✅ PRIORIDAD ALTA (Hacerlo ahora)

1. **Renombrar campos de datos**:
   - `Tissue` → `Sample_Type`
   - `Tissue_confidence` → `Sample_Annotation`
   - Agregar `Material_Type`

2. **Generalizar SRA parser**:
   - Inferencia multi-dominio
   - Keywords configurables

3. **Ampliar query builder**:
   - Agregar sinónimos para humanos, bacterias
   - Hacer experimentos más allá de RNA-seq

4. **Actualizar documentación**:
   - Cambiar "plant transcriptomics" → "bioinformatics"
   - Ejemplos diversos

### ⚠️ PRIORIDAD MEDIA (Siguiente iteración)

5. **Quality assessment configurable**:
   - Keywords por dominio
   - Pesos ajustables

6. **Crear ejemplos diversos**:
   - Humanos, bacterias, levaduras

### 🔮 FUTURO

7. **Interfaz de configuración**:
   - YAML para configurar dominios
   - Vocabularios personalizados

8. **Auto-detección de dominio**:
   - Basado en organismo detectar keywords relevantes

---

## 🎯 Beneficios de la Generalización

1. ✅ **Aplicable a cualquier campo biológico**
2. ✅ **No limitado a RNA-seq**
3. ✅ **Metadatos más ricos y flexibles**
4. ✅ **Mayor adopción potencial**
5. ✅ **Verdaderamente PRISMA-compliant para cualquier revisión sistemática**

---

## 📊 Métricas de Éxito

- [ ] README no menciona "plants" como foco principal
- [ ] Ejemplos funcionan para humanos, plantas Y bacterias
- [ ] Query builder tiene sinónimos de ≥3 dominios
- [ ] Quality assessment no asume tejidos vegetales
- [ ] Esquema de datos es agnóstico al tipo de organismo
- [ ] Tests cubren humanos, plantas, bacterias

---

¿Procedemos a implementar estos cambios? ¿Empezamos con PRIORIDAD ALTA?
