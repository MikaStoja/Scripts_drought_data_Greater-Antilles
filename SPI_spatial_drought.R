library(SPEI)
library(ncdf4)

# Read the data files
pre_nc <- nc_open("/path/monthly_MSWEP_1980_2023_CUBA.nc")

#pre_nc <- nc_open("/path/monthly_MSWEP_1980_2023_JAMAICA.nc")

#pre_nc <- nc_open("/path/monthly_MSWEP_1980_2023_LA_ESPAÑOLA.nc")

#pre_nc <- nc_open("/path/monthly_MSWEP_1980_2023_PUERTO_RICO.nc")


# Extract precipitation data
pre <- ncvar_get(pre_nc, "precipitation")  
lats <- ncvar_get(pre_nc, "lat")
lons <- ncvar_get(pre_nc, "lon")
times <- ncvar_get(pre_nc, "time") 
times <- 0:527

# Initialize SPI array
spi_1 <- array(NA, dim=dim(pre))

# COMPUTE SPI

for(lon in 1:length(lons)){
  for(lat in 1:length(lats)){
    spi_1[lon, lat, ] <- spi(data=ts(pre[lon, lat, ], freq=12, start=c(1980,1)), 
                             scale=1, ref.start=c(1980,1), ref.end=c(2023,12), 
                             na.rm=TRUE)$fitted
  }
}

# Define dimensions
lons_nc <- ncdim_def("lon", "degrees_east", lons ) # longitudes
lats_nc <- ncdim_def("lat", "degrees_north", lats ) # latitudes
times_nc <- ncdim_def("time", "months since 1980-1-1", times ) # time

# Define variables
spi_nc <- ncvar_def("spi", "-", list(lons_nc, lats_nc, times_nc), -999.9, 
                    longname="Standardized Precipitation Index", prec="double")

# Replace infinite and NaN values with NA
spi_1[is.infinite(spi_1)] <- NA
spi_1[is.nan(spi_1)] <- NA

# Create NetCDF file
output_fname <- "/path/spi1_MSWEP_CUBA.nc"

#output_fname <- "/path/spi1_MSWEP_JAMAICA.nc"

#output_fname <- "/path/spi1_MSWEP_LA_ESPAÑOLA.nc"

#output_fname <- "/path/spi1_MSWEP_PUERTO_RICO.nc"

spi <- nc_create(output_fname, list(spi_nc))

# Insert data into NetCDF file
ncvar_put(spi, "spi", spi_1)
ncatt_put(spi, "lon", "axis", "X")
ncatt_put(spi, "lat", "axis", "Y")
ncatt_put(spi, "time", "axis", "T")

# Close NetCDF file
nc_close(spi)
