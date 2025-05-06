# setwd('./Visualization')
library(plyr)
library(ggplot2)
library(maptools)
library(reshape2)
library(gridExtra)
library(rgdal)

#import the data
Data<-as.data.frame(read.csv("../../data/map_R_province.csv",sep=';',header=T))

#aggregrate
Data_agg<-ddply(Data,.(City),summarize,Complaints_value=length(City))
City_code<-read.table("../../assets/city_geocode_lookup.csv", sep=',', header=T)
Da<-merge(Data_agg,City_code,by.x='City',by.y='City')

#Import the map data
province<-readShapePoly("../../assets/province.shp")
chinamap<-fortify(province)
provincedata<-data.frame(province@data,id=seq(0:924)-1)
china_mapdata<-join(chinamap, provincedata, type = "full")

#plot
p1<-ggplot(data = chinamap) + geom_path(aes(x = long, y = lat, group = id),size=0.2, colour="black")+coord_map(ylim = c(14,55))
p1<-p1 + geom_polygon(aes(x=long,y=lat,group=id),fill = 'grey90',size=0.1, alpha=0.4)
p1<-p1 + geom_point(data=Da, aes(x=Lon, y=Lat, size=Complaints_value),color='red',alpha=0.45)+scale_size(range = c(0,4))
p1<-p1 + annotate("text",x = 84,y =20, label = "YueTan",family = "serif", fontface = "italic", colour = "black", size = 4)

theme_map <- list(theme(panel.grid.minor = element_blank(),
 panel.grid.major = element_blank(),
 panel.border = element_blank(),
 axis.line = element_blank(),
 axis.text.x = element_blank(),
 axis.text.y = element_blank(),
 axis.ticks = element_blank(),
 axis.title.x = element_blank(),
 axis.title.y = element_blank(),
 panel.background = element_rect(fill="transparent"),
 plot.background = element_rect(fill = "transparent"),
 legend.background = element_rect(fill = "transparent"),
 legend.box.background = element_rect(fill = "transparent")))

p1<-p1+theme_map+ggtitle('Welcome to follow')+theme(plot.title = element_text(family = 'Helvetica',face = "bold"))
ggsave("../../assets/images/China map bubble plot.png", p1, height=4.8, width=9.5)
