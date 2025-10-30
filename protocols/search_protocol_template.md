# Search Protocol Template

**Version:** 1.0
**Date:** YYYY-MM-DD
**Protocol ID:** PROTO-001

## 1. Research Question

Clearly state the research question or objective of the systematic search.

**Example:** *What RNA-seq datasets are available for salt stress response in Arabidopsis thaliana?*

---

## 2. Eligibility Criteria

### 2.1 Inclusion Criteria
- **Organism:**
- **Experimental Condition:**
- **Experiment Type:**
- **Data Availability:**
- **Publication Date Range:**

### 2.2 Exclusion Criteria
-
-
-

---

## 3. Information Sources

### 3.1 Databases
- [ ] NCBI BioProject
- [ ] NCBI SRA (Sequence Read Archive)
- [ ] NCBI GEO (Gene Expression Omnibus)
- [ ] NCBI PubMed
- [ ] Other: ___________

### 3.2 Date of Last Search
-

### 3.3 Search Constraints
- Language restrictions:
- Publication year range:
- Other limitations:

---

## 4. Search Strategy

### 4.1 Search Terms

**Organism Terms:**
```
"Arabidopsis thaliana" OR "A. thaliana" OR [taxonomy_id]
```

**Condition Terms:**
```
"salt stress" OR "salt" OR "NaCl" OR "salinity"
```

**Experiment Type Terms:**
```
"RNA-seq" OR "RNAseq" OR "transcriptome" OR "transcriptomic"
```

### 4.2 Boolean Query Construction

**Final Query:**
```
(organism_terms) AND (condition_terms) AND (experiment_type_terms)
```

### 4.3 Filters Applied
- Data type:
- Organism:
- Study type:
- Date range:

---

## 5. Selection Process

### 5.1 Screening Stages
1. **Identification:** Automated retrieval from databases
2. **Title/Abstract Screening:** Review of titles and descriptions
3. **Metadata Quality Assessment:** Evaluation of completeness
4. **Final Inclusion:** Records meeting all criteria

### 5.2 Number of Reviewers
- Automated screening: 1 (script-based)
- Manual review (if applicable):

### 5.3 Conflict Resolution
- Method for handling ambiguous records:

---

## 6. Data Collection Process

### 6.1 Data Items Extracted
For each record, extract:
- Database source (BioProject, SRA, GEO, PubMed)
- Unique identifier (accession number)
- Title
- Description/Abstract
- Organism
- Tissue type (if available)
- Tissue inference confidence (explicit/inferred/unknown)
- Publication date
- Related publications
- Data availability status

### 6.2 Quality Assessment Criteria

| Criterion | Weight | Assessment Method |
|-----------|--------|-------------------|
| Metadata completeness | High | % of fields populated |
| Title informativeness | Medium | Presence of key terms |
| Tissue information | Medium | Explicit vs. inferred |
| Data accessibility | High | Public availability |

---

## 7. Output Files

### 7.1 Data Files Generated
- `data/raw/[condition]_[date]_raw.csv` - All retrieved records
- `data/processed/[condition]_[date]_processed.csv` - After quality filtering
- `data/excluded/[condition]_[date]_excluded.csv` - Excluded records with reasons

### 7.2 PRISMA Documentation
- `data/prisma_flows/[condition]_[date]_prisma_flow.json` - Flow diagram data
- `logs/[condition]_[date]_screening.log` - Detailed screening log

---

## 8. Risk of Bias Assessment

### 8.1 Sources of Bias
- Database coverage bias (not all datasets may be in NCBI)
- Temporal bias (recent datasets more likely to have complete metadata)
- Language bias (predominantly English-language publications)
- Tissue annotation bias (quality varies by submitter)

### 8.2 Mitigation Strategies
- Query multiple databases
- Document all search parameters and dates
- Record confidence levels for inferred data
- Version control all protocols

---

## 9. Data Synthesis Methods

- Statistical summary of records by database source
- Tissue distribution analysis
- Temporal trends in data availability
- Quality metrics aggregation

---

## 10. Protocol Amendments

| Date | Version | Change Description | Rationale |
|------|---------|-------------------|-----------|
|      |         |                   |           |

---

## 11. Registration

- Protocol registration: [ ] Yes / [ ] No
- Registration platform:
- Registration ID:
- Registration date:

---

## References

List any relevant methodological papers or guidelines followed:
- PRISMA 2020: http://www.prisma-statement.org/
-

---

**Protocol prepared by:** [Name]
**Affiliation:** [Institution/Lab]
**Contact:** [Email]
