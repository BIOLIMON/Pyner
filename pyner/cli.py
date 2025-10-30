"""
Command-line interface for Pyner.

Provides CLI for running PRISMA-compliant data mining operations.
"""

import argparse
import sys
from pathlib import Path
from .config import Config
from .core import DataMiner


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Pyner: PRISMA-compliant bioinformatics data mining",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search with environment variables for credentials
  pyner --organism "Arabidopsis thaliana" --condition "salt stress" \\
        --experiment "RNA-seq" --label salt

  # With explicit email and API key
  pyner --email your.email@institution.edu --api-key YOUR_KEY \\
        --organism "Solanum lycopersicum" --condition drought \\
        --experiment transcriptome --label tomato_drought

  # With custom output directory and quality filtering
  pyner --organism "Oryza sativa" --condition "heat stress" \\
        --experiment RNA-seq --label rice_heat \\
        --output-dir ./my_results --min-quality 70

Environment Variables:
  NCBI_EMAIL     : Email for NCBI API (required if --email not provided)
  NCBI_API_KEY   : NCBI API key (optional but recommended)
        """
    )

    # Required arguments
    parser.add_argument(
        "--organism",
        required=True,
        help="Target organism (e.g., 'Arabidopsis thaliana')"
    )
    parser.add_argument(
        "--condition",
        required=True,
        help="Experimental condition (e.g., 'salt stress', 'drought')"
    )
    parser.add_argument(
        "--experiment",
        required=True,
        help="Experiment type (e.g., 'RNA-seq', 'transcriptome')"
    )
    parser.add_argument(
        "--label",
        required=True,
        help="Short label for output files (e.g., 'salt', 'drought')"
    )

    # NCBI credentials
    parser.add_argument(
        "--email",
        help="Email for NCBI API (or set NCBI_EMAIL env variable)"
    )
    parser.add_argument(
        "--api-key",
        help="NCBI API key (or set NCBI_API_KEY env variable)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to config file"
    )

    # Output options
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Output directory (default: current directory)"
    )

    # Quality filtering
    parser.add_argument(
        "--no-quality-filter",
        action="store_true",
        help="Disable quality-based filtering"
    )
    parser.add_argument(
        "--min-quality",
        type=float,
        default=50.0,
        help="Minimum quality score threshold (0-100, default: 50)"
    )

    # Other options
    parser.add_argument(
        "--version",
        action="version",
        version="Pyner 0.1.0"
    )

    args = parser.parse_args()

    # Create configuration
    try:
        if args.config:
            config = Config.from_file(args.config)
        elif args.email:
            config = Config(email=args.email, api_key=args.api_key)
        else:
            config = Config.from_env()
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("\nPlease provide NCBI credentials via:", file=sys.stderr)
        print("  1. --email and --api-key arguments", file=sys.stderr)
        print("  2. NCBI_EMAIL and NCBI_API_KEY environment variables", file=sys.stderr)
        print("  3. --config file", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Run data mining
    try:
        miner = DataMiner(config)
        results = miner.run(
            organism=args.organism,
            condition=args.condition,
            experiment=args.experiment,
            label=args.label,
            output_dir=args.output_dir,
            enable_quality_filter=not args.no_quality_filter,
            min_quality_score=args.min_quality
        )

        print("\n✓ Data mining completed successfully!")
        print(f"\nSummary:")
        for key, value in results["summary"].items():
            print(f"  {key}: {value}")

        print(f"\nFiles generated:")
        for file_type, path in results["files"].items():
            print(f"  {file_type}: {path}")

        sys.exit(0)

    except Exception as e:
        print(f"\nError during data mining: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
