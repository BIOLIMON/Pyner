# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyner is a PRISMA 2020-compliant bioinformatics data mining tool for systematic retrieval and analysis of RNA-seq datasets from NCBI databases (BioProject, SRA, GEO, PubMed). Designed for plant transcriptomics research but applicable to any organism.

**Current Status:** Beta (v0.1.0) - Core NCBI functionality implemented, no test suite yet.

## Development Commands

### Installation

```bash
# Development installation with all dependencies
pip install -e ".[dev,viz]"
```

### Code Quality

```bash
# Format code (line-length 88, Python 3.8+)
black pyner/

# Lint
flake8 pyner/

# Type checking (lenient mode currently)
mypy pyner/
```

### Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage reports
pytest --cov=pyner --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_parsers.py

# Run specific test
pytest tests/test_config.py::TestConfig::test_from_env_missing_email
```

**Note:** Test suite does not exist yet. When writing tests, follow pytest conventions:
- Test files: `test_*.py` in `tests/` directory
- Test classes: `Test*`
- Test functions: `test_*`
- Use mocks for NCBI API calls to avoid rate limits

### Running the Tool

```bash
# CLI usage
pyner --organism "Arabidopsis thaliana" \
      --condition "salt stress" \
      --experiment "RNA-seq" \
      --label salt \
      --min-quality 60

# Programmatic usage - see examples/basic_usage.py and examples/complete_example.py
python examples/basic_usage.py
```

## Architecture

### Data Flow Pipeline (6 Stages)

Orchestrated by `DataMiner` class in `pyner/core.py`:

```
1. IDENTIFICATION
   └─ Fetchers query NCBI databases → List of IDs per database

2. SCREENING
   └─ Fetchers retrieve metadata → Parsers standardize format → DataFrame

3. QUALITY ASSESSMENT
   └─ QualityAssessor scores each record (0-100) + assigns grade (A-F)

4. FILTERING
   └─ Apply quality threshold → Split included/excluded → Log decisions

5. SAVE DATA
   └─ Write CSV files: processed/ (included), excluded/ (excluded)

6. PRISMA DOCUMENTATION
   └─ Generate: flow diagram (JSON), screening log (CSV), reports (TXT)
```

### Key Modules

**`pyner/core.py` - DataMiner**
- Main orchestrator of the entire pipeline
- Method `run()` executes all 6 stages sequentially
- Returns dict with: `data`, `files`, `summary`

**`pyner/config.py` - Config**
- Manages NCBI credentials (email required, API key recommended)
- Three loading methods: `from_env()`, `from_file()`, direct constructor
- Handles rate limiting: 0.34s without API key, 0.11s with key

**`pyner/fetchers/` - Database Access**
- `ncbi_base.py`: Base class with Biopython Entrez integration, rate limiting, pagination
- Database-specific fetchers: `bioproject_fetcher.py`, `sra_fetcher.py`, `geo_fetcher.py`, `pubmed_fetcher.py`
- Each implements: `fetch_ids()`, `fetch_summaries()`

**`pyner/parsers/` - Data Standardization**
- Convert database-specific formats → 11-column DataFrame standard
- Columns: `Fuente`, `Condicion`, `ID`, `Title`, `Description`, `Organism`, `Tissue`, `Tissue_confidence`, `Extra`, `quality_score`, `grade`
- Only SRA parser performs tissue inference (keyword-based with 28 tissue terms)

**`pyner/query_builder.py` - Query Construction**
- Expands terms with synonyms (e.g., "salt stress" → "salt OR NaCl OR salinity")
- Database-specific query formatting
- Methods: `build_ncbi_query()`, `build_sra_query()`, `build_geo_query()`, etc.

**`pyner/prisma/` - PRISMA 2020 Compliance**
- `flow_diagram.py` (PRISMAFlow): Tracks counts at each pipeline stage, generates JSON + text reports
- `screening_log.py` (ScreeningLog): Detailed audit trail (CSV) of every inclusion/exclusion decision
- `quality_assessment.py` (QualityAssessor): Multi-factor scoring with configurable weights

### Standard DataFrame Schema (11 Columns)

All parsers output this format:

| Column | Type | Description |
|--------|------|-------------|
| `Fuente` | str | Source database (BioProject/SRA/GEO/PubMed) |
| `Condicion` | str | User-defined condition label |
| `ID` | str | Accession number (PRJNA*/SRX*/GSE*/PMID) |
| `Title` | str | Record title |
| `Description` | str | Summary/abstract text |
| `Organism` | str | Scientific name |
| `Tissue` | str | Tissue type (or None) |
| `Tissue_confidence` | str | "explicit", "inferred", "unknown", or None |
| `Extra` | str | JSON-serialized dict of database-specific metadata |
| `quality_score` | float | 0-100 quality metric |
| `grade` | str | A/B/C/D/F letter grade |

### Quality Scoring System

Weighted multi-factor assessment (configurable via `QualityAssessor.weights`):

- **Completeness (30%)**: Proportion of required vs. optional fields populated
- **Title quality (20%)**: Length + biological keyword presence
- **Description quality (20%)**: Length + methodological keywords
- **Tissue quality (20%)**: Explicit (100) > Inferred (60) > Unknown (30) > None (0)
- **Organism specificity (10%)**: Binomial (100) > Genus (60) > Common name (40)

Grades: A (≥90), B (≥80), C (≥70), D (≥60), F (<60)

### Tissue Inference (SRA Only)

Currently uses keyword-based matching against 28 plant tissue terms:
```python
tissue_keywords = [
    'root', 'leaf', 'leaves', 'shoot', 'stem', 'flower', 'seed',
    'fruit', 'berry', 'petal', 'sepal', 'carpel', 'stamen',
    'cotyledon', 'hypocotyl', 'radicle', 'meristem', 'bark',
    'xylem', 'phloem', 'pollen', 'ovule', 'embryo', 'endosperm',
    'whole plant', 'seedling', 'callus', 'culture', 'cell'
]
```

Searches combined text from: title + sample name + BioSample XML + ExpXml

**Confidence levels:**
- `explicit`: Found in structured metadata field
- `inferred`: Found via keyword matching
- `unknown`: No tissue information available

## Extending the Codebase

### Adding a New Database

1. **Create fetcher** in `pyner/fetchers/new_db_fetcher.py`:
   ```python
   from .ncbi_base import NCBIBaseFetcher

   class NewDBFetcher(NCBIBaseFetcher):
       def __init__(self, config):
           super().__init__(config, database="newdb")

       def fetch_ids(self, organism, condition, experiment):
           # Return list of IDs
           pass

       def fetch_summaries(self, id_list):
           # Return list of dicts with metadata
           pass
   ```

2. **Create parser** in `pyner/parsers/new_db_parser.py`:
   ```python
   class NewDBParser:
       def parse_summaries(self, summaries, condition):
           # Return list of dicts with 11-column schema
           pass

       def parse_single_summary(self, summary, condition):
           # Return single dict with standardized fields
           pass
   ```

3. **Register in `__init__.py`** files for both directories

4. **Integrate in `core.py`** by adding to `DataMiner.run()` pipeline

### Adding a New Quality Metric

Extend `QualityAssessor` in `pyner/prisma/quality_assessment.py`:

```python
class QualityAssessor:
    def __init__(self):
        self.weights = {
            "completeness": 0.25,         # Reduce existing
            "title_quality": 0.20,
            "description_quality": 0.20,
            "tissue_quality": 0.15,       # Reduce existing
            "organism_specificity": 0.10,
            "new_metric": 0.10            # Add new metric
        }

    def _assess_new_metric(self, record_dict):
        # Return 0-100 score
        pass

    def assess_record(self, record_dict):
        # Add self._assess_new_metric() to the weighted sum
        pass
```

Ensure weights sum to 1.0.

### Adding Tests

Create test files in `tests/` directory following pytest conventions:

```python
# tests/test_parsers.py
import pytest
from pyner.parsers import BioProjectParser

class TestBioProjectParser:
    def test_parse_single_summary_extracts_id(self):
        parser = BioProjectParser()
        summary = {"Project_Acc": "PRJNA123456", "Project_Title": "Test"}
        result = parser.parse_single_summary(summary, "test_condition")
        assert result["ID"] == "PRJNA123456"
        assert result["Fuente"] == "BioProject"
```

**Important:** Mock NCBI API calls to avoid rate limits and ensure reproducibility:

```python
@pytest.mark.integration  # Tag real API tests
class TestBioProjectFetcher:
    @pytest.fixture
    def config(self):
        return Config(email="test@test.edu")

    @pytest.fixture
    def mock_entrez(self, monkeypatch):
        # Mock Biopython Entrez calls
        pass
```

## Configuration Management

### Required: NCBI Email

NCBI requires an email for API access. Set via:

```bash
# Environment variable (recommended)
export NCBI_EMAIL="your.email@institution.edu"

# Or in Python
config = Config(email="your.email@institution.edu")
```

### Recommended: NCBI API Key

Increases rate limit from 3 req/s to 10 req/s:

```bash
export NCBI_API_KEY="your_api_key_here"
```

Get your API key: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

### Configuration Priority

1. Direct constructor parameters: `Config(email="...", api_key="...")`
2. Config file: `Config.from_file("config_local.py")`
3. Environment variables: `Config.from_env()`

### Never Commit Credentials

- Use `.gitignore` for `config_local.py`, `.env` files
- `Config.__repr__()` masks API keys in logs: `api_key=***`

## Important Implementation Details

### Rate Limiting

All NCBI fetchers inherit rate limiting from `NCBIBaseFetcher`:
- Without API key: 0.34s delay between requests
- With API key: 0.11s delay
- Automatically enforced via `time.sleep()` in base class

**Do not bypass rate limits** - NCBI will block your IP.

### Pagination

`NCBIBaseFetcher.search_all()` handles large result sets automatically:
- Fetches in batches (default: 1000 records)
- Combines results from multiple API calls
- Respects rate limits between batches

### Error Handling Philosophy

- **Missing data**: Return empty results, allow pipeline to continue
- **Parse failures**: Log warning, skip record, continue processing
- **API errors**: Return empty list, log error
- **Config errors**: Fail loudly with helpful messages

### PRISMA Integration Points

PRISMA compliance is integrated throughout the pipeline, not bolted on afterward:

1. **Identification** (Step 1): `prisma_flow.add_identified(database, count)` after each fetcher
2. **Screening** (Step 2): `prisma_flow.set_screened(count)` after metadata collection
3. **Filtering** (Step 4): `screening_log.add_entry(record, decision, reason)` for each record
4. **Documentation** (Step 6): Both PRISMAFlow and ScreeningLog save JSON/CSV/TXT

See `docs/PRISMA_CHECKLIST.md` for full PRISMA 2020 compliance guide.

## File Structure Notes

### Output Directory Structure

```
data/
├── raw/                    # Raw API responses (not currently used)
├── processed/              # Final included datasets
│   └── {label}_YYYYMMDD_processed.csv
├── excluded/               # Excluded records with reasons
│   └── {label}_YYYYMMDD_excluded.csv
└── prisma_flows/           # PRISMA documentation
    ├── {label}_YYYYMMDD_prisma_flow.json
    └── {label}_report.txt

logs/
├── {label}_YYYYMMDD_screening.log         # CSV audit trail
└── {label}_YYYYMMDD_screening_summary.txt # Human-readable summary
```

### Protocol Documentation

Before starting a systematic search, document your protocol:

```bash
cp protocols/search_protocol_template.md protocols/my_search_v1.md
# Edit with your specific criteria
```

This ensures PRISMA compliance and reproducibility.

## Known Limitations

1. **Tissue Inference**: Only SRA has tissue inference; currently keyword-based only
2. **PubMed Organism Extraction**: Limited to 10 hardcoded plant species in title matching
3. **No Duplicate Detection**: Records from overlapping databases (e.g., SRA + GEO) are not deduplicated
4. **Sequential Processing**: No concurrent API calls (by design, to respect rate limits)
5. **No Tests**: Test suite not yet implemented despite pytest configuration

## Roadmap Features

Per README_ES.md, planned features include:

- [ ] EBI fetchers (ENA, BioStudies)
- [ ] Improved tissue inference via BioSample XML parsing
- [ ] Visualization module
- [ ] PlantExp and Ensembl Plants support
- [ ] Web interface
- [ ] Machine learning for quality prediction
- [ ] Cross-database duplicate detection

When implementing roadmap features, follow existing architectural patterns:
- New databases → Fetcher + Parser pair
- New functionality → Modular with clear separation of concerns
- New outputs → Update PRISMA tracking accordingly

## Code Style Conventions

- **Formatting**: Black (line-length 88, Python 3.8+)
- **Linting**: Flake8 standard rules
- **Type Hints**: Encouraged but not strictly enforced (mypy lenient mode)
- **Naming**:
  - Classes: PascalCase (`DataMiner`, `BioProjectFetcher`)
  - Functions/methods: snake_case (`fetch_ids`, `parse_single_summary`)
  - Private methods: Leading underscore (`_clean_text`, `_infer_tissue`)
- **Docstrings**: Include Args, Returns, and Example sections for public APIs

## Example Workflows

### Basic Search

```python
from pyner import DataMiner, Config

config = Config.from_env()
miner = DataMiner(config)

results = miner.run(
    organism="Arabidopsis thaliana",
    condition="salt stress",
    experiment="RNA-seq",
    label="salt"
)

included = results["data"]["included"]
print(f"Found {len(included)} records")
```

### Custom Quality Filtering

```python
# Disable quality filter to get all records
results = miner.run(
    organism="Oryza sativa",
    condition="drought",
    experiment="RNA-seq",
    label="rice_drought",
    enable_quality_filter=False
)

# Apply custom filtering post-hoc
included = results["data"]["included"]
high_quality = included[included["quality_score"] >= 85]
has_tissue = included[included["Tissue"].notna()]
custom_subset = included[
    (included["quality_score"] >= 70) &
    (included["Tissue_confidence"] == "explicit")
]
```

### Batch Processing Multiple Conditions

```bash
#!/bin/bash
for condition in "salt" "drought" "cold" "heat"; do
    pyner --organism "Arabidopsis thaliana" \
          --condition "${condition} stress" \
          --experiment "RNA-seq" \
          --label "arab_${condition}" \
          --output-dir "./results"
done
```

### Analyzing PRISMA Outputs

```python
from pyner.prisma import PRISMAFlow, ScreeningLog

# Load and analyze flow
flow = PRISMAFlow.load("data/prisma_flows/salt_20241030_prisma_flow.json")
print(flow.generate_text_report())

# Analyze screening decisions
log = ScreeningLog.load("logs/salt_20241030_screening.log")
stats = log.get_statistics()
print(f"Inclusion rate: {stats['inclusion_rate']:.1f}%")
print(f"Exclusion reasons: {stats['exclusion_reasons']}")
```

## Git Workflow for Contributors

This project is hosted at https://github.com/BIOLIMON/Pyner

### Standard Contribution Flow

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Pyner.git
cd Pyner

# 3. Add upstream remote
git remote add upstream https://github.com/BIOLIMON/Pyner.git

# 4. Create feature branch
git checkout -b feature/your-feature-name

# 5. Make changes and commit
git add file1.py file2.py
git commit -m "feat: Add improved tissue inference for GEO datasets"

# 6. Keep branch updated
git fetch upstream
git rebase upstream/main

# 7. Push to your fork
git push origin feature/your-feature-name

# 8. Open Pull Request on GitHub
```

### Commit Message Conventions

Follow conventional commits for clarity:

```
feat: Add new database fetcher for ENA
fix: Correct tissue inference regex in SRA parser
docs: Update PRISMA checklist with new requirements
test: Add unit tests for query builder
refactor: Simplify quality assessment scoring logic
chore: Update dependencies in pyproject.toml
```

### Before Opening PR

1. Format code: `black pyner/`
2. Check linting: `flake8 pyner/`
3. Run tests (when available): `pytest`
4. Update documentation if adding features
5. Test your changes with real NCBI queries
6. Add examples if introducing new functionality

## Contact and Resources

- **Repository**: https://github.com/BIOLIMON/Pyner
- **Issues**: https://github.com/BIOLIMON/Pyner/issues
- **PRISMA 2020**: http://www.prisma-statement.org/
- **NCBI E-utilities**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **Biopython**: https://biopython.org/

For questions about systematic review methodology, consult `docs/PRISMA_CHECKLIST.md`.
