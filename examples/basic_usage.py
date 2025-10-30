"""
Basic usage example for Pyner.

This script demonstrates how to use Pyner for systematic data mining
with PRISMA compliance.
"""

from pyner import DataMiner, Config

def main():
    # Configure NCBI access
    # Option 1: From environment variables
    config = Config.from_env()

    # Option 2: Explicit configuration
    # config = Config(
    #     email="your.email@institution.edu",
    #     api_key="your_api_key_here"
    # )

    # Initialize data miner
    miner = DataMiner(config)

    # Run systematic search
    results = miner.run(
        organism="Arabidopsis thaliana",
        condition="salt stress",
        experiment="RNA-seq",
        label="salt",
        enable_quality_filter=True,
        min_quality_score=60.0
    )

    # Print summary
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)

    summary = results["summary"]
    print(f"\nIdentified:  {summary['total_identified']:>6,} records")
    print(f"Screened:    {summary['total_screened']:>6,} records")
    print(f"Excluded:    {summary['total_excluded']:>6,} records")
    print(f"Included:    {summary['total_included']:>6,} records")
    print(f"Exclusion rate: {summary['exclusion_rate']:>5.1f}%")

    # Access data
    included = results["data"]["included"]
    excluded = results["data"]["excluded"]

    print(f"\n{'='*60}")
    print("INCLUDED RECORDS BY DATABASE")
    print("="*60)
    print(included["Fuente"].value_counts())

    print(f"\n{'='*60}")
    print("AVERAGE QUALITY SCORE")
    print("="*60)
    print(f"{included['quality_score'].mean():.1f}/100")

    # List generated files
    print(f"\n{'='*60}")
    print("GENERATED FILES")
    print("="*60)
    for file_type, path in results["files"].items():
        print(f"{file_type:20s}: {path}")

    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
