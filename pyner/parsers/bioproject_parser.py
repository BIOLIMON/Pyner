"""
Parser for BioProject summaries.

Extracts structured metadata from BioProject records.
"""

from typing import List, Dict, Any
import re


class BioProjectParser:
    """
    Parser for NCBI BioProject summaries.

    Extracts project information including title, description,
    organism, and project type.
    """

    def __init__(self):
        """Initialize BioProject parser."""
        pass

    def parse_summaries(self, summaries: List[dict], condition: str) -> List[Dict[str, Any]]:
        """
        Parse list of BioProject summaries.

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
                print(f"  Warning: Failed to parse BioProject {summary.get('Id', 'unknown')}: {e}")
                continue

        return parsed_records

    def parse_single_summary(self, summary: dict, condition: str) -> Dict[str, Any]:
        """
        Parse single BioProject summary.

        Args:
            summary: Summary dictionary from Entrez
            condition: Experimental condition label

        Returns:
            Parsed record dictionary
        """
        # Extract fields with safe defaults
        project_id = summary.get('Project_Acc', summary.get('Id', 'unknown'))
        title = summary.get('Project_Title', '')
        description = summary.get('Project_Description', '')

        # Organism information
        organism_name = summary.get('Organism_Name', '')
        if not organism_name and 'Organism' in summary:
            organism_info = summary['Organism']
            if isinstance(organism_info, dict):
                organism_name = organism_info.get('OrganismName', '')
            elif isinstance(organism_info, str):
                organism_name = organism_info

        # Project data type
        project_data_type = summary.get('Project_Data_Type', '')
        if isinstance(project_data_type, list):
            project_data_type = ', '.join(project_data_type)

        # Registration date
        reg_date = summary.get('Registration_Date', '')

        # Build extra metadata
        extra = {
            'project_data_type': project_data_type,
            'registration_date': reg_date,
            'project_subtype': summary.get('Project_Subtype', ''),
        }

        return {
            'Fuente': 'BioProject',
            'Condicion': condition,
            'ID': project_id,
            'Title': self._clean_text(title),
            'Description': self._clean_text(description),
            'Organism': organism_name,
            'Tissue': None,  # BioProject doesn't have tissue info
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

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text


def parse_bioproject_summary(summaries: List[dict], condition: str) -> List[Dict[str, Any]]:
    """
    Convenience function to parse BioProject summaries.

    Args:
        summaries: List of summary dictionaries
        condition: Experimental condition label

    Returns:
        List of parsed records
    """
    parser = BioProjectParser()
    return parser.parse_summaries(summaries, condition)
