"""
Parser for SRA summaries.

Extracts structured metadata from SRA records, including tissue information.
"""

from typing import List, Dict, Any
import re


class SRAParser:
    """
    Parser for NCBI SRA summaries.

    Extracts experiment information including title, library info,
    organism, and tissue annotations.
    """

    def __init__(self):
        """Initialize SRA parser."""
        # Common tissue keywords for inference
        self.tissue_keywords = [
            'root', 'leaf', 'leaves', 'shoot', 'stem', 'flower', 'seed',
            'fruit', 'berry', 'petal', 'sepal', 'carpel', 'stamen',
            'cotyledon', 'hypocotyl', 'radicle', 'meristem', 'bark',
            'xylem', 'phloem', 'pollen', 'ovule', 'embryo', 'endosperm',
            'whole plant', 'seedling', 'callus', 'culture', 'cell'
        ]

    def parse_summaries(self, summaries: List[dict], condition: str) -> List[Dict[str, Any]]:
        """
        Parse list of SRA summaries.

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
                print(f"  Warning: Failed to parse SRA {summary.get('Id', 'unknown')}: {e}")
                continue

        return parsed_records

    def parse_single_summary(self, summary: dict, condition: str) -> Dict[str, Any]:
        """
        Parse single SRA summary.

        Args:
            summary: Summary dictionary from Entrez
            condition: Experimental condition label

        Returns:
            Parsed record dictionary
        """
        # Extract basic fields
        experiment_acc = summary.get('Experiment', summary.get('Id', 'unknown'))
        title = summary.get('Title', '')

        # Extract runs information
        runs = summary.get('Runs', '')
        run_info = self._parse_runs(runs)

        # Organism
        organism = summary.get('Organism', summary.get('ScientificName', ''))

        # Sample information
        sample_name = summary.get('Sample', '')

        # Library information
        library_strategy = summary.get('LibraryStrategy', '')
        library_source = summary.get('LibrarySource', '')
        library_layout = summary.get('LibraryLayout', '')
        platform = summary.get('Platform', '')

        # Combine all text for tissue inference
        full_text = ' '.join([
            title,
            sample_name,
            str(summary.get('ExpXml', '')),
            str(summary.get('BioSample', ''))
        ])

        # Infer tissue
        tissue, confidence = self._infer_tissue(full_text, summary)

        # Build extra metadata
        extra = {
            'runs': run_info,
            'library_strategy': library_strategy,
            'library_source': library_source,
            'library_layout': library_layout,
            'platform': platform,
            'sample': sample_name,
            'biosample': summary.get('BioSample', ''),
        }

        return {
            'Fuente': 'SRA',
            'Condicion': condition,
            'ID': experiment_acc,
            'Title': self._clean_text(title),
            'Description': self._clean_text(f"{library_strategy} from {organism}"),
            'Organism': organism,
            'Tissue': tissue,
            'Tissue_confidence': confidence,
            'Extra': str(extra)
        }

    def _parse_runs(self, runs_data: Any) -> str:
        """
        Parse runs information.

        Args:
            runs_data: Runs data from summary

        Returns:
            Formatted runs information
        """
        if not runs_data:
            return ""

        if isinstance(runs_data, str):
            # Extract run accessions with regex
            run_accs = re.findall(r'(SRR\d+)', runs_data)
            return ', '.join(run_accs[:5])  # Limit to first 5

        return str(runs_data)

    def _infer_tissue(self, text: str, summary: dict) -> tuple[str, str]:
        """
        Infer tissue type from text.

        Args:
            text: Combined text from multiple fields
            summary: Original summary dict

        Returns:
            Tuple of (tissue_name, confidence_level)
        """
        text_lower = text.lower()

        # Check for explicit tissue annotation in BioSample or attributes
        # This would require fetching BioSample XML, which is not done here
        # For now, use keyword-based inference

        for tissue in self.tissue_keywords:
            # Look for tissue keyword with word boundaries
            pattern = r'\b' + re.escape(tissue) + r'\b'
            if re.search(pattern, text_lower):
                return tissue, 'inferred'

        # No tissue found
        return None, 'unknown'

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


def parse_sra_summary(summaries: List[dict], condition: str) -> List[Dict[str, Any]]:
    """
    Convenience function to parse SRA summaries.

    Args:
        summaries: List of summary dictionaries
        condition: Experimental condition label

    Returns:
        List of parsed records
    """
    parser = SRAParser()
    return parser.parse_summaries(summaries, condition)
