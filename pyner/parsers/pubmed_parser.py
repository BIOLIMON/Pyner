"""
Parser for PubMed summaries.

Extracts structured metadata from PubMed articles.
"""

from typing import List, Dict, Any
import re


class PubMedParser:
    """
    Parser for PubMed summaries.

    Extracts article information including title, authors,
    journal, and publication date.
    """

    def __init__(self):
        """Initialize PubMed parser."""
        pass

    def parse_summaries(self, summaries: List[dict], condition: str) -> List[Dict[str, Any]]:
        """
        Parse list of PubMed summaries.

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
                print(f"  Warning: Failed to parse PubMed {summary.get('Id', 'unknown')}: {e}")
                continue

        return parsed_records

    def parse_single_summary(self, summary: dict, condition: str) -> Dict[str, Any]:
        """
        Parse single PubMed summary.

        Args:
            summary: Summary dictionary from Entrez
            condition: Experimental condition label

        Returns:
            Parsed record dictionary
        """
        # Extract fields
        pmid = summary.get('Id', 'unknown')
        title = summary.get('Title', '')

        # Authors
        author_list = summary.get('AuthorList', [])
        if isinstance(author_list, list) and author_list:
            first_author = author_list[0] if author_list else ''
            authors = ', '.join(author_list[:3])  # First 3 authors
            if len(author_list) > 3:
                authors += ', et al.'
        else:
            first_author = ''
            authors = ''

        # Source (journal)
        source = summary.get('Source', '')
        fulljournalname = summary.get('FullJournalName', '')

        # Publication date
        pub_date = summary.get('PubDate', '')
        epub_date = summary.get('EPubDate', '')

        # DOI
        doi = ''
        article_ids = summary.get('ArticleIds', {})
        if isinstance(article_ids, dict):
            doi = article_ids.get('doi', '')

        # Organism - try to extract from title or mesh terms
        organism = self._extract_organism(summary)

        # Build description from available info
        description_parts = []
        if authors:
            description_parts.append(authors)
        if source:
            description_parts.append(source)
        if pub_date:
            description_parts.append(f"({pub_date})")

        description = '. '.join(description_parts)

        # Build extra metadata
        extra = {
            'authors': authors,
            'first_author': first_author,
            'journal': fulljournalname or source,
            'publication_date': pub_date,
            'epub_date': epub_date,
            'doi': doi,
            'pmid': pmid
        }

        return {
            'Fuente': 'PubMed',
            'Condicion': condition,
            'ID': f"PMID:{pmid}",
            'Title': self._clean_text(title),
            'Description': self._clean_text(description),
            'Organism': organism,
            'Tissue': None,  # PubMed doesn't have tissue info
            'Tissue_confidence': None,
            'Extra': str(extra)
        }

    def _extract_organism(self, summary: dict) -> str:
        """
        Try to extract organism from PubMed summary.

        Looks in title and available metadata.

        Args:
            summary: Summary dictionary

        Returns:
            Organism name if found, empty string otherwise
        """
        # Common model organisms
        organisms = [
            'Arabidopsis thaliana',
            'Oryza sativa',
            'Zea mays',
            'Solanum lycopersicum',
            'Glycine max',
            'Triticum aestivum',
            'Hordeum vulgare',
            'Medicago truncatula',
            'Populus trichocarpa',
            'Vitis vinifera'
        ]

        title = summary.get('Title', '').lower()

        for organism in organisms:
            if organism.lower() in title:
                return organism

        # If not found in common list, return empty
        return ''

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


def parse_pubmed_summary(summaries: List[dict], condition: str) -> List[Dict[str, Any]]:
    """
    Convenience function to parse PubMed summaries.

    Args:
        summaries: List of summary dictionaries
        condition: Experimental condition label

    Returns:
        List of parsed records
    """
    parser = PubMedParser()
    return parser.parse_summaries(summaries, condition)
