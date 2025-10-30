"""
PRISMA Flow Diagram Generator.

Tracks and visualizes the systematic review process following PRISMA guidelines.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class PRISMAFlow:
    """
    Manages PRISMA flow diagram data for systematic data mining.

    Tracks the number of records at each stage:
    - Identification: Records retrieved from each database
    - Screening: Records after initial filtering
    - Exclusion: Records removed (with reasons)
    - Inclusion: Final dataset

    Example:
        >>> flow = PRISMAFlow(condition="salt_stress")
        >>> flow.add_identified("BioProject", 150)
        >>> flow.add_identified("SRA", 1200)
        >>> flow.add_excluded(50, reason="Missing tissue information")
        >>> flow.save()
    """

    def __init__(self, condition: str, label: Optional[str] = None):
        """
        Initialize PRISMA flow tracker.

        Args:
            condition: Experimental condition being searched
            label: Short label for output files (defaults to condition)
        """
        self.condition = condition
        self.label = label or condition
        self.timestamp = datetime.now().isoformat()

        self.data = {
            "metadata": {
                "condition": condition,
                "label": label,
                "timestamp": self.timestamp
            },
            "identification": {
                "databases": {},  # {db_name: count}
                "total": 0
            },
            "screening": {
                "records_screened": 0,
                "records_excluded": 0,
                "exclusion_reasons": {}  # {reason: count}
            },
            "included": {
                "total": 0,
                "by_source": {}  # {db_name: count}
            }
        }

    def add_identified(self, database: str, count: int):
        """
        Record number of records identified from a database.

        Args:
            database: Database name (e.g., "BioProject", "SRA")
            count: Number of records retrieved
        """
        self.data["identification"]["databases"][database] = count
        self.data["identification"]["total"] = sum(
            self.data["identification"]["databases"].values()
        )

    def set_screened(self, count: int):
        """
        Set number of records after initial screening.

        Args:
            count: Number of records that passed initial screening
        """
        self.data["screening"]["records_screened"] = count

    def add_excluded(self, count: int, reason: str):
        """
        Record excluded records with reason.

        Args:
            count: Number of records excluded for this reason
            reason: Explanation for exclusion
        """
        if reason in self.data["screening"]["exclusion_reasons"]:
            self.data["screening"]["exclusion_reasons"][reason] += count
        else:
            self.data["screening"]["exclusion_reasons"][reason] = count

        self.data["screening"]["records_excluded"] = sum(
            self.data["screening"]["exclusion_reasons"].values()
        )

    def set_included(self, total: int, by_source: Optional[Dict[str, int]] = None):
        """
        Set final included records count.

        Args:
            total: Total number of records in final dataset
            by_source: Optional breakdown by database source
        """
        self.data["included"]["total"] = total
        if by_source:
            self.data["included"]["by_source"] = by_source

    def get_summary(self) -> Dict:
        """
        Get summary statistics for the flow.

        Returns:
            Dictionary with key statistics
        """
        return {
            "total_identified": self.data["identification"]["total"],
            "total_screened": self.data["screening"]["records_screened"],
            "total_excluded": self.data["screening"]["records_excluded"],
            "total_included": self.data["included"]["total"],
            "exclusion_rate": (
                self.data["screening"]["records_excluded"] /
                self.data["screening"]["records_screened"] * 100
                if self.data["screening"]["records_screened"] > 0 else 0
            )
        }

    def save(self, output_dir: Optional[Path] = None) -> Path:
        """
        Save flow diagram data to JSON file.

        Args:
            output_dir: Directory to save file (defaults to data/prisma_flows/)

        Returns:
            Path to saved file
        """
        if output_dir is None:
            output_dir = Path("data/prisma_flows")

        output_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{self.label}_{date_str}_prisma_flow.json"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        return filepath

    @classmethod
    def load(cls, filepath: Path) -> 'PRISMAFlow':
        """
        Load existing flow data from JSON file.

        Args:
            filepath: Path to saved JSON file

        Returns:
            PRISMAFlow instance with loaded data
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        flow = cls(
            condition=data["metadata"]["condition"],
            label=data["metadata"]["label"]
        )
        flow.data = data
        flow.timestamp = data["metadata"]["timestamp"]

        return flow

    def generate_text_report(self) -> str:
        """
        Generate human-readable text report of the flow.

        Returns:
            Formatted text report
        """
        summary = self.get_summary()

        report = f"""
PRISMA Flow Summary
===================

Condition: {self.condition}
Date: {self.timestamp}

IDENTIFICATION
--------------
"""
        for db, count in self.data["identification"]["databases"].items():
            report += f"  {db}: {count:,} records\n"
        report += f"  TOTAL: {summary['total_identified']:,} records\n\n"

        report += f"""SCREENING
---------
Records screened: {summary['total_screened']:,}
Records excluded: {summary['total_excluded']:,} ({summary['exclusion_rate']:.1f}%)

Exclusion reasons:
"""
        for reason, count in self.data["screening"]["exclusion_reasons"].items():
            pct = (count / summary['total_excluded'] * 100) if summary['total_excluded'] > 0 else 0
            report += f"  - {reason}: {count:,} ({pct:.1f}%)\n"

        report += f"""
INCLUDED
--------
Final dataset: {summary['total_included']:,} records
"""
        if self.data["included"]["by_source"]:
            report += "\nBy source:\n"
            for source, count in self.data["included"]["by_source"].items():
                pct = (count / summary['total_included'] * 100) if summary['total_included'] > 0 else 0
                report += f"  {source}: {count:,} ({pct:.1f}%)\n"

        return report
