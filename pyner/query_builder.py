"""
Query builder for constructing database-specific search queries.

Handles different query syntaxes for NCBI, EBI, and other databases.
Supports diverse plant bioinformatics experiments beyond just RNA-seq.
"""

from typing import List, Dict, Optional
from .domain_vocabularies import CONDITION_SYNONYMS, EXPERIMENT_SYNONYMS


class QueryBuilder:
    """
    Constructs search queries for different databases.

    Handles organism names, conditions, experiment types, and database-specific
    syntax requirements.
    """

    def __init__(self):
        """Initialize query builder."""
        pass

    def build_ncbi_query(
        self,
        organism: str,
        condition: str,
        experiment: str,
        additional_terms: Optional[List[str]] = None
    ) -> str:
        """
        Build query for NCBI databases (BioProject, SRA, GEO, PubMed).

        NCBI E-utilities use a specific query syntax with boolean operators.

        Args:
            organism: Target organism (e.g., "Arabidopsis thaliana")
            condition: Experimental condition (e.g., "salt stress")
            experiment: Experiment type (e.g., "RNA-seq")
            additional_terms: Optional additional search terms

        Returns:
            Formatted query string

        Example:
            >>> builder = QueryBuilder()
            >>> query = builder.build_ncbi_query(
            ...     "Arabidopsis thaliana",
            ...     "salt stress",
            ...     "RNA-seq"
            ... )
            >>> print(query)
            "(Arabidopsis thaliana[Organism]) AND (salt stress OR salt OR NaCl OR salinity OR sodium chloride OR saline OR ionic stress) AND (RNA-seq OR RNAseq OR RNA seq OR transcriptome OR transcriptomic OR transcriptomics)"
        """
        # Expand organism (add common variations)
        organism_terms = self._expand_organism(organism)

        # Expand condition (add synonyms)
        condition_terms = self._expand_condition(condition)

        # Expand experiment type
        experiment_terms = self._expand_experiment(experiment)

        # Build query with boolean operators
        query_parts = []

        if organism_terms:
            query_parts.append(f"({organism_terms})")

        if condition_terms:
            query_parts.append(f"({condition_terms})")

        if experiment_terms:
            query_parts.append(f"({experiment_terms})")

        if additional_terms:
            for term in additional_terms:
                query_parts.append(f"({term})")

        return " AND ".join(query_parts)

    def build_sra_query(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> str:
        """
        Build query specifically for SRA database.

        SRA allows additional filters by library strategy (RNA-Seq, WGS, ChIP-Seq, etc.)

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            SRA-optimized query with strategy filters
        """
        base_query = self.build_ncbi_query(organism, condition, experiment)

        # Add SRA-specific strategy filters based on experiment type
        strategy_filter = ""
        experiment_lower = experiment.lower()

        # Map experiment types to SRA strategies
        if any(term in experiment_lower for term in ["rna", "transcriptome"]):
            strategy_filter = " AND strategy_rna_seq[Properties]"
        elif any(term in experiment_lower for term in ["chip", "chromatin immunoprecipitation"]):
            strategy_filter = " AND strategy_chip_seq[Properties]"
        elif "atac" in experiment_lower:
            strategy_filter = " AND strategy_atac_seq[Properties]"
        elif any(term in experiment_lower for term in ["bisulfite", "methylation"]):
            strategy_filter = " AND strategy_bisulfite_seq[Properties]"
        elif any(term in experiment_lower for term in ["wgs", "whole genome"]):
            strategy_filter = " AND strategy_wgs[Properties]"

        return base_query + strategy_filter

    def build_geo_query(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> str:
        """
        Build query for GEO database.

        GEO contains expression profiling, genome binding/occupancy, methylation, and other data types.

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            GEO-optimized query with dataset type filters
        """
        base_query = self.build_ncbi_query(organism, condition, experiment)

        # Add GEO-specific filters based on experiment type
        experiment_lower = experiment.lower()
        dataset_filter = ""

        if any(term in experiment_lower for term in ["rna", "transcriptome"]):
            dataset_filter = " AND expression profiling by high throughput sequencing[DataSet Type]"
        elif any(term in experiment_lower for term in ["chip", "binding"]):
            dataset_filter = " AND genome binding/occupancy profiling by high throughput sequencing[DataSet Type]"
        elif any(term in experiment_lower for term in ["methylation", "bisulfite"]):
            dataset_filter = " AND methylation profiling by high throughput sequencing[DataSet Type]"
        elif "microarray" in experiment_lower:
            dataset_filter = " AND expression profiling by array[DataSet Type]"

        return base_query + dataset_filter

    def build_ena_query(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> Dict[str, str]:
        """
        Build query parameters for ENA Portal API.

        ENA uses a different query format (key-value parameters).

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            Dictionary of query parameters for ENA API
        """
        # ENA uses different parameter names
        query_parts = []

        # Organism
        organism_expanded = self._expand_organism(organism, separator=" OR ")
        query_parts.append(f"({organism_expanded})")

        # Condition
        condition_expanded = self._expand_condition(condition, separator=" OR ")
        query_parts.append(f"({condition_expanded})")

        # Experiment
        experiment_expanded = self._expand_experiment(experiment, separator=" OR ")
        query_parts.append(f"({experiment_expanded})")

        full_query = " AND ".join(query_parts)

        return {
            "query": full_query,
            "result": "read_run",  # or "read_experiment"
            "fields": "all",
            "format": "json",
            "limit": "0"  # Will be set dynamically
        }

    def build_biostudies_query(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> Dict[str, str]:
        """
        Build query for BioStudies API.

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            Dictionary of query parameters
        """
        # BioStudies simple text search
        query_terms = [
            self._expand_organism(organism, separator=" "),
            self._expand_condition(condition, separator=" "),
            self._expand_experiment(experiment, separator=" ")
        ]

        query_text = " ".join(query_terms)

        return {
            "query": query_text,
            "pageSize": "100",
            "page": "1"
        }

    def _expand_organism(self, organism: str, separator: str = " OR ") -> str:
        """
        Expand organism name with common variations.

        Args:
            organism: Scientific name (e.g., "Arabidopsis thaliana")
            separator: Separator for terms (default: " OR ")

        Returns:
            Expanded organism string
        """
        terms = [organism]

        # Add abbreviated form
        parts = organism.split()
        if len(parts) >= 2:
            abbreviated = f"{parts[0][0]}. {parts[1]}"
            terms.append(abbreviated)

            # Add genus only
            terms.append(parts[0])

        # Add with [Organism] field tag for NCBI
        if separator == " OR ":
            terms_with_tags = [f"{term}[Organism]" for term in terms]
            return separator.join(terms_with_tags)
        else:
            return separator.join(terms)

    def _expand_condition(self, condition: str, separator: str = " OR ") -> str:
        """
        Expand condition with synonyms from domain vocabularies.

        Supports diverse plant conditions including:
        - Abiotic stress (salt, drought, cold, heat, UV, etc.)
        - Biotic stress (pathogen, herbivory, elicitor)
        - Hormones (auxin, cytokinin, ABA, ethylene, etc.)
        - Development (flowering, germination, senescence, etc.)
        - Treatments (chemical, light, circadian)

        Args:
            condition: Experimental condition
            separator: Separator for terms

        Returns:
            Expanded condition string with synonyms
        """
        terms = [condition]

        # Check if condition matches any synonym category from domain vocabularies
        condition_lower = condition.lower()
        for key, synonym_list in CONDITION_SYNONYMS.items():
            if key in condition_lower or any(syn.lower() in condition_lower for syn in synonym_list):
                terms = synonym_list
                break

        return separator.join(terms)

    def _expand_experiment(self, experiment: str, separator: str = " OR ") -> str:
        """
        Expand experiment type with variations from domain vocabularies.

        Supports diverse plant bioinformatics experiments including:
        - Transcriptomics: RNA-seq, single-cell RNA-seq, microarray, small RNA
        - Genomics: WGS, resequencing, targeted sequencing, ddRAD
        - Epigenomics: ChIP-seq, ATAC-seq, bisulfite-seq, DNase-seq, MNase-seq
        - Proteomics: proteomics, phosphoproteomics
        - Other: Hi-C, CLIP-seq, ribosome profiling, degradome, ChIA-PET

        Args:
            experiment: Experiment type
            separator: Separator for terms

        Returns:
            Expanded experiment string with variations
        """
        terms = [experiment]

        # Check if experiment matches any synonym category from domain vocabularies
        experiment_lower = experiment.lower()
        for key, synonym_list in EXPERIMENT_SYNONYMS.items():
            if key in experiment_lower or any(syn.lower() in experiment_lower for syn in synonym_list):
                terms = synonym_list
                break

        return separator.join(terms)

    def validate_query(self, query: str) -> bool:
        """
        Validate that query is well-formed.

        Args:
            query: Query string to validate

        Returns:
            True if valid, False otherwise
        """
        if not query or not query.strip():
            return False

        # Check for balanced parentheses
        if query.count("(") != query.count(")"):
            return False

        # Check for empty parentheses
        if "()" in query:
            return False

        return True
