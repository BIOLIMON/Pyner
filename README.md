# Pyner

**PRISMA-compliant bioinformatics data mining for plant transcriptomics research**

Pyner is a systematic tool for mining NCBI databases (BioProject, SRA, GEO, PubMed) to retrieve and analyze RNA-seq datasets. Built with [PRISMA 2020 guidelines](http://www.prisma-statement.org/) in mind, it provides comprehensive documentation of the search and screening process for reproducible meta-analyses.

## Features

- 🔍 **Multi-database Search**: Query 6+ databases simultaneously
  - **NCBI**: BioProject, SRA, GEO, PubMed
  - **EBI**: ENA, BioStudies (planned)
  - **Plant-specific**: PlantExp, Ensembl Plants (planned)
- 📊 **PRISMA Compliance**: Automatic generation of flow diagrams, screening logs, and quality reports
- ✅ **Quality Assessment**: Evaluate metadata completeness and reliability (0-100 scoring with grades A-F)
- 🌱 **Plant-focused**: Designed for plant transcriptomics but works with any organism
- 🧬 **Tissue Inference**: Automatic tissue type detection with confidence levels
- 📝 **Full Documentation**: Track every decision from identification to inclusion
- 🔄 **Reproducible**: Version-controlled protocols and detailed logging
- 🚀 **Extensible**: Modular architecture for adding new databases

## Installation

### From source

```bash
git clone https://github.com/yourlab/pyner.git
cd pyner
pip install -e .
```

### Development installation

```bash
pip install -e ".[dev]"  # Includes testing and linting tools
pip install -e ".[viz]"  # Includes visualization libraries
```

## Quick Start

### 1. Set up NCBI credentials

Pyner requires an email address for NCBI API access. An API key is optional but strongly recommended for higher rate limits.

```bash
# Option A: Environment variables (recommended)
export NCBI_EMAIL="your.email@institution.edu"
export NCBI_API_KEY="your_api_key_here"

# Option B: Configuration file
cat > config_local.py <<EOF
NCBI_EMAIL = "your.email@institution.edu"
NCBI_API_KEY = "your_api_key_here"
EOF
```

**Get your NCBI API key**: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

### 2. Run a search

```bash
pyner --organism "Arabidopsis thaliana" \
      --condition "salt stress" \
      --experiment "RNA-seq" \
      --label salt
```

### 3. Check the outputs

```
data/
├── processed/          # Final included dataset
│   └── salt_20241030_processed.csv
├── excluded/           # Excluded records with reasons
│   └── salt_20241030_excluded.csv
└── prisma_flows/       # PRISMA flow diagram data
    ├── salt_20241030_prisma_flow.json
    └── salt_report.txt

logs/
├── salt_20241030_screening.log         # Detailed screening decisions
└── salt_20241030_screening_summary.txt # Summary statistics
```

## Usage

### Command Line Interface

```bash
# Basic usage
pyner --organism "ORGANISM" \
      --condition "CONDITION" \
      --experiment "EXPERIMENT_TYPE" \
      --label LABEL

# With custom output directory
pyner --organism "Solanum lycopersicum" \
      --condition "drought" \
      --experiment "transcriptome" \
      --label tomato_drought \
      --output-dir ./my_results

# With quality filtering
pyner --organism "Oryza sativa" \
      --condition "heat stress" \
      --experiment "RNA-seq" \
      --label rice_heat \
      --min-quality 70  # Only include records with quality score >= 70

# Disable quality filtering
pyner --organism "Zea mays" \
      --condition "nitrogen deficiency" \
      --experiment "RNA-seq" \
      --label maize_nitrogen \
      --no-quality-filter
```

### Python API

```python
from pyner import DataMiner, Config

# Configure NCBI access
config = Config.from_env()  # Use environment variables
# OR
config = Config(email="your.email@edu", api_key="YOUR_KEY")

# Initialize miner
miner = DataMiner(config)

# Run search
results = miner.run(
    organism="Arabidopsis thaliana",
    condition="salt stress",
    experiment="RNA-seq",
    label="salt",
    enable_quality_filter=True,
    min_quality_score=60.0
)

# Access results
print(f"Identified: {results['summary']['total_identified']} records")
print(f"Included: {results['summary']['total_included']} records")

# DataFrames
included_data = results['data']['included']
excluded_data = results['data']['excluded']

# File paths
print(results['files'])
```

## PRISMA Compliance

Pyner implements PRISMA 2020 guidelines for systematic reviews and meta-analyses:

### 1. Protocol Documentation

Document your search strategy before starting:

```bash
cp protocols/search_protocol_template.md protocols/my_search_protocol_v1.md
# Edit the protocol with your specific criteria
```

See [docs/PRISMA_CHECKLIST.md](docs/PRISMA_CHECKLIST.md) for full checklist.

### 2. PRISMA Flow Diagram

Automatically generated JSON file tracking:
- **Identification**: Records retrieved from each database
- **Screening**: Records after metadata extraction
- **Exclusion**: Records removed (with reasons)
- **Inclusion**: Final dataset

```python
from pyner.prisma import PRISMAFlow

# Load and visualize
flow = PRISMAFlow.load("data/prisma_flows/salt_20241030_prisma_flow.json")
print(flow.generate_text_report())
```

### 3. Screening Log

Detailed audit trail of every inclusion/exclusion decision:

```python
from pyner.prisma import ScreeningLog

log = ScreeningLog.load("logs/salt_20241030_screening.log")
stats = log.get_statistics()
print(f"Inclusion rate: {stats['inclusion_rate']:.1f}%")
```

### 4. Quality Assessment

Metadata quality scores based on:
- **Completeness** (30%): Proportion of fields populated
- **Title quality** (20%): Informativeness of title
- **Description quality** (20%): Richness of description
- **Tissue annotation** (20%): Presence and confidence of tissue info
- **Organism specificity** (10%): Precision of organism name

Grades: A (≥90), B (≥80), C (≥70), D (≥60), F (<60)

## Project Structure

```
Pyner/
├── pyner/                  # Main package
│   ├── core.py             # Pipeline orchestration
│   ├── config.py           # Configuration management
│   ├── cli.py              # Command-line interface
│   ├── fetchers/           # Database query modules
│   ├── parsers/            # Metadata extraction
│   ├── prisma/             # PRISMA compliance tools
│   │   ├── flow_diagram.py
│   │   ├── screening_log.py
│   │   └── quality_assessment.py
│   └── utils/              # Helper functions
├── data/                   # Data outputs
│   ├── raw/                # Raw retrieved data
│   ├── processed/          # Final included datasets
│   ├── excluded/           # Excluded records
│   └── prisma_flows/       # PRISMA documentation
├── logs/                   # Screening and execution logs
├── docs/                   # Documentation
│   └── PRISMA_CHECKLIST.md
├── protocols/              # Search protocols
│   └── search_protocol_template.md
├── tests/                  # Unit tests
└── examples/               # Example scripts
```

## Advanced Usage

### Custom Quality Weights

```python
from pyner.prisma import QualityAssessor

assessor = QualityAssessor()
assessor.weights = {
    "completeness": 0.40,      # Increase completeness weight
    "title_quality": 0.15,
    "description_quality": 0.15,
    "tissue_quality": 0.25,
    "organism_specificity": 0.05
}

# Use in assessment
scores = assessor.assess_record(record_dict)
```

### Batch Processing Multiple Conditions

```bash
#!/bin/bash
CONDITIONS=("salt" "drought" "cold" "heat")
TERMS=("salt stress" "drought" "cold stress" "heat stress")

for i in "${!CONDITIONS[@]}"; do
    pyner --organism "Arabidopsis thaliana" \
          --condition "${TERMS[$i]}" \
          --experiment "RNA-seq" \
          --label "${CONDITIONS[$i]}" \
          --output-dir "./results"
done
```

### Comparing Multiple Conditions

Use the included visualization scripts (inherited from original Minero):

```bash
# After running searches for multiple conditions
Rscript plot_condiciones.R  # Compare conditions
Rscript plot_tejidos.R      # Analyze tissue distribution
```

## Data Schema

Output CSV files follow this schema:

| Column | Description | Example |
|--------|-------------|---------|
| `Fuente` | Database source | BioProject, SRA, GEO, PubMed |
| `Condicion` | User-defined condition label | salt, drought |
| `ID` | Database accession number | PRJNA123456 |
| `Title` | Record title | Salt stress response in Arabidopsis |
| `Description` | Detailed description | RNA-seq analysis of... |
| `Organism` | Scientific name | Arabidopsis thaliana |
| `Tissue` | Tissue type (if available) | root, leaf, shoot |
| `Tissue_confidence` | Confidence level | explicit, inferred, unknown |
| `Extra` | Additional metadata | JSON string |
| `quality_score` | Quality assessment (0-100) | 85.3 |
| `grade` | Quality grade | A, B, C, D, F |

## Configuration Options

### Environment Variables

- `NCBI_EMAIL`: Email for NCBI E-utilities (required)
- `NCBI_API_KEY`: API key for increased rate limits (recommended)

### Configuration File

Create `config_local.py`:

```python
NCBI_EMAIL = "your.email@institution.edu"
NCBI_API_KEY = "your_api_key_here"
```

Then use:

```bash
pyner --config config_local.py --organism ... --condition ...
```

## Development

### Running Tests

```bash
pytest
pytest --cov=pyner --cov-report=html
```

### Code Formatting

```bash
black pyner/
flake8 pyner/
mypy pyner/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure tests pass and code is formatted
5. Commit your changes (follow conventional commits)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Troubleshooting

### HTTP 429 Error (Too Many Requests)

**Problem**: NCBI rate limiting

**Solution**:
1. Add an API key: https://www.ncbi.nlm.nih.gov/account/settings/
2. Check `rate_limit` in Config (default: 0.34s without key, 0.11s with key)

### Missing Tissue Information

**Problem**: Many records have `Tissue: unknown`

**Solution**:
- For SRA records, tissue inference is in development
- Current version does basic keyword matching
- Consider manual curation for critical records

### Quality Scores Too Low

**Problem**: Many records excluded due to low quality

**Solution**:
1. Lower threshold: `--min-quality 40`
2. Disable filtering: `--no-quality-filter`
3. Customize quality weights (see Advanced Usage)

## Citation

If you use Pyner in your research, please cite:

```bibtex
@software{pyner2024,
  title = {Pyner: PRISMA-compliant bioinformatics data mining},
  author = {Your Lab},
  year = {2024},
  url = {https://github.com/yourlab/pyner}
}
```

Please also cite the PRISMA 2020 statement:

> Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ* 2021;372:n71. doi:10.1136/bmj.n71

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built upon the original Minero R implementation
- PRISMA guidelines: http://www.prisma-statement.org/
- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- BioPython: https://biopython.org/

## Contact

- **Issues**: https://github.com/yourlab/pyner/issues
- **Email**: contact@lab.org
- **Documentation**: https://github.com/yourlab/pyner/wiki

---

**Status**: Beta - Core NCBI functionality implemented

**Completed**:
- [x] NCBI fetchers (BioProject, SRA, GEO, PubMed)
- [x] NCBI parsers with standardized output
- [x] PRISMA flow tracking
- [x] Quality assessment system
- [x] Screening log generation
- [x] Query builder with synonym expansion
- [x] Tissue inference (keyword-based)

**Roadmap**:
- [ ] EBI fetchers (ENA, BioStudies)
- [ ] Enhanced tissue inference via BioSample XML parsing
- [ ] Implement visualization module
- [ ] Add PlantExp and Ensembl Plants support
- [ ] Create web interface
- [ ] Add machine learning for quality prediction
- [ ] Duplicate detection across databases
