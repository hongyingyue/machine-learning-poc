# Code snippets in R/Python


## Map
If you want to download more specific province of China, you could download from [NGCC](http://www.webmap.cn/mapDataAction.do?method=forw&resType=5&storeId=2&storeName=%E5%9B%BD%E5%AE%B6%E5%9F%BA%E7%A1%80%E5%9C%B0%E7%90%86%E4%BF%A1%E6%81%AF%E4%B8%AD%E5%BF%83)

```bash
Rscript China_map_bubble.R
Rscript Chine_map_great_circle.R
```

## weather
-  Get the data from RNCEP. Further reading [this posting](https://dominicroye.github.io/en/2018/access-to-climate-reanalysis-data-from-r/)

- check the official [China weather API](http://data.cma.cn/Market/MarketList.html), or download through FTP directly from [NOAA](https://www.esrl.noaa.gov/psd/data/gridded/help.html#FTP)

```shell
install.packages("RNCEP")
# In Mac,  I have to install xquartz: `brew cask install xquartz`, and restart
```
