"""
BioProject database fetcher.

Retrieves study-level information from NCBI BioProject.
"""

from typing import List
from .ncbi_base import NCBIBaseFetcher
from ..config import Config
from ..query_builder import QueryBuilder


class BioProjectFetcher(NCBIBaseFetcher):
    """
    Fetcher for NCBI BioProject database.

    BioProject provides high-level study information and links
    to related data in other NCBI databases.
    """

    def __init__(self, config: Config):
        """
        Initialize BioProject fetcher.

        Args:
            config: Configuration with NCBI credentials
        """
        super().__init__(config)
        self.db = "bioproject"
        self.query_builder = QueryBuilder()

    def fetch_ids(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> List[str]:
        """
        Search BioProject and return list of project IDs.

        Args:
            organism: Target organism (e.g., "Arabidopsis thaliana")
            condition: Experimental condition (e.g., "salt stress")
            experiment: Experiment type (e.g., "RNA-seq")

        Returns:
            List of BioProject IDs (e.g., ['PRJNA123456', 'PRJNA789012'])

        Example:
            >>> fetcher = BioProjectFetcher(config)
            >>> ids = fetcher.fetch_ids(
            ...     "Arabidopsis thaliana",
            ...     "salt stress",
            ...     "RNA-seq"
            ... )
            >>> print(f"Found {len(ids)} BioProjects")
        """
        # Build query
        query = self.query_builder.build_ncbi_query(
            organism=organism,
            condition=condition,
            experiment=experiment
        )

        print(f"  BioProject query: {query}")

        # Search and return IDs
        ids = self.search_all(self.db, query)

        print(f"  Retrieved {len(ids):,} BioProject IDs")

        return ids

    def fetch_summaries(self, id_list: List[str]) -> List[dict]:
        """
        Fetch detailed summaries for BioProject IDs.

        Args:
            id_list: List of BioProject IDs

        Returns:
            List of summary dictionaries

        Example:
            >>> summaries = fetcher.fetch_summaries(['PRJNA123456'])
            >>> print(summaries[0]['Project_Title'])
        """
        print(f"  Fetching summaries for {len(id_list):,} BioProjects...")

        return super().fetch_summaries(self.db, id_list)


def fetch_bioproject_ids(
    organism: str,
    condition: str,
    experiment: str,
    config: Config
) -> List[str]:
    """
    Convenience function to fetch BioProject IDs.

    Args:
        organism: Target organism
        condition: Experimental condition
        experiment: Experiment type
        config: NCBI configuration

    Returns:
        List of BioProject IDs
    """
    fetcher = BioProjectFetcher(config)
    return fetcher.fetch_ids(organism, condition, experiment)
