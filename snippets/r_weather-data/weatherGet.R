install.packages("RNCEP")


library(lubridate)
library(RNCEP)


get_weather=function(RYear,RMonth,Lon,Lat){   
  wx.extent <- NCEP.gather(variable='air',level=850,months.minmax=c(RMonth,RMonth),years.minmax=c(RYear,RYear),lat.southnorth=c(Lat,Lat), lon.westeast=c(Lon,Lon),reanalysis2=FALSE,return.units=TRUE)-273.15
  wx.ag <- NCEP.aggregate(wx.data=wx.extent, YEARS=TRUE, MONTHS=TRUE,DAYS=TRUE, HOURS=FALSE, fxn='mean')
  wx <- NCEP.array2df(wx.ag, var.names=NULL)
  w <- wx[1,4]
  return(w)   
}

w=get_weather(2017,1,103,31)

View(w)


wx.extent1 <- NCEP.gather(variable='air', level=850,
                          months.minmax=c(9,10), years.minmax=c(1998,1998),
                          lat.southnorth=c(50,51), lon.westeast=c(5,6),
                          reanalysis2 = FALSE, return.units = TRUE)

View(wx.extent1)

dimnames(wx.extent1)[[1]]
dimnames(wx.extent1)[[2]]
dimnames(wx.extent1)[[3]]

class(wx.extent1)


wx.df <- NCEP.array2df(wx.extent1[,,])
View(wx.df)
