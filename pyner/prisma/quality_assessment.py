"""
Quality assessment module for PRISMA compliance.

Evaluates metadata completeness and quality for retrieved records.
Uses plant-specific quality keywords for diverse experiment types.
"""

from typing import Dict, List, Optional, Any
import pandas as pd
from pathlib import Path
from datetime import datetime
from ..domain_vocabularies import QUALITY_KEYWORDS, METHOD_KEYWORDS


class QualityAssessor:
    """
    Assess quality and completeness of retrieved metadata.

    Evaluates records based on:
    - Metadata completeness (% of fields populated)
    - Title informativeness (presence of key terms)
    - Tissue annotation quality (explicit vs. inferred)
    - Description richness

    Example:
        >>> assessor = QualityAssessor()
        >>> score = assessor.assess_record({
        ...     "ID": "PRJNA123456",
        ...     "Title": "Salt stress response in Arabidopsis root tissue",
        ...     "Description": "Detailed description...",
        ...     "Organism": "Arabidopsis thaliana",
        ...     "Tissue": "root",
        ...     "Tissue_confidence": "explicit"
        ... })
        >>> print(f"Quality score: {score['total_score']:.1f}/100")
    """

    def __init__(self):
        """Initialize quality assessor with default weights."""
        self.weights = {
            "completeness": 0.30,  # 30% weight
            "title_quality": 0.20,  # 20% weight
            "description_quality": 0.20,  # 20% weight
            "tissue_quality": 0.20,  # 20% weight
            "organism_specificity": 0.10  # 10% weight
        }

        # Required fields for completeness check
        self.required_fields = [
            "ID", "Title", "Description", "Organism", "Fuente"
        ]

        # Optional but valuable fields
        self.optional_fields = [
            "Tissue", "Tissue_confidence", "Extra"
        ]

    def assess_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess quality of a single record.

        Args:
            record: Dictionary containing record metadata

        Returns:
            Dictionary with quality scores and breakdown
        """
        scores = {}

        # 1. Completeness score
        scores["completeness"] = self._assess_completeness(record)

        # 2. Title quality
        scores["title_quality"] = self._assess_title(record.get("Title", ""))

        # 3. Description quality
        scores["description_quality"] = self._assess_description(
            record.get("Description", "")
        )

        # 4. Tissue annotation quality
        scores["tissue_quality"] = self._assess_tissue(
            record.get("Tissue", ""),
            record.get("Tissue_confidence", "")
        )

        # 5. Organism specificity
        scores["organism_specificity"] = self._assess_organism(
            record.get("Organism", "")
        )

        # Calculate weighted total
        total_score = sum(
            scores[key] * self.weights[key]
            for key in self.weights.keys()
        )

        return {
            "record_id": record.get("ID", "unknown"),
            "total_score": total_score,
            "scores": scores,
            "grade": self._assign_grade(total_score)
        }

    def _assess_completeness(self, record: Dict[str, Any]) -> float:
        """
        Calculate completeness score (0-100).

        Checks proportion of required and optional fields that are populated.
        """
        required_filled = sum(
            1 for field in self.required_fields
            if field in record and record[field] and str(record[field]).strip()
        )
        required_score = (required_filled / len(self.required_fields)) * 70

        optional_filled = sum(
            1 for field in self.optional_fields
            if field in record and record[field] and str(record[field]).strip()
        )
        optional_score = (optional_filled / len(self.optional_fields)) * 30

        return required_score + optional_score

    def _assess_title(self, title: str) -> float:
        """
        Assess title informativeness (0-100).

        Checks for:
        - Non-empty title
        - Minimum length
        - Presence of key biological terms (plant-specific)

        Uses comprehensive plant biology keywords from domain vocabularies.
        """
        if not title or not title.strip():
            return 0.0

        score = 30.0  # Base score for having a title

        # Length check (good titles are usually 40-200 chars)
        if 40 <= len(title) <= 200:
            score += 30.0
        elif len(title) > 20:
            score += 15.0

        # Check for biological keywords from domain vocabularies
        # Combine general and plant-specific keywords
        keywords = QUALITY_KEYWORDS["general"] + QUALITY_KEYWORDS["plant_specific"]

        title_lower = title.lower()
        found_keywords = sum(1 for kw in keywords if kw.lower() in title_lower)
        score += min(found_keywords * 10, 40)

        return min(score, 100.0)

    def _assess_description(self, description: str) -> float:
        """
        Assess description quality (0-100).

        Checks for:
        - Non-empty description
        - Sufficient length
        - Informative content with methodological keywords

        Uses comprehensive methodological keywords covering transcriptomics,
        genomics, epigenomics, proteomics, and other plant biology methods.
        """
        if not description or not description.strip():
            return 0.0

        score = 20.0  # Base score for having a description

        # Length-based scoring
        length = len(description)
        if length > 200:
            score += 40.0
        elif length > 100:
            score += 30.0
        elif length > 50:
            score += 20.0
        else:
            score += 10.0

        # Check for methodological keywords from domain vocabularies
        # Flatten all method keywords from different experiment types
        all_method_keywords = []
        for method_type, keywords in METHOD_KEYWORDS.items():
            all_method_keywords.extend(keywords)

        description_lower = description.lower()
        found_methods = sum(1 for kw in all_method_keywords if kw.lower() in description_lower)
        score += min(found_methods * 4, 40)

        return min(score, 100.0)

    def _assess_tissue(self, tissue: str, confidence: str) -> float:
        """
        Assess tissue annotation quality (0-100).

        Scoring:
        - Explicit tissue with name: 100
        - Inferred tissue with name: 60
        - Unknown but attempted: 30
        - No information: 0
        """
        if not tissue or tissue.strip().lower() in ["", "unknown", "none", "na"]:
            if confidence and confidence.strip().lower() == "unknown":
                return 30.0  # At least attempted
            return 0.0

        confidence_lower = confidence.lower() if confidence else ""

        if "explicit" in confidence_lower:
            return 100.0
        elif "inferred" in confidence_lower:
            return 60.0
        elif tissue and tissue.strip():
            return 50.0  # Has tissue but no confidence info
        else:
            return 0.0

    def _assess_organism(self, organism: str) -> float:
        """
        Assess organism specificity (0-100).

        Scoring:
        - Full species name (e.g., "Arabidopsis thaliana"): 100
        - Genus only (e.g., "Arabidopsis"): 60
        - Common name only: 40
        - No information: 0
        """
        if not organism or not organism.strip():
            return 0.0

        organism_lower = organism.lower()

        # Check for binomial nomenclature (two words)
        parts = organism.strip().split()
        if len(parts) >= 2:
            # Check if looks like scientific name (genus capitalized)
            if parts[0][0].isupper() and parts[1][0].islower():
                return 100.0
            else:
                return 80.0  # Has two parts but not standard format

        # Single word - could be genus
        if len(parts) == 1 and parts[0][0].isupper():
            return 60.0

        # Has something but not well formatted
        if organism.strip():
            return 40.0

        return 0.0

    def _assign_grade(self, score: float) -> str:
        """
        Assign letter grade based on total score.

        Args:
            score: Total quality score (0-100)

        Returns:
            Letter grade (A, B, C, D, F)
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def assess_dataset(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Assess quality for an entire dataset.

        Args:
            data: DataFrame with records to assess

        Returns:
            DataFrame with added quality score columns
        """
        results = []
        for _, row in data.iterrows():
            assessment = self.assess_record(row.to_dict())
            results.append({
                "ID": row.get("ID"),
                "quality_score": assessment["total_score"],
                "grade": assessment["grade"],
                **assessment["scores"]
            })

        quality_df = pd.DataFrame(results)

        # Merge with original data
        return data.merge(quality_df, on="ID", how="left")

    def generate_quality_report(
        self,
        data: pd.DataFrame,
        output_dir: Optional[Path] = None
    ) -> Path:
        """
        Generate comprehensive quality assessment report.

        Args:
            data: DataFrame with assessed records
            output_dir: Directory to save report (defaults to data/)

        Returns:
            Path to generated report
        """
        if output_dir is None:
            output_dir = Path("data")

        output_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"quality_report_{date_str}.txt"
        filepath = output_dir / filename

        # Calculate summary statistics
        avg_score = data["quality_score"].mean()
        median_score = data["quality_score"].median()
        grade_counts = data["grade"].value_counts().to_dict()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("Quality Assessment Report\n")
            f.write("========================\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total records: {len(data):,}\n\n")

            f.write("OVERALL QUALITY METRICS\n")
            f.write("-----------------------\n")
            f.write(f"Average quality score: {avg_score:.1f}/100\n")
            f.write(f"Median quality score: {median_score:.1f}/100\n\n")

            f.write("GRADE DISTRIBUTION\n")
            f.write("------------------\n")
            for grade in ["A", "B", "C", "D", "F"]:
                count = grade_counts.get(grade, 0)
                pct = (count / len(data) * 100) if len(data) > 0 else 0
                f.write(f"{grade}: {count:,} ({pct:.1f}%)\n")

            f.write("\n")
            f.write("COMPONENT SCORES (Average)\n")
            f.write("-------------------------\n")
            for component in self.weights.keys():
                if component in data.columns:
                    avg = data[component].mean()
                    f.write(f"{component}: {avg:.1f}/100\n")

            f.write("\n")
            f.write("RECOMMENDATIONS\n")
            f.write("---------------\n")

            if avg_score < 60:
                f.write("⚠️  Overall quality is LOW. Consider:\n")
                f.write("  - Reviewing data sources\n")
                f.write("  - Improving metadata extraction\n")
                f.write("  - Adding manual curation for key records\n")
            elif avg_score < 75:
                f.write("⚠️  Overall quality is MODERATE. Consider:\n")
                f.write("  - Enhancing tissue inference algorithms\n")
                f.write("  - Validating key records manually\n")
            else:
                f.write("✓ Overall quality is GOOD.\n")

            # Identify specific issues
            low_completeness = (data["completeness"] < 60).sum()
            if low_completeness > len(data) * 0.2:
                f.write(f"⚠️  {low_completeness} records ({low_completeness/len(data)*100:.1f}%) have low completeness.\n")

            no_tissue = (data["tissue_quality"] < 30).sum()
            if no_tissue > len(data) * 0.3:
                f.write(f"⚠️  {no_tissue} records ({no_tissue/len(data)*100:.1f}%) lack tissue information.\n")

        return filepath
