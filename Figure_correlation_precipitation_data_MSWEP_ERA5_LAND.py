import xarray as xr
import numpy as np
from scipy.stats import pearsonr
import cftime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

plt.rcParams.update({'font.size': 13})

# Function to manually convert time
def convert_time(ds, time_name='time'):
    ds = ds.rename({time_name: 'time'})
    ds['time'] = xr.cftime_range(start='1980-01-01', periods=ds.sizes['time'], freq='MS')
    return ds

# Load datasets without decoding time
file1 = 'MSWEP_1980_2023_data.nc'
file2 = 'ERA5_LAND_1980_2023_data.nc'

ds1 = xr.open_dataset(file1, decode_times=False)
ds2 = xr.open_dataset(file2, decode_times=False)

# Convert time in both datasets
ds1 = convert_time(ds1, time_name='time')
ds2 = convert_time(ds2, time_name='valid_time')  # Rename and convert

# Adjust longitudes if necessary
def adjust_longitudes(ds):
    if ds.lon.max() > 180:
        ds['lon'] = (((ds['lon'] + 180) % 360) - 180)
    return ds.sortby('lon')

ds1 = adjust_longitudes(ds1)
ds2 = adjust_longitudes(ds2)

# Reinterpolate to ensure coordinates match
ds2_interp = ds2.interp(lat=ds1.lat, lon=ds1.lon)

# Select variables
var1 = ds1['precipitation']
var2 = ds2_interp['tp'] * 1000  # convert from m to mm

# Compute Pearson correlation and p-value point by point
def compute_correlation(x, y):
    mask = ~np.isnan(x) & ~np.isnan(y)
    if mask.sum() > 2:
        return pearsonr(x[mask], y[mask])
    else:
        return np.nan, np.nan

results = xr.apply_ufunc(
    compute_correlation,
    var1, var2,
    input_core_dims=[['time'], ['time']],
    output_core_dims=[[], []],
    vectorize=True,
    dask='parallelized',
    output_dtypes=[float, float]
)

correlation, p_value = results

# Save results
correlation.name = 'correlation'
p_value.name = 'p_value'

result = xr.Dataset({'correlation': correlation, 'p_value': p_value})
result.to_netcdf('correlation_MSWEP_vs_ERA5_Land.nc')

# Plot correlation with borders and labels
plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
bounds = [float(ds1.lon.min()), float(ds1.lon.max()), float(ds1.lat.min()), float(ds1.lat.max())]
ax.set_extent(bounds, crs=ccrs.PlateCarree())

c = ax.pcolormesh(ds1.lon, ds1.lat, correlation, cmap='Reds', vmin=0, vmax=1, transform=ccrs.PlateCarree())
cb = plt.colorbar(c, ax=ax, orientation='vertical', shrink=0.5, label='Pearson Correlation')

# Add borders and coastlines
ax.add_feature(cfeature.BORDERS, linewidth=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

# Configure gridlines and labels
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.0, linestyle='--')
gl.top_labels = False
gl.right_labels = False

plt.savefig('correlation_MSWEP_vs_ERA5.png', dpi=300, bbox_inches='tight')
plt.show()

print("Computation completed. Results saved as 'correlation_MSWEP_vs_ERA5_Land.nc' and plot saved as 'correlation_MSWEP_vs_ERA5_Land.png'.")

