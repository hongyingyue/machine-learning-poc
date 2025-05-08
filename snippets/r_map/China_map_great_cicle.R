#setwd('./Visualization')
library(ggplot2)
library(maptools)
library(geosphere)
library(plyr)

#Sales data import and pro-processing
MBsales<-read.csv("../../data/map_R_circle.csv",sep=';',header=T)
MBsales2016<-MBsales[MBsales$Year==2016,]
Csales2016<-MBsales[MBsales$Model=="C CLASS SEDAN"& MBsales$Year==2016 & MBsales$CBU.PbP=="PBP",]
Csales2016<-data.frame(Csales2016)
Sales<-ddply(Csales2016,.(City),summarize,Sales=sum(Total.Year))
Sales<-Sales[order(-Sales$Sales),]
Sales$id<-as.character(c(1:nrow(Sales)))
Sales$City<-gsub("'","",Sales$City)
Sales$City<-gsub("Nanning City","NANNING",Sales$City)
Sales$City<-gsub("Fu2zhou","FUZHOU",Sales$City)
Sales$City<-gsub("Liuzhou City","Liuzhou",Sales$City)
Sales$City<-gsub("Foshan Nanhai","Foshan",Sales$City)
Sales$City<-gsub("Foshan Shunde","Foshan",Sales$City)
Sales$City<-toupper(Sales$City)

#China CityGeocode data import
Citygeocode<-read.csv("../../assets/city_geocode_lookup.csv",sep=',',header=T)
Citygeocode$City<-toupper(Citygeocode$City)
#selected<-toupper(c("Beijing", "Shanghai", "Guangzhou",?"Foshan", "Xi��an", "Chengdu", "Suzhou", "Dalian"))
#selected<-Citygeocode[Citygeocode$City %in% selected,]

Sales<-merge(Sales,Citygeocode,by.x='City',by.y='City',all.x=TRUE)

BBACcode=c(116.3,39.9)
Sales<-Sales[complete.cases(Sales),]
routes = gcIntermediate(BBACcode,Sales[,c('Lon', 'Lat')], 300, breakAtDateLine=FALSE, addStartEnd=TRUE, sp=TRUE)

fortify.SpatialLinesDataFrame = function(model, data, ...) {ldply(model@lines, fortify)}
fortifiedroutes = fortify.SpatialLinesDataFrame(routes) 

greatcircles = merge(fortifiedroutes, Sales, all.x=T, by="id")

ChinaProvince<-readShapePoly("../../assets/province.shp")
Chinamap <- fortify(ChinaProvince)

theme_map <- list(theme(panel.grid.minor = element_blank(),
 panel.grid.major = element_blank(),
 panel.border = element_blank(),
 axis.line = element_blank(),
 axis.text.x = element_blank(),
 axis.text.y = element_blank(),
 axis.ticks = element_blank(),
 axis.title.x = element_blank(),
 axis.title.y = element_blank(),
 panel.background = element_blank(),
 plot.background = element_blank()))

p1<-ggplot(Sales)+
 geom_path(aes(x = long, y = lat, group = id), size=0.2, data=Chinamap)+
 geom_line(aes(long,lat,group=id), data=greatcircles, color='grey', alpha=0.25, size=0.15)+
 geom_point(aes(Lon,Lat,group=id,alpha=Sales,size=Sales),color="red")+scale_size(range = c(0, 4))+
 geom_text(aes(Lon,Lat,label=City),data=Sales[1:5,],hjust =-0.4,check_overlap = TRUE,size=2.5)+
 scale_alpha_continuous(range = c(0.25, 0.8))+coord_map()+ylim(14,55)+theme_map

ggsave("../../assets/images/China map great circle.png", p1, height=4.8, width=9.5)