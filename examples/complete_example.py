"""
Complete example demonstrating all Pyner features.

This script shows:
1. Configuration setup
2. Running the full pipeline
3. Accessing PRISMA documentation
4. Quality assessment
5. Custom filtering
"""

from pyner import DataMiner, Config
from pyner.prisma import PRISMAFlow, ScreeningLog, QualityAssessor
import pandas as pd
from pathlib import Path


def main():
    print("="*70)
    print("Pyner Complete Example: Salt Stress in Arabidopsis thaliana")
    print("="*70)

    # =========================================================================
    # STEP 1: Configuration
    # =========================================================================
    print("\nSTEP 1: Setting up configuration")
    print("-" * 70)

    # Option A: From environment variables
    try:
        config = Config.from_env()
        print("✓ Loaded configuration from environment variables")
    except ValueError:
        print("⚠ Environment variables not set. Using demo configuration.")
        print("  Please set NCBI_EMAIL and optionally NCBI_API_KEY")
        print("\n  Example:")
        print("    export NCBI_EMAIL='your.email@institution.edu'")
        print("    export NCBI_API_KEY='your_api_key'")
        return

    print(f"  Email: {config.email}")
    print(f"  API Key: {'Set' if config.api_key else 'Not set (using lower rate limit)'}")
    print(f"  Rate limit: {config.rate_limit:.2f}s between requests")

    # =========================================================================
    # STEP 2: Run Data Mining
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 2: Running systematic data mining")
    print("="*70)

    output_dir = Path("./results")

    miner = DataMiner(config)

    results = miner.run(
        organism="Arabidopsis thaliana",
        condition="salt stress",
        experiment="RNA-seq",
        label="salt",
        output_dir=output_dir,
        enable_quality_filter=True,
        min_quality_score=60.0
    )

    # =========================================================================
    # STEP 3: Analyze Results
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 3: Analyzing Results")
    print("="*70)

    included_data = results["data"]["included"]
    excluded_data = results["data"]["excluded"]

    print(f"\nDataset Summary:")
    print(f"  Total included: {len(included_data):,} records")
    print(f"  Total excluded: {len(excluded_data):,} records")

    if len(included_data) > 0:
        print(f"\n  Records by source:")
        source_counts = included_data["Fuente"].value_counts()
        for source, count in source_counts.items():
            pct = (count / len(included_data) * 100)
            print(f"    {source:15s}: {count:5,} ({pct:5.1f}%)")

        print(f"\n  Quality distribution:")
        if "quality_score" in included_data.columns:
            print(f"    Average score: {included_data['quality_score'].mean():.1f}/100")
            print(f"    Median score:  {included_data['quality_score'].median():.1f}/100")
            print(f"    Min score:     {included_data['quality_score'].min():.1f}/100")
            print(f"    Max score:     {included_data['quality_score'].max():.1f}/100")

            if "grade" in included_data.columns:
                print(f"\n    Grade distribution:")
                grade_counts = included_data["grade"].value_counts()
                for grade in ["A", "B", "C", "D", "F"]:
                    if grade in grade_counts:
                        count = grade_counts[grade]
                        pct = (count / len(included_data) * 100)
                        print(f"      {grade}: {count:5,} ({pct:5.1f}%)")

        # Tissue information
        if "Tissue" in included_data.columns:
            tissue_counts = included_data[included_data["Tissue"].notna()]["Tissue"].value_counts()
            if len(tissue_counts) > 0:
                print(f"\n  Top tissues:")
                for tissue, count in tissue_counts.head(5).items():
                    pct = (count / len(included_data) * 100)
                    print(f"    {tissue:15s}: {count:5,} ({pct:5.1f}%)")

    # =========================================================================
    # STEP 4: PRISMA Documentation
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 4: PRISMA Documentation")
    print("="*70)

    # Load PRISMA flow
    prisma_flow_path = results["files"].get("prisma_flow")
    if prisma_flow_path and prisma_flow_path.exists():
        flow = PRISMAFlow.load(prisma_flow_path)
        print("\n" + flow.generate_text_report())

    # Load screening log
    screening_log_path = results["files"].get("screening_log")
    if screening_log_path and screening_log_path.exists():
        log = ScreeningLog.load(screening_log_path)
        stats = log.get_statistics()

        print("\nScreening Log Statistics:")
        print(f"  Total screened: {stats['total_screened']:,}")
        print(f"  Included: {stats['included']:,} ({stats['inclusion_rate']:.1f}%)")
        print(f"  Excluded: {stats['excluded']:,}")

        if stats['exclusion_reasons']:
            print(f"\n  Exclusion reasons:")
            for reason, count in stats['exclusion_reasons'].items():
                print(f"    - {reason}: {count:,}")

    # =========================================================================
    # STEP 5: Generated Files
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 5: Generated Files")
    print("="*70)

    print("\nAll generated files:")
    for file_type, path in results["files"].items():
        print(f"  {file_type:20s}: {path}")

    # =========================================================================
    # STEP 6: Custom Analysis Example
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 6: Custom Analysis Example")
    print("="*70)

    if len(included_data) > 0:
        # Find records with explicit tissue information
        explicit_tissue = included_data[
            included_data["Tissue_confidence"] == "explicit"
        ]

        print(f"\nRecords with explicit tissue information: {len(explicit_tissue):,}")

        # Find high-quality records from BioProject
        high_quality_bioproject = included_data[
            (included_data["Fuente"] == "BioProject") &
            (included_data["quality_score"] >= 80)
        ]

        print(f"High-quality BioProject records (≥80): {len(high_quality_bioproject):,}")

        # Export subset for further analysis
        if len(high_quality_bioproject) > 0:
            subset_path = output_dir / "data" / "processed" / "salt_high_quality_bioproject.csv"
            high_quality_bioproject.to_csv(subset_path, index=False)
            print(f"\nExported subset to: {subset_path}")

    print("\n" + "="*70)
    print("EXAMPLE COMPLETE!")
    print("="*70)
    print(f"\nAll outputs saved to: {output_dir}")
    print("\nNext steps:")
    print("  1. Review PRISMA flow diagram in data/prisma_flows/")
    print("  2. Check screening log in logs/")
    print("  3. Analyze processed data in data/processed/")
    print("  4. Use excluded data to refine search parameters")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
