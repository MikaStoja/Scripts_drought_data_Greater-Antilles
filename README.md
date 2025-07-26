# Multimetric Drought Dataset for the Greater Antilles

This repository contains the Python and R scripts used to process and analyze data for the study:

**"Multimetric Drought Dataset for the Greater Antilles: A Resource for Environmental and Adaptation Studies"**

## Contents
- SPI, DPI, OSI, DER, and ROR calculation scripts
- Data preprocessing scripts
- Visualization scripts

## Script Execution Order
To ensure full reproducibility of the results, the R scripts should be run in the following order:

1. SPI_spatial_drought.R
   Calculates the SPI (1-12 temporal scales) at month timescale and generates spatial drought index over each island of Greater Antilles.
2. SPI_temporal_drought.R
   Computes the SPI (1-12 temporal scales) using averaged precipitation over each island of Greater Antilles.
3. Moisture_contribution.R
   Spatially averages the (E–P) field over each island of Greater Antilles, generating the time series of moisture contribution used in the drought attribution analysis.

The Python scripts can be executed independently in any order, depending on the specific analysis or figure to be reproduced.

## Datasets
- [MSWEP precipitation data](https://www.gloh2o.org/mswep/)
- [ERA5-Land reanalysis](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land-monthly-means?tab=download)
- [CubaPrec dataset](https://zenodo.org/records/7847844)
- Zenodo archive of this dataset: [https://doi.org/10.5281/zenodo.15411715](https://doi.org/10.5281/zenodo.15411715)

## Code Availability
All scripts used to generate the drought indices and visualisations are provided in this repository. 
Please refer to the Script Execution Order section below for recommended usage.
