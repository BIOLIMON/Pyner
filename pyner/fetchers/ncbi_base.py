"""
Base fetcher for NCBI databases.

Provides common functionality for all NCBI E-utilities queries.
"""

from Bio import Entrez
import time
from typing import List, Optional
from ..config import Config


class NCBIBaseFetcher:
    """
    Base class for NCBI database fetchers.

    Handles authentication, rate limiting, and common query patterns.
    """

    def __init__(self, config: Config):
        """
        Initialize NCBI fetcher.

        Args:
            config: Configuration with NCBI credentials
        """
        self.config = config
        Entrez.email = config.email
        if config.api_key:
            Entrez.api_key = config.api_key

    def search(
        self,
        db: str,
        term: str,
        retmax: int = 10000,
        retstart: int = 0
    ) -> List[str]:
        """
        Search NCBI database and return list of IDs.

        Args:
            db: Database name (bioproject, sra, gds, pubmed)
            term: Search query
            retmax: Maximum results to return
            retstart: Starting index for pagination

        Returns:
            List of database IDs
        """
        try:
            time.sleep(self.config.rate_limit)

            handle = Entrez.esearch(
                db=db,
                term=term,
                retmax=retmax,
                retstart=retstart,
                usehistory="y"  # Use history for large result sets
            )

            record = Entrez.read(handle)
            handle.close()

            return record.get("IdList", [])

        except Exception as e:
            print(f"Error searching {db}: {e}")
            return []

    def search_all(
        self,
        db: str,
        term: str,
        batch_size: Optional[int] = None
    ) -> List[str]:
        """
        Search database and retrieve all results using pagination.

        Args:
            db: Database name
            term: Search query
            batch_size: Number of IDs per batch (uses config default if None)

        Returns:
            Complete list of IDs
        """
        if batch_size is None:
            batch_size = self.config.batch_size

        all_ids = []
        retstart = 0

        # First query to get total count
        time.sleep(self.config.rate_limit)
        handle = Entrez.esearch(
            db=db,
            term=term,
            retmax=0,
            usehistory="y"
        )
        record = Entrez.read(handle)
        handle.close()

        count = int(record.get("Count", 0))

        if count == 0:
            return []

        print(f"  Found {count:,} records in {db}")

        # Fetch in batches
        while retstart < count:
            batch_ids = self.search(db, term, retmax=batch_size, retstart=retstart)
            all_ids.extend(batch_ids)
            retstart += batch_size

            if len(batch_ids) < batch_size:
                break

        return all_ids

    def fetch_summaries(
        self,
        db: str,
        id_list: List[str],
        batch_size: Optional[int] = None
    ) -> List[dict]:
        """
        Fetch summaries for list of IDs.

        Args:
            db: Database name
            id_list: List of database IDs
            batch_size: Number of IDs per batch

        Returns:
            List of summary records
        """
        if not id_list:
            return []

        if batch_size is None:
            batch_size = self.config.batch_size

        all_records = []

        # Process in batches to avoid overwhelming the API
        for i in range(0, len(id_list), batch_size):
            batch = id_list[i:i + batch_size]

            try:
                time.sleep(self.config.rate_limit)

                handle = Entrez.esummary(
                    db=db,
                    id=",".join(batch)
                )

                records = Entrez.read(handle)
                handle.close()

                # Handle different return formats
                if isinstance(records, list):
                    all_records.extend(records)
                elif isinstance(records, dict):
                    # Some databases return dict with 'DocumentSummarySet'
                    if 'DocumentSummarySet' in records:
                        doc_sum = records['DocumentSummarySet']
                        if 'DocumentSummary' in doc_sum:
                            all_records.extend(doc_sum['DocumentSummary'])
                    else:
                        all_records.append(records)

            except Exception as e:
                print(f"Error fetching summaries from {db} for batch {i//batch_size + 1}: {e}")
                continue

        return all_records

    def fetch_xml(
        self,
        db: str,
        id_list: List[str],
        rettype: str = "xml",
        retmode: str = "xml"
    ) -> str:
        """
        Fetch full XML records for list of IDs.

        Args:
            db: Database name
            id_list: List of database IDs
            rettype: Return type (xml, fasta, gb, etc.)
            retmode: Return mode (xml, text, etc.)

        Returns:
            XML string
        """
        if not id_list:
            return ""

        try:
            time.sleep(self.config.rate_limit)

            handle = Entrez.efetch(
                db=db,
                id=",".join(id_list),
                rettype=rettype,
                retmode=retmode
            )

            xml_data = handle.read()
            handle.close()

            return xml_data

        except Exception as e:
            print(f"Error fetching XML from {db}: {e}")
            return ""
