"""
GEO (Gene Expression Omnibus) database fetcher.

Retrieves functional genomics data from NCBI GEO.
"""

from typing import List
from .ncbi_base import NCBIBaseFetcher
from ..config import Config
from ..query_builder import QueryBuilder


class GEOFetcher(NCBIBaseFetcher):
    """
    Fetcher for NCBI GEO database.

    GEO contains processed gene expression data and experimental metadata.
    """

    def __init__(self, config: Config):
        """
        Initialize GEO fetcher.

        Args:
            config: Configuration with NCBI credentials
        """
        super().__init__(config)
        self.db = "gds"  # GEO DataSets database
        self.query_builder = QueryBuilder()

    def fetch_ids(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> List[str]:
        """
        Search GEO and return list of dataset IDs.

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            List of GEO IDs (e.g., ['200123456', '200789012'])
            Note: These are internal GDS IDs, not GSE accessions

        Example:
            >>> fetcher = GEOFetcher(config)
            >>> ids = fetcher.fetch_ids(
            ...     "Arabidopsis thaliana",
            ...     "salt stress",
            ...     "RNA-seq"
            ... )
        """
        # Build GEO-specific query
        query = self.query_builder.build_geo_query(
            organism=organism,
            condition=condition,
            experiment=experiment
        )

        print(f"  GEO query: {query}")

        # Search and return IDs
        ids = self.search_all(self.db, query)

        print(f"  Retrieved {len(ids):,} GEO IDs")

        return ids

    def fetch_summaries(self, id_list: List[str]) -> List[dict]:
        """
        Fetch detailed summaries for GEO IDs.

        Args:
            id_list: List of GEO IDs

        Returns:
            List of summary dictionaries
        """
        print(f"  Fetching summaries for {len(id_list):,} GEO datasets...")

        return super().fetch_summaries(self.db, id_list)


def fetch_geo_ids(
    organism: str,
    condition: str,
    experiment: str,
    config: Config
) -> List[str]:
    """
    Convenience function to fetch GEO IDs.

    Args:
        organism: Target organism
        condition: Experimental condition
        experiment: Experiment type
        config: NCBI configuration

    Returns:
        List of GEO IDs
    """
    fetcher = GEOFetcher(config)
    return fetcher.fetch_ids(organism, condition, experiment)
