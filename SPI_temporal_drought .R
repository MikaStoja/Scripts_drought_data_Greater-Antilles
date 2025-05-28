# LOAD PRECIPITATION AND ETO DATA

library(SPEI)
library(ncdf4)

# Open the precipitation dataset
pre_nc <- nc_open("/path/monthly_MSWEP_data_1980_2023_Greater_Antilles.nc")

# Extract precipitation data
pre <- ncvar_get(pre_nc, "precipitation")

# Extract latitude, longitude, and time data
lats <- ncvar_get(pre_nc, "lat")
lons <- ncvar_get(pre_nc, "lon")
times <- 0:527

# LOAD MASK DATA

mask1 <- nc_open(paste("/path/mask_Cuba.nc")) 
#mask1 <- nc_open(paste("/path/mask_Jamaica.nc")) 
#mask1 <- nc_open(paste("/path/mask_Puerto_Rico.nc")) 
#mask1 <- nc_open(paste("/path/mask_La_Española.nc")) 
m1 <- ncvar_get(mask1, "mask")


pre1 <- array(NA, dim=dim(pre))

# Apply mask to precipitation data
for(lon in 1:length(lons)) {
  for(lat in 1:length(lats)) {
    pre1[lon, lat, ] <- pre[lon, lat, ] * m1[lon, lat]
  }
}

# Calculate mean precipitation and ETO for each region
mean_pre1 <- apply(pre1, c(3), mean)

# CALCULATE SPI FOR SCALES FROM 1 TO 48 MONTHS

spi1 <- matrix(data=NA, nrow=528, ncol=48)
for (i in 1:48) {
  spi1[,i] <- spi(data=ts(mean_pre1, freq=12, start=c(1980,1)), scale=i, ref.start=c(1980,1), ref.end=c(2023,12), distribution="Gamma")$fitted
}

# SAVE RESULTS TO CSV FILES
write.table(spi1, paste('/path/SPI_CUBA_1980_2023.csv', sep=""), sep=';', row.names=FALSE)
#write.table(spi1, paste('/path/SPI_JAMAICA_1980_2023.csv', sep=""), sep=';', row.names=FALSE)
#write.table(spi1, paste('/path/SPI_PUERTO_RICO_1980_2023.csv', sep=""), sep=';', row.names=FALSE)
#write.table(spi1, paste('/path/SPI_LA_ESPAÑOLA_1980_2023.csv', sep=""), sep=';', row.names=FALSE)
