"""
Screening log for PRISMA compliance.

Records detailed information about inclusion/exclusion decisions during
the systematic review process.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any


class ScreeningLog:
    """
    Records screening decisions for each record evaluated.

    Maintains a detailed audit trail of:
    - Which records were evaluated
    - Whether they were included or excluded
    - Reasons for exclusion
    - Quality assessment notes

    Example:
        >>> log = ScreeningLog(condition="salt_stress")
        >>> log.add_entry(
        ...     record_id="PRJNA123456",
        ...     database="BioProject",
        ...     decision="included",
        ...     title="Salt stress response in Arabidopsis"
        ... )
        >>> log.add_entry(
        ...     record_id="SRX987654",
        ...     database="SRA",
        ...     decision="excluded",
        ...     reason="Missing tissue information"
        ... )
        >>> log.save()
    """

    def __init__(self, condition: str, label: Optional[str] = None):
        """
        Initialize screening log.

        Args:
            condition: Experimental condition
            label: Short label for output files
        """
        self.condition = condition
        self.label = label or condition
        self.timestamp = datetime.now().isoformat()

        self.entries: List[Dict[str, Any]] = []

        self.fieldnames = [
            "timestamp",
            "record_id",
            "database",
            "title",
            "decision",  # "included" or "excluded"
            "reason",  # exclusion reason (if excluded)
            "quality_score",  # optional quality score
            "notes"  # additional notes
        ]

    def add_entry(
        self,
        record_id: str,
        database: str,
        decision: str,
        title: Optional[str] = None,
        reason: Optional[str] = None,
        quality_score: Optional[float] = None,
        notes: Optional[str] = None
    ):
        """
        Add a screening decision entry.

        Args:
            record_id: Database accession ID
            database: Source database (BioProject, SRA, GEO, PubMed)
            decision: "included" or "excluded"
            title: Record title (optional)
            reason: Reason for exclusion (required if decision="excluded")
            quality_score: Optional quality assessment score (0-100)
            notes: Additional notes
        """
        if decision not in ["included", "excluded"]:
            raise ValueError("Decision must be 'included' or 'excluded'")

        if decision == "excluded" and not reason:
            raise ValueError("Reason required for excluded records")

        entry = {
            "timestamp": datetime.now().isoformat(),
            "record_id": record_id,
            "database": database,
            "title": title or "",
            "decision": decision,
            "reason": reason or "",
            "quality_score": quality_score or "",
            "notes": notes or ""
        }

        self.entries.append(entry)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get summary statistics for screening decisions.

        Returns:
            Dictionary with counts and percentages
        """
        total = len(self.entries)
        included = sum(1 for e in self.entries if e["decision"] == "included")
        excluded = total - included

        # Count exclusion reasons
        exclusion_reasons = {}
        for entry in self.entries:
            if entry["decision"] == "excluded" and entry["reason"]:
                reason = entry["reason"]
                exclusion_reasons[reason] = exclusion_reasons.get(reason, 0) + 1

        # Count by database
        by_database = {}
        for entry in self.entries:
            db = entry["database"]
            if db not in by_database:
                by_database[db] = {"total": 0, "included": 0, "excluded": 0}
            by_database[db]["total"] += 1
            by_database[db][entry["decision"]] += 1

        return {
            "total_screened": total,
            "included": included,
            "excluded": excluded,
            "inclusion_rate": (included / total * 100) if total > 0 else 0,
            "exclusion_reasons": exclusion_reasons,
            "by_database": by_database
        }

    def save(self, output_dir: Optional[Path] = None) -> Path:
        """
        Save screening log to CSV file.

        Args:
            output_dir: Directory to save file (defaults to logs/)

        Returns:
            Path to saved file
        """
        if output_dir is None:
            output_dir = Path("logs")

        output_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.label}_{date_str}_screening.log"
        filepath = output_dir / filename

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.entries)

        return filepath

    def save_summary(self, output_dir: Optional[Path] = None) -> Path:
        """
        Save summary statistics to text file.

        Args:
            output_dir: Directory to save file (defaults to logs/)

        Returns:
            Path to saved file
        """
        if output_dir is None:
            output_dir = Path("logs")

        output_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.label}_{date_str}_screening_summary.txt"
        filepath = output_dir / filename

        stats = self.get_statistics()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Screening Log Summary\n")
            f.write(f"====================\n\n")
            f.write(f"Condition: {self.condition}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"OVERALL STATISTICS\n")
            f.write(f"------------------\n")
            f.write(f"Total screened: {stats['total_screened']:,}\n")
            f.write(f"Included: {stats['included']:,} ({stats['inclusion_rate']:.1f}%)\n")
            f.write(f"Excluded: {stats['excluded']:,} ({100-stats['inclusion_rate']:.1f}%)\n\n")

            if stats['exclusion_reasons']:
                f.write(f"EXCLUSION REASONS\n")
                f.write(f"-----------------\n")
                for reason, count in sorted(
                    stats['exclusion_reasons'].items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    pct = (count / stats['excluded'] * 100) if stats['excluded'] > 0 else 0
                    f.write(f"  {reason}: {count:,} ({pct:.1f}%)\n")
                f.write("\n")

            f.write(f"BY DATABASE\n")
            f.write(f"-----------\n")
            for db, counts in stats['by_database'].items():
                inc_rate = (counts['included'] / counts['total'] * 100) if counts['total'] > 0 else 0
                f.write(f"{db}:\n")
                f.write(f"  Total: {counts['total']:,}\n")
                f.write(f"  Included: {counts['included']:,} ({inc_rate:.1f}%)\n")
                f.write(f"  Excluded: {counts['excluded']:,} ({100-inc_rate:.1f}%)\n")

        return filepath

    @classmethod
    def load(cls, filepath: Path) -> 'ScreeningLog':
        """
        Load screening log from CSV file.

        Args:
            filepath: Path to CSV log file

        Returns:
            ScreeningLog instance with loaded data
        """
        # Extract condition from filename (assumes format: condition_date_screening.log)
        filename = filepath.stem
        condition = filename.split('_')[0]

        log = cls(condition=condition)

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            log.entries = list(reader)

        return log
