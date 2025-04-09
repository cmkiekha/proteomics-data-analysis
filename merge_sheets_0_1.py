import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

def merge_proteomics_datasets(
    transformed_data_path: str,
    combat_data_path: str,
    output_dir: str,
    output_filename: str = "merged_proteomics_data.csv"
) -> pd.DataFrame:
    """
    Merge the transformed proteomics data with additional data from the COMBAT dataset
    
    This function:
    1. Loads both datasets
    2. Ensures they have compatible PatientID and Timepoint formats
    3. Performs an outer join to preserve all proteins from both datasets
    4. Handles any duplicate column names across datasets
    5. Saves the merged dataset to disk
    
    Args:
        transformed_data_path: Path to the transformed data CSV file
        combat_data_path: Path to the COMBAT dataset CSV file
        output_dir: Directory to save the merged data
        output_filename: Name of the output file
        
    Returns:
        Merged DataFrame containing all proteins from both datasets
    """
    logger.info("Starting merge of proteomics datasets")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the datasets
    logger.info(f"Loading transformed data from {transformed_data_path}")
    transformed_df = pd.read_csv(transformed_data_path)
    
    logger.info(f"Loading COMBAT data from {combat_data_path}")
    combat_df = pd.read_csv(combat_data_path)
    
    # Get column lists (excluding PatientID and Timepoint)
    transformed_cols = [col for col in transformed_df.columns if col not in ['PatientID', 'Timepoint']]
    combat_cols = [col for col in combat_df.columns if col not in ['PatientID', 'Timepoint']]
    
    # Check for overlapping columns
    overlapping_cols = set(transformed_cols).intersection(set(combat_cols))
    logger.info(f"Found {len(overlapping_cols)} overlapping protein columns")
    
    # Merge datasets on PatientID and Timepoint
    logger.info("Merging datasets on PatientID and Timepoint")
    merged_df = pd.merge(
        transformed_df, 
        combat_df,
        on=['PatientID', 'Timepoint'], 
        how='outer',
        suffixes=('', '_combat')  # Keep original names for transformed data, add suffix for COMBAT
    )
    
    # Handle overlapping columns if needed
    for col in overlapping_cols:
        combat_col = f"{col}_combat"
        if combat_col in merged_df.columns:
            # Count non-NaN values in each column
            original_count = merged_df[col].notna().sum()
            combat_count = merged_df[combat_col].notna().sum()
            
            logger.info(f"Column '{col}' exists in both datasets. "
                       f"Original has {original_count} values, COMBAT has {combat_count} values.")
            
            # Fill NaN values in the original column with values from COMBAT column
            merged_df[col] = merged_df[col].fillna(merged_df[combat_col])
            
            # Drop the duplicate COMBAT column
            merged_df.drop(columns=[combat_col], inplace=True)
            
            logger.info(f"Merged values for '{col}', now has {merged_df[col].notna().sum()} values")
    
    # Get statistics about the merged dataset
    total_proteins = len([col for col in merged_df.columns if col not in ['PatientID', 'Timepoint']])
    total_patients = merged_df['PatientID'].nunique()
    total_timepoints = merged_df['Timepoint'].nunique()
    
    logger.info(f"Merged dataset contains {total_proteins} proteins, "
               f"{total_patients} unique patients, and {total_timepoints} timepoints")
    
    # Save merged dataset
    output_path = os.path.join(output_dir, output_filename)
    merged_df.to_csv(output_path, index=False)
    logger.info(f"Saved merged dataset to {output_path}")
    
    print(f"Merged dataset created with {total_proteins} proteins")
    print(f"Dataset contains {total_patients} unique patients with {total_timepoints} timepoints")
    print(f"Saved to {output_path}")
    
    return merged_df

def get_protein_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary of all proteins in the merged dataset
    
    This function:
    1. Calculates coverage (percentage of non-NA values) for each protein
    2. Calculates basic statistics (min, max, mean, std) for each protein
    3. Creates a sorted summary dataframe with this information
    
    Args:
        df: Merged proteomics DataFrame
        
    Returns:
        Summary DataFrame with protein statistics
    """
    # Get protein columns (all columns except PatientID and Timepoint)
    protein_cols = [col for col in df.columns if col not in ['PatientID', 'Timepoint']]
    
    # Calculate coverage for each protein
    total_samples = len(df)
    coverage = {protein: (df[protein].notna().sum() / total_samples) * 100 for protein in protein_cols}
    
    # Calculate basic statistics
    summary_data = []
    
    for protein in protein_cols:
        protein_data = df[protein].dropna()
        if len(protein_data) > 0:
            summary_data.append({
                'Protein': protein,
                'Coverage (%)': coverage[protein],
                'Count': len(protein_data),
                'Min': protein_data.min(),
                'Max': protein_data.max(),
                'Mean': protein_data.mean(),
                'Std': protein_data.std()
            })
    
    # Create summary dataframe
    summary_df = pd.DataFrame(summary_data)

    # Sort by coverage (descending)
    summary_df.sort_values('Coverage (%)', ascending=False, inplace=True)
    
    return summary_df

def save_protein_summary(summary_df: pd.DataFrame, output_dir: str, filename: str = "protein_summary.csv") -> str:
    """
    Save the protein summary to a CSV file
    
    Args:
        summary_df: Summary DataFrame to save
        output_dir: Directory to save the summary
        filename: Name of the output file
        
    Returns:
        Path to the saved summary file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save summary
    output_path = os.path.join(output_dir, filename)
    summary_df.to_csv(output_path, index=False)
    
    print(f"Protein summary saved to {output_path}")
    return output_path

# Example usage
if __name__ == "__main__":
    # Define paths
    transformed_data_path = "07_transformed_data.csv"
    combat_data_path = "COMBAT_cleaned_sheet1.csv"
    output_dir = "merged_results"
    
    # Merge datasets
    merged_df = merge_proteomics_datasets(
        transformed_data_path,
        combat_data_path,
        output_dir
    )
    
    # Generate and save protein summary
    summary_df = get_protein_summary(merged_df)
    save_protein_summary(summary_df, output_dir)
