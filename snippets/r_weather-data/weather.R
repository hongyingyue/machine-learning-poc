library(RNCEP)
library(tidyverse)


get_weather=function(RYear,RMonth,Lon,Lat){   
  wx.extent <- NCEP.gather(variable='air',level=850,months.minmax=c(RMonth,RMonth),
                           years.minmax=c(RYear,RYear),
                           lat.southnorth=c(Lat,Lat), lon.westeast=c(Lon,Lon),
                           reanalysis2=FALSE,return.units=TRUE)-273.15
  wx.ag <- NCEP.aggregate(wx.data=wx.extent, YEARS=TRUE, MONTHS=TRUE,DAYS=TRUE, 
                          HOURS=TRUE, fxn='mean')
  wx <- NCEP.array2df(wx.ag, var.names="temp")
  #w <- wx[1,4]
  return(wx)   
}

w=get_weather(2017,1,103,31)



  
  
wx.ag.t1 <- NCEP.aggregate(wx.data=wx.t1, YEARS=TRUE, MONTHS=TRUE,DAYS=TRUE, 
                          HOURS=FALSE,fxn = 'mean')
View(wx.ag.t1)

flight <- NCEP.flight(beg.loc=c(58.00,7.00), 
                      end.loc=c(53.00,7.00), begin.dt='2007-10-01 18:00:00',
                      flow.assist='NCEP.Tailwind', fa.args=list(airspeed=12),
                      path='loxodrome', calibrate.dir=FALSE, calibrate.alt=FALSE,
                      cutoff=0, when2stop='latitude', levels2consider=c(850,925),
                      hours=12, evaluation.interval=60, id=1, land.if.bad=FALSE,
                      reanalysis2 = FALSE, query=TRUE)


wx.t1 <- NCEP.gather(variable='air.2m', level='gaussian', 
                     months.minmax = c(1,12),years.minmax = c(2017,2017),
                     lat.southnorth = c(30,31), lon.westeast = c(104,104), 
                     reanalysis2 = FALSE, return.units = TRUE)-273.15

wx.t2 <- NCEP.gather(variable='shum.2m', level='gaussian', 
                     months.minmax = c(1,12),years.minmax = c(2017,2017),
                     lat.southnorth = c(30,31), lon.westeast = c(104,104), 
                     reanalysis2 = FALSE, return.units = TRUE)

wx.df1 <- NCEP.array2df(wx.data=wx.t1, var.names='temperature')
wx.df2 <- NCEP.array2df(wx.data=wx.t2, var.names='humidity')


wx.df <- wx.df1 %>%
  inner_join(wx.df2)



View(wx.df)
write_csv(wx.df, "hum.csv")