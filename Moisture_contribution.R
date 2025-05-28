library(ncdf4)

pre_nc <- nc_open("Cuba_fw.nc")

pre <- ncvar_get(pre_nc, "pre") #pre
lats <- ncvar_get(pre_nc, "lat")
lons <- ncvar_get(pre_nc, "lon")
times <- 0:515

  mask1 <- nc_open(paste("mask_Cuba.nc")) 
  m1 <- ncvar_get(mask1, "source")
  pre1 <- array(NA, dim=dim(pre))
  for(lon in 1:length(lons)){
    for(lat in 1:length(lats)){
      pre1[lon,lat,] <- pre[lon,lat,]*m1[lon,lat]
      } 
    }
  mean_pre1 <- apply(pre1,c(3),mean, na.rm=TRUE)
write.table(mean_pre1,paste('Cuba_fw_moisture_contribution.csv',sep=""),sep=';',row.names=FALSE)

