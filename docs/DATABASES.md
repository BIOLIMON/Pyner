# RNA-seq and Genomics Databases Integrated in Pyner

This document describes all databases integrated in Pyner for systematic mining of transcriptomics data.

## Overview

Pyner queries multiple international repositories to ensure comprehensive coverage of RNA-seq and genomics data. Databases are organized by geographic location and scope.

---

## NCBI (USA) - National Center for Biotechnology Information

### 1. GEO (Gene Expression Omnibus)
- **URL**: https://www.ncbi.nlm.nih.gov/geo/
- **Content**: Microarray and RNA-seq functional genomics data
- **Data Type**: Processed data, metadata, some raw data
- **Coverage**: >300,000 RNA-seq samples from thousands of experiments
- **Access Method**: NCBI E-utilities API
- **Best For**: Processed expression matrices, experimental design metadata

### 2. SRA (Sequence Read Archive)
- **URL**: https://www.ncbi.nlm.nih.gov/sra
- **Content**: Raw sequencing reads (FASTQ, SRA format)
- **Data Type**: Raw unprocessed reads
- **Coverage**: Millions of sequencing runs across all organisms
- **Access Method**: NCBI E-utilities API
- **Best For**: Raw RNA-seq reads, library information, sequencing platform details

### 3. BioProject
- **URL**: https://www.ncbi.nlm.nih.gov/bioproject/
- **Content**: High-level study/project information
- **Data Type**: Project metadata, links to related data
- **Coverage**: Parent records linking multiple datasets
- **Access Method**: NCBI E-utilities API
- **Best For**: Study-level information, publication links, experimental overview

### 4. PubMed
- **URL**: https://pubmed.ncbi.nlm.nih.gov/
- **Content**: Biomedical literature
- **Data Type**: Publication metadata, abstracts
- **Coverage**: >35 million citations
- **Access Method**: NCBI E-utilities API
- **Best For**: Finding related publications, methods descriptions

---

## EMBL-EBI (Europe) - European Bioinformatics Institute

### 5. ENA (European Nucleotide Archive)
- **URL**: https://www.ebi.ac.uk/ena
- **Content**: Raw sequencing reads (equivalent to SRA)
- **Data Type**: Raw reads, assemblies, annotations
- **Coverage**: Mirrors SRA data plus Europe-submitted data
- **Access Method**: ENA REST API
- **Best For**: European submissions, alternative to SRA
- **Note**: Part of INSDC (International Nucleotide Sequence Database Collaboration)

### 6. BioStudies (formerly ArrayExpress)
- **URL**: https://www.ebi.ac.uk/biostudies/
- **Content**: Functional genomics studies
- **Data Type**: Processed data, experimental metadata
- **Coverage**: Replaced ArrayExpress in 2021
- **Access Method**: BioStudies REST API
- **Best For**: European functional genomics submissions
- **Note**: ArrayExpress stopped importing from GEO in 2017

---

## Plant-Specific Databases (Optional)

### 7. PlantExp
- **URL**: Not directly accessible via API
- **Content**: Plant-specific RNA-seq data
- **Data Type**: Aggregated from public repositories
- **Coverage**: 131,432 samples, 8,303 studies, 85 plant species
- **Access Method**: Web interface only (no public API)
- **Best For**: Plant-specific curated datasets
- **Status**: Not implemented in current version (web scraping required)

### 8. Plant Public RNA-seq Database (PPRD)
- **URL**: https://plantrnadb.com/
- **Content**: Curated plant RNA-seq libraries
- **Data Type**: Expression data for major crops
- **Coverage**: Maize (19,664), Rice (11,726), Soybean (4,085), Wheat (5,816), Cotton (3,483)
- **Access Method**: Web interface
- **Best For**: Major crop species
- **Status**: Not implemented (aggregates from NCBI/EBI)

### 9. Ensembl Plants
- **URL**: https://plants.ensembl.org/
- **Content**: Plant genomes and annotations
- **Data Type**: Reference genomes, gene annotations, RNA-seq tracks
- **Coverage**: Hundreds of plant species
- **Access Method**: REST API
- **Best For**: Reference genomes, gene IDs, annotations
- **Status**: Future integration planned

---

## Other International Repositories (Not Currently Integrated)

### DDBJ (Japan)
- **DRA (DDBJ Read Archive)**: Japanese equivalent of SRA/ENA
- **URL**: https://www.ddbj.nig.ac.jp/dra/
- **Note**: Part of INSDC, data mirrored to SRA/ENA

### GSA (China)
- **Genome Sequence Archive**: Chinese repository
- **URL**: https://ngdc.cncb.ac.cn/gsa/
- **Note**: Independent but growing repository

---

## Database Selection Strategy

Pyner implements a **tiered search strategy**:

### Tier 1: Primary NCBI Databases (Always Searched)
1. BioProject - Study-level information
2. SRA - Library-level information with tissue metadata
3. GEO - Processed datasets with experimental design
4. PubMed - Related publications

### Tier 2: European Alternatives (Optional, for broader coverage)
5. ENA - Alternative to SRA
6. BioStudies - Alternative to GEO

### Tier 3: Specialized Databases (Future)
7. Ensembl Plants - For gene-level queries
8. Plant-specific repositories

---

## Data Relationships

```
BioProject (Study)
    ├── SRA Experiments (Libraries)
    │   └── SRA Runs (Raw FASTQ files)
    ├── GEO Series (GSE)
    │   └── GEO Samples (GSM)
    └── PubMed (Publications)

ENA (mirrors SRA structure)
BioStudies (similar to GEO)
```

---

## API Access Requirements

### NCBI E-utilities
- **Email**: Required (set in config)
- **API Key**: Optional but strongly recommended
- **Rate Limits**:
  - Without API key: 3 requests/second
  - With API key: 10 requests/second
- **Documentation**: https://www.ncbi.nlm.nih.gov/books/NBK25501/

### ENA REST API
- **Authentication**: Not required for public data
- **Rate Limits**: 20 requests/second (no authentication needed)
- **Documentation**: https://www.ebi.ac.uk/ena/portal/api/

### BioStudies REST API
- **Authentication**: Not required for public data
- **Documentation**: https://www.ebi.ac.uk/biostudies/help

---

## Coverage Comparison

| Database | Type | Geographic | RNA-seq Samples | Raw Reads |
|----------|------|-----------|-----------------|-----------|
| GEO | Functional genomics | Global | ~300,000+ | Limited |
| SRA | Raw sequencing | Global | Millions | Yes |
| BioProject | Study metadata | Global | N/A | No |
| PubMed | Literature | Global | N/A | No |
| ENA | Raw sequencing | Europe-focused | Millions | Yes |
| BioStudies | Functional genomics | Europe-focused | Thousands | No |

---

## Implementation Status

| Database | Fetcher | Parser | Status |
|----------|---------|--------|--------|
| BioProject | ✅ | ✅ | Implemented |
| SRA | ✅ | ✅ | Implemented |
| GEO | ✅ | ✅ | Implemented |
| PubMed | ✅ | ✅ | Implemented |
| ENA | ✅ | ✅ | Implemented |
| BioStudies | ✅ | ✅ | Implemented |
| PlantExp | ❌ | ❌ | Planned |
| Ensembl Plants | ❌ | ❌ | Planned |

---

## Data Deduplication

Since databases mirror each other (SRA ↔ ENA), Pyner implements deduplication:
- Uses accession number as unique identifier
- Prioritizes NCBI records when duplicates exist
- Logs source of each record for provenance tracking

---

## References

1. INSDC (International Nucleotide Sequence Database Collaboration)
   - https://www.insdc.org/

2. Gene Expression Repositories Explained
   - https://www.ccdatalab.org/blog/gene-expression-repositories-explained

3. PlantExp: Platform for plant RNA-seq exploration
   - https://academic.oup.com/nar/article/51/D1/D1483/6769746

4. Plant Public RNA-seq Database
   - https://doi.org/10.1111/pbi.13798

5. Exploiting plant transcriptomic databases
   - https://doi.org/10.1016/j.pld.2022.05.003
