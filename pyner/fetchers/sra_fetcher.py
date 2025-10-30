"""
SRA (Sequence Read Archive) database fetcher.

Retrieves sequencing library information from NCBI SRA.
"""

from typing import List
from .ncbi_base import NCBIBaseFetcher
from ..config import Config
from ..query_builder import QueryBuilder


class SRAFetcher(NCBIBaseFetcher):
    """
    Fetcher for NCBI SRA database.

    SRA contains raw sequencing data and library metadata,
    including tissue information for many samples.
    """

    def __init__(self, config: Config):
        """
        Initialize SRA fetcher.

        Args:
            config: Configuration with NCBI credentials
        """
        super().__init__(config)
        self.db = "sra"
        self.query_builder = QueryBuilder()

    def fetch_ids(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> List[str]:
        """
        Search SRA and return list of experiment IDs.

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            List of SRA IDs (e.g., ['SRX123456', 'SRX789012'])

        Example:
            >>> fetcher = SRAFetcher(config)
            >>> ids = fetcher.fetch_ids(
            ...     "Arabidopsis thaliana",
            ...     "salt stress",
            ...     "RNA-seq"
            ... )
        """
        # Build SRA-specific query
        query = self.query_builder.build_sra_query(
            organism=organism,
            condition=condition,
            experiment=experiment
        )

        print(f"  SRA query: {query}")

        # Search and return IDs
        ids = self.search_all(self.db, query)

        print(f"  Retrieved {len(ids):,} SRA IDs")

        return ids

    def fetch_summaries(self, id_list: List[str]) -> List[dict]:
        """
        Fetch detailed summaries for SRA IDs.

        Note: SRA summaries can be complex and may require
        additional parsing to extract tissue information.

        Args:
            id_list: List of SRA IDs

        Returns:
            List of summary dictionaries
        """
        print(f"  Fetching summaries for {len(id_list):,} SRA experiments...")

        return super().fetch_summaries(self.db, id_list)


def fetch_sra_ids(
    organism: str,
    condition: str,
    experiment: str,
    config: Config
) -> List[str]:
    """
    Convenience function to fetch SRA IDs.

    Args:
        organism: Target organism
        condition: Experimental condition
        experiment: Experiment type
        config: NCBI configuration

    Returns:
        List of SRA IDs
    """
    fetcher = SRAFetcher(config)
    return fetcher.fetch_ids(organism, condition, experiment)
