"""
Parser for GEO summaries.

Extracts structured metadata from GEO DataSet records.
"""

from typing import List, Dict, Any
import re


class GEOParser:
    """
    Parser for NCBI GEO summaries.

    Extracts dataset information including title, summary,
    organism, and platform details.
    """

    def __init__(self):
        """Initialize GEO parser."""
        pass

    def parse_summaries(self, summaries: List[dict], condition: str) -> List[Dict[str, Any]]:
        """
        Parse list of GEO summaries.

        Args:
            summaries: List of summary dictionaries from Entrez
            condition: Experimental condition label

        Returns:
            List of parsed records in standard format
        """
        parsed_records = []

        for summary in summaries:
            try:
                record = self.parse_single_summary(summary, condition)
                if record:
                    parsed_records.append(record)
            except Exception as e:
                print(f"  Warning: Failed to parse GEO {summary.get('Id', 'unknown')}: {e}")
                continue

        return parsed_records

    def parse_single_summary(self, summary: dict, condition: str) -> Dict[str, Any]:
        """
        Parse single GEO summary.

        Args:
            summary: Summary dictionary from Entrez
            condition: Experimental condition label

        Returns:
            Parsed record dictionary
        """
        # Extract fields
        gds_id = summary.get('Accession', summary.get('Id', 'unknown'))
        title = summary.get('title', '')
        summary_text = summary.get('summary', '')

        # Organism
        organism = summary.get('taxon', '')

        # Platform and sample information
        platform_technology = summary.get('PlatformTechnology', '')
        platform_organism = summary.get('PlatformOrganism', '')
        sample_count = summary.get('n_samples', 0)

        # Dataset type
        dataset_type = summary.get('entryType', '')
        gse = summary.get('GSE', '')  # Related GSE series

        # Publication date
        pub_date = summary.get('PDAT', '')

        # FTP link
        ftp_link = summary.get('FTPLink', '')

        # Build extra metadata
        extra = {
            'platform_technology': platform_technology,
            'platform_organism': platform_organism,
            'n_samples': sample_count,
            'dataset_type': dataset_type,
            'gse': gse,
            'publication_date': pub_date,
            'ftp_link': ftp_link
        }

        # Combine title and summary for description
        description = f"{title}. {summary_text}" if summary_text else title

        return {
            'Fuente': 'GEO',
            'Condicion': condition,
            'ID': gds_id,
            'Title': self._clean_text(title),
            'Description': self._clean_text(description),
            'Organism': organism,
            'Tissue': None,  # GEO summaries don't typically include tissue
            'Tissue_confidence': None,
            'Extra': str(extra)
        }

    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and newlines.

        Args:
            text: Raw text

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text


def parse_geo_summary(summaries: List[dict], condition: str) -> List[Dict[str, Any]]:
    """
    Convenience function to parse GEO summaries.

    Args:
        summaries: List of summary dictionaries
        condition: Experimental condition label

    Returns:
        List of parsed records
    """
    parser = GEOParser()
    return parser.parse_summaries(summaries, condition)
