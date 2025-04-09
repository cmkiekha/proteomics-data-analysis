# Proteomics Data Cleaning Summary

Processed on: 2025-04-08 21:19:11

Input file: subset.csv
Output directory: results

## Dataset Summary

- **Patients:** 50
- **Proteins:** 86
- **Timepoints:** 2

## Quality Summary

- **Total patients:** 50.00

- **Total proteins:** 86.00

- **Avg missing values (%):** 0.00

- **Proteins with >50% missing:** 0.00

- **Proteins with high CV (>100%):** 2.00

- **Proteins with >50% zeros:** 6.00

- **Proteins with >5% negative values:** 0.00

- **Proteins with >10% IQR outliers:** 2.00

- **Proteins with >10% Z-score outliers:** 0.00

- **Proteins with multiple flags:** 2.00

## Potential Problem Areas

- **Proteins with multiple quality flags:** 2

### Top 10 most problematic proteins:
- **D-Dimer_H4t6** (AF): high variability, many zeros, IQR outliers
- **D-Dimer_6t12** (AF): high variability, many zeros
- **Fibrinogen_6t12** (AF): many zeros
- **Fibrinogen_24+** (AF): many zeros
- **Fibrinogen_H4t6** (AF): many zeros
- **Fibrinogen_F** (AF): many zeros
- **Fibrinogen_12t24** (AF): IQR outliers
- **CFAH_286_GDE** (Fused): 
- **C4BPA_79_TCL** (Fused): 
- **FIBA_309_PGS** (Fused): 

## Output Files

1. **01_raw_data.csv** - Raw data from input file
2. **02_af_protein_labels.csv** - Protein labels from column AF
3. **03_fused_protein_ids.csv** - Fused protein IDs from columns B and X
4. **04_patient_columns.csv** - Mapping of columns to patients
5. **05_protein_values_sample.csv** - Sample of extracted protein values
6. **06_protein_coverage.csv** - Coverage statistics for all proteins
7. **07_transformed_data.csv** - Final transformed dataset
8. **07_included_proteins.csv** - List of proteins included in final dataset
9. **08_protein_statistics.csv** - Statistics for each protein
10. **08_problematic_proteins.csv** - Proteins with quality issues
11. **08_protein_outliers.csv** - Detected outliers by protein and patient
12. **08_quality_summary.csv** - Summary of quality metrics
13. **09_validation_results.csv** - Results of validation checks
14. **09_value_validation_samples.csv** - Validation of sample values
15. **visualizations/** - Visualizations of protein distributions

## Next Steps

1. Review the quality metrics to identify problematic proteins
2. Examine the visualizations for proteins with quality flags
3. Consider filtering out proteins with high missingness (>50%)
4. Develop an imputation strategy for proteins with <20% missingness
5. Consider normalization approaches based on data distribution
6. Flag proteins with extreme outliers for special handling
7. Consult domain experts about proteins with unusual distributions