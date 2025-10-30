"""
PubMed database fetcher.

Retrieves biomedical literature related to RNA-seq studies.
"""

from typing import List
from .ncbi_base import NCBIBaseFetcher
from ..config import Config
from ..query_builder import QueryBuilder


class PubMedFetcher(NCBIBaseFetcher):
    """
    Fetcher for PubMed database.

    PubMed contains biomedical literature citations and abstracts.
    """

    def __init__(self, config: Config):
        """
        Initialize PubMed fetcher.

        Args:
            config: Configuration with NCBI credentials
        """
        super().__init__(config)
        self.db = "pubmed"
        self.query_builder = QueryBuilder()

    def fetch_ids(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> List[str]:
        """
        Search PubMed and return list of PMIDs.

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            List of PubMed IDs (PMIDs)

        Example:
            >>> fetcher = PubMedFetcher(config)
            >>> ids = fetcher.fetch_ids(
            ...     "Arabidopsis thaliana",
            ...     "salt stress",
            ...     "RNA-seq"
            ... )
        """
        # Build query
        query = self.query_builder.build_ncbi_query(
            organism=organism,
            condition=condition,
            experiment=experiment
        )

        print(f"  PubMed query: {query}")

        # Search and return IDs
        ids = self.search_all(self.db, query)

        print(f"  Retrieved {len(ids):,} PubMed IDs")

        return ids

    def fetch_summaries(self, id_list: List[str]) -> List[dict]:
        """
        Fetch detailed summaries for PubMed IDs.

        Args:
            id_list: List of PMIDs

        Returns:
            List of summary dictionaries
        """
        print(f"  Fetching summaries for {len(id_list):,} PubMed articles...")

        return super().fetch_summaries(self.db, id_list)


def fetch_pubmed_ids(
    organism: str,
    condition: str,
    experiment: str,
    config: Config
) -> List[str]:
    """
    Convenience function to fetch PubMed IDs.

    Args:
        organism: Target organism
        condition: Experimental condition
        experiment: Experiment type
        config: NCBI configuration

    Returns:
        List of PubMed IDs
    """
    fetcher = PubMedFetcher(config)
    return fetcher.fetch_ids(organism, condition, experiment)
