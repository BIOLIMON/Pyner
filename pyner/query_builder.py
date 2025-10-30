"""
Query builder for constructing database-specific search queries.

Handles different query syntaxes for NCBI, EBI, and other databases.
"""

from typing import List, Dict, Optional


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
            "(Arabidopsis thaliana[Organism]) AND (salt stress OR salt OR NaCl) AND (RNA-seq OR RNAseq OR transcriptome)"
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

        SRA allows additional filters like strategy:RNA-Seq

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            SRA-optimized query
        """
        base_query = self.build_ncbi_query(organism, condition, experiment)

        # Add SRA-specific filters
        strategy_filter = ""
        if "rna" in experiment.lower() or "transcriptome" in experiment.lower():
            strategy_filter = " AND strategy_rna_seq[Properties]"

        return base_query + strategy_filter

    def build_geo_query(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> str:
        """
        Build query for GEO database.

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            GEO-optimized query
        """
        base_query = self.build_ncbi_query(organism, condition, experiment)

        # Add GEO-specific filters for expression data
        if "rna" in experiment.lower():
            base_query += " AND expression profiling by high throughput sequencing[DataSet Type]"

        return base_query

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
        Expand condition with synonyms.

        Args:
            condition: Experimental condition
            separator: Separator for terms

        Returns:
            Expanded condition string with synonyms
        """
        terms = [condition]

        # Define common synonyms
        synonyms = {
            "salt": ["salt stress", "salt", "NaCl", "salinity", "sodium chloride"],
            "drought": ["drought", "water deficit", "water stress", "dehydration"],
            "cold": ["cold stress", "cold", "low temperature", "chilling"],
            "heat": ["heat stress", "heat", "high temperature"],
            "uv": ["UV", "UV-B", "ultraviolet", "UV radiation"],
            "oxidative": ["oxidative stress", "H2O2", "hydrogen peroxide", "ROS"],
            "pathogen": ["pathogen", "infection", "disease", "biotic stress"],
            "nutrient": ["nutrient", "nitrogen", "phosphorus", "deficiency"]
        }

        # Check if condition matches any synonym category
        condition_lower = condition.lower()
        for key, synonym_list in synonyms.items():
            if key in condition_lower:
                terms = synonym_list
                break

        return separator.join(terms)

    def _expand_experiment(self, experiment: str, separator: str = " OR ") -> str:
        """
        Expand experiment type with variations.

        Args:
            experiment: Experiment type
            separator: Separator for terms

        Returns:
            Expanded experiment string
        """
        terms = [experiment]

        # RNA-seq variations
        if "rna" in experiment.lower():
            terms = [
                "RNA-seq",
                "RNAseq",
                "RNA seq",
                "transcriptome",
                "transcriptomic",
                "transcriptomics"
            ]

        # ChIP-seq variations
        elif "chip" in experiment.lower():
            terms = [
                "ChIP-seq",
                "ChIPseq",
                "ChIP seq",
                "chromatin immunoprecipitation"
            ]

        # ATAC-seq variations
        elif "atac" in experiment.lower():
            terms = [
                "ATAC-seq",
                "ATACseq",
                "ATAC seq"
            ]

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
