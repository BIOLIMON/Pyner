"""
Core data mining pipeline for Pyner.

Orchestrates the PRISMA-compliant systematic data retrieval process.
"""

from typing import List, Dict, Optional, Any
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

from .config import Config
from .prisma import PRISMAFlow, ScreeningLog, QualityAssessor


class DataMiner:
    """
    Main orchestrator for PRISMA-compliant data mining.

    Coordinates:
    1. Query construction
    2. Multi-database searching (BioProject, SRA, GEO, PubMed)
    3. Metadata extraction
    4. PRISMA flow tracking
    5. Quality assessment
    6. Data export

    Example:
        >>> from pyner import DataMiner, Config
        >>> config = Config.from_env()
        >>> miner = DataMiner(config)
        >>> results = miner.run(
        ...     organism="Arabidopsis thaliana",
        ...     condition="salt stress",
        ...     experiment="RNA-seq",
        ...     label="salt"
        ... )
    """

    def __init__(self, config: Config):
        """
        Initialize data miner.

        Args:
            config: Configuration with NCBI credentials
        """
        self.config = config
        self.config.validate()

        self.prisma_flow = None
        self.screening_log = None
        self.quality_assessor = QualityAssessor()

        # Database handlers will be initialized when needed
        self.databases = ["bioproject", "sra", "gds", "pubmed"]

    def run(
        self,
        organism: str,
        condition: str,
        experiment: str,
        label: str,
        output_dir: Optional[Path] = None,
        enable_quality_filter: bool = True,
        min_quality_score: float = 50.0
    ) -> Dict[str, Any]:
        """
        Execute complete PRISMA-compliant data mining pipeline.

        Args:
            organism: Target organism (e.g., "Arabidopsis thaliana")
            condition: Experimental condition (e.g., "salt stress")
            experiment: Experiment type (e.g., "RNA-seq")
            label: Short label for output files (e.g., "salt")
            output_dir: Base directory for outputs (defaults to current dir)
            enable_quality_filter: Apply quality filtering to results
            min_quality_score: Minimum quality score threshold (0-100)

        Returns:
            Dictionary with paths to generated files and summary statistics
        """
        if output_dir is None:
            output_dir = Path.cwd()

        print(f"\n{'='*60}")
        print(f"Pyner: PRISMA-Compliant Data Mining")
        print(f"{'='*60}")
        print(f"Organism: {organism}")
        print(f"Condition: {condition}")
        print(f"Experiment: {experiment}")
        print(f"Label: {label}")
        print(f"{'='*60}\n")

        # Initialize PRISMA tracking
        self.prisma_flow = PRISMAFlow(condition=condition, label=label)
        self.screening_log = ScreeningLog(condition=condition, label=label)

        # Step 1: Identification - Search all databases
        print("STEP 1: IDENTIFICATION")
        print("-" * 40)
        raw_results = self._search_databases(organism, condition, experiment)

        # Step 2: Screening - Fetch metadata
        print("\nSTEP 2: SCREENING")
        print("-" * 40)
        metadata = self._fetch_metadata(raw_results)

        # Step 3: Quality Assessment
        print("\nSTEP 3: QUALITY ASSESSMENT")
        print("-" * 40)
        assessed_data = self._assess_quality(metadata)

        # Step 4: Apply filters and exclusions
        print("\nSTEP 4: FILTERING")
        print("-" * 40)
        included_data, excluded_data = self._apply_filters(
            assessed_data,
            enable_quality_filter,
            min_quality_score
        )

        # Step 5: Save outputs
        print("\nSTEP 5: SAVING OUTPUTS")
        print("-" * 40)
        output_paths = self._save_outputs(
            included_data,
            excluded_data,
            label,
            output_dir
        )

        # Step 6: Generate PRISMA documentation
        print("\nSTEP 6: GENERATING PRISMA DOCUMENTATION")
        print("-" * 40)
        prisma_paths = self._generate_prisma_docs(output_dir)

        print(f"\n{'='*60}")
        print("PIPELINE COMPLETE")
        print(f"{'='*60}")
        print(f"Records identified: {self.prisma_flow.data['identification']['total']:,}")
        print(f"Records included: {len(included_data):,}")
        print(f"Records excluded: {len(excluded_data):,}")
        print(f"\nOutputs saved to: {output_dir}")
        print(f"{'='*60}\n")

        return {
            "data": {
                "included": included_data,
                "excluded": excluded_data
            },
            "files": {**output_paths, **prisma_paths},
            "summary": self.prisma_flow.get_summary()
        }

    def _search_databases(
        self,
        organism: str,
        condition: str,
        experiment: str
    ) -> Dict[str, List[str]]:
        """
        Search all NCBI databases and collect IDs.

        This is a placeholder - actual implementation would use Bio.Entrez
        to search BioProject, SRA, GEO, and PubMed.

        Args:
            organism: Target organism
            condition: Experimental condition
            experiment: Experiment type

        Returns:
            Dictionary mapping database names to lists of IDs
        """
        print("Searching NCBI databases...")
        print(f"  Query: ({organism}) AND ({condition}) AND ({experiment})")

        # TODO: Implement actual Entrez searches
        # This is a placeholder showing the expected structure
        results = {
            "bioproject": [],
            "sra": [],
            "gds": [],
            "pubmed": []
        }

        # Record in PRISMA flow
        for database, ids in results.items():
            self.prisma_flow.add_identified(database, len(ids))
            print(f"  {database}: {len(ids):,} records")

        return results

    def _fetch_metadata(self, raw_results: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Fetch detailed metadata for all retrieved IDs.

        This is a placeholder - actual implementation would use Bio.Entrez
        to fetch summaries and parse them.

        Args:
            raw_results: Dictionary of database IDs

        Returns:
            DataFrame with metadata for all records
        """
        print("Fetching metadata for retrieved records...")

        all_records = []

        # TODO: Implement actual metadata fetching
        # This is a placeholder

        df = pd.DataFrame(all_records)

        self.prisma_flow.set_screened(len(df))
        print(f"  Metadata retrieved for {len(df):,} records")

        return df

    def _assess_quality(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Assess quality for all records.

        Args:
            data: DataFrame with record metadata

        Returns:
            DataFrame with added quality scores
        """
        print("Assessing metadata quality...")

        assessed_data = self.quality_assessor.assess_dataset(data)

        avg_score = assessed_data["quality_score"].mean()
        print(f"  Average quality score: {avg_score:.1f}/100")

        return assessed_data

    def _apply_filters(
        self,
        data: pd.DataFrame,
        enable_quality_filter: bool,
        min_quality_score: float
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Apply filters and separate included/excluded records.

        Args:
            data: Assessed data
            enable_quality_filter: Whether to apply quality filtering
            min_quality_score: Minimum quality score threshold

        Returns:
            Tuple of (included_data, excluded_data)
        """
        print("Applying filters...")

        excluded_data = pd.DataFrame()

        if enable_quality_filter:
            # Separate based on quality score
            included_mask = data["quality_score"] >= min_quality_score
            included_data = data[included_mask].copy()
            excluded_data = data[~included_mask].copy()

            # Add exclusion reason
            excluded_data["exclusion_reason"] = (
                f"Quality score below threshold ({min_quality_score})"
            )

            # Log exclusions
            for _, row in excluded_data.iterrows():
                self.screening_log.add_entry(
                    record_id=row["ID"],
                    database=row["Fuente"],
                    decision="excluded",
                    title=row.get("Title", ""),
                    reason=f"Low quality score: {row['quality_score']:.1f}",
                    quality_score=row["quality_score"]
                )

            self.prisma_flow.add_excluded(
                len(excluded_data),
                reason=f"Quality score < {min_quality_score}"
            )

            print(f"  Included: {len(included_data):,} records")
            print(f"  Excluded: {len(excluded_data):,} records (low quality)")
        else:
            included_data = data.copy()
            print(f"  No quality filtering applied")
            print(f"  Included: {len(included_data):,} records")

        # Log inclusions
        for _, row in included_data.iterrows():
            self.screening_log.add_entry(
                record_id=row["ID"],
                database=row["Fuente"],
                decision="included",
                title=row.get("Title", ""),
                quality_score=row.get("quality_score")
            )

        self.prisma_flow.set_included(len(included_data))

        return included_data, excluded_data

    def _save_outputs(
        self,
        included_data: pd.DataFrame,
        excluded_data: pd.DataFrame,
        label: str,
        output_dir: Path
    ) -> Dict[str, Path]:
        """
        Save data files to appropriate directories.

        Args:
            included_data: Included records
            excluded_data: Excluded records
            label: File label
            output_dir: Base output directory

        Returns:
            Dictionary of output file paths
        """
        date_str = datetime.now().strftime("%Y%m%d")

        paths = {}

        # Save included data
        included_dir = output_dir / "data" / "processed"
        included_dir.mkdir(parents=True, exist_ok=True)
        included_path = included_dir / f"{label}_{date_str}_processed.csv"
        included_data.to_csv(included_path, index=False)
        paths["included"] = included_path
        print(f"  Saved included data: {included_path}")

        # Save excluded data (if any)
        if len(excluded_data) > 0:
            excluded_dir = output_dir / "data" / "excluded"
            excluded_dir.mkdir(parents=True, exist_ok=True)
            excluded_path = excluded_dir / f"{label}_{date_str}_excluded.csv"
            excluded_data.to_csv(excluded_path, index=False)
            paths["excluded"] = excluded_path
            print(f"  Saved excluded data: {excluded_path}")

        return paths

    def _generate_prisma_docs(self, output_dir: Path) -> Dict[str, Path]:
        """
        Generate PRISMA documentation files.

        Args:
            output_dir: Base output directory

        Returns:
            Dictionary of documentation file paths
        """
        paths = {}

        # Save PRISMA flow diagram data
        flow_path = self.prisma_flow.save(output_dir / "data" / "prisma_flows")
        paths["prisma_flow"] = flow_path
        print(f"  Saved PRISMA flow: {flow_path}")

        # Generate and save text report
        report = self.prisma_flow.generate_text_report()
        report_path = output_dir / "data" / "prisma_flows" / f"{self.prisma_flow.label}_report.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        paths["prisma_report"] = report_path
        print(f"  Saved PRISMA report: {report_path}")

        # Save screening log
        log_path = self.screening_log.save(output_dir / "logs")
        paths["screening_log"] = log_path
        print(f"  Saved screening log: {log_path}")

        # Save screening summary
        summary_path = self.screening_log.save_summary(output_dir / "logs")
        paths["screening_summary"] = summary_path
        print(f"  Saved screening summary: {summary_path}")

        return paths
