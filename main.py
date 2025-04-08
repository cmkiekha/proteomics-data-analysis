"""
Proteomics Data Cleaner

A tool for cleaning and validation:
- Transforms complex proteomics data into analysis-ready format
- Removes unwanted rows and columns
- Fuses protein IDs
- Combines protein labels from different sources
- Validates all steps with detailed checks
- Calculates missingness, outliers, and basic statistics
- Creates visualizations for quality assessment
- Saves intermediate files at each processing step

Usage:
python main.py --input data.csv --output-dir results
"""

import argparse
import sys
from proteomics_cleaner import ProteomicsCleaner


def parse_arguments():
    """
    Parse command line arguments for the proteomics cleaner
    """
    parser = argparse.ArgumentParser(
        description="Clean and validate proteomics data",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--input", required=True, help="Input CSV or Excel file")

    parser.add_argument(
        "--output-dir", required=True, help="Output directory for all generated files"
    )

    parser.add_argument(
        "--sheet", default=0, help="Sheet name or index (only used for Excel files)"
    )

    parser.add_argument(
        "--column-af",
        type=int,
        default=31,
        help="Index for column AF containing protein labels",
    )

    parser.add_argument(
        "--patient-start",
        type=int,
        default=47,
        help="Column index where patient data starts",
    )

    parser.add_argument(
        "--min-coverage",
        type=float,
        default=10.0,
        help="Minimum percentage of patients with protein value for inclusion",
    )

    parser.add_argument(
        "--max-viz",
        type=int,
        default=100,
        help="Maximum number of proteins to visualize",
    )

    return parser.parse_args()


def main():
    """
    # Main execution function for the proteomics cleaner
    """
    args = parse_arguments()

    print(f"Processing file: {args.input}")
    print(f"Output directory: {args.output_dir}")

    # Create cleaner instance
    cleaner = ProteomicsCleaner(
        input_file=args.input,
        output_dir=args.output_dir,
        sheet_name=args.sheet,
        column_af_index=args.column_af,
        patient_start_index=args.patient_start,
    )

    # Run the pipeline
    success = cleaner.run_pipeline(
        min_coverage_pct=args.min_coverage, max_viz_proteins=args.max_viz
    )

    if not success:
        print("\nCleaning pipeline encountered errors. Check the log file for details.")
        return 1

    print("\nProteomic data cleaning completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
