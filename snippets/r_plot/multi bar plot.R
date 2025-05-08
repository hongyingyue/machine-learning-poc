library(readxl)
library(plyr)
library(ggplot2)
library(ggthemes)
library(gridExtra)
# setwd(".\\06-QFS_month")


MB=data.frame(read_excel("MB Online master sheet_201812.xlsx",sheet=1,col_names=TRUE))
MB$Complaint=paste(MB$QFS_Tier1, MB$QFS_Tier3,sep=" ")
MBagg<-ddply(MB,.(Carline,Complaint),summarize,Value=length(Complaint))
MBagg<-MBagg[order(MBagg$Value,decreasing=T),]
MBagg1<-by(MBagg,MBagg['Carline'],head,n=3)
MBagg2<-Reduce(rbind,MBagg1)
MBagg2<-MBagg2[MBagg2$Carline %in% c("V205","V213","X253","X156"),]
MBagg2$Carline<-factor(MBagg2$Carline, levels=c("V205","V213","X253","X156"))

max=max(MBagg2[,"Value"])
n=1

p<-list()
for (i in c("V205","V213","X253","X156"))
{
MBcar<-MBagg2[MBagg2$Carline==i,]
p[[n]]<-ggplot(MBcar)+geom_bar(aes(x=reorder(Complaint,Value),y=Value),stat='identity',fill="#d3ba68",alpha=0.7)+ylim(0,max)+geom_text(aes(x=Complaint,y=0,label=Complaint),size=4,hjust=0)+coord_flip()+ theme_wsj()+theme(axis.text.y = element_blank(),axis.text.x = element_text(size = 7))
n=n+1
}
p2<-grid.arrange(p[[1]],p[[2]],p[[3]],p[[4]],ncol = 1, nrow = 4)





BMW=data.frame(read_excel("BMW Online master sheet_201812.xlsx",sheet=1,col_names=TRUE))
BMW$Complaint=paste(BMW$QFS_Tier1, BMW$QFS_Tier3,sep=" ")
BMWagg<-ddply(BMW,.(Type.Class,Complaint),summarize,Value=length(Complaint))
BMWagg<-BMWagg[order(BMWagg$Value,decreasing=T),]
BMWagg1<-by(BMWagg,BMWagg['Type.Class'],head,n=3)
BMWagg2<-Reduce(rbind,BMWagg1)
BMWagg2<-BMWagg2[BMWagg2$Type.Class %in% c("3-Series","5-Series","X3","X1"),]
BMWagg2$Type.Class<-factor(BMWagg2$Type.Class, levels=c("3-Series","5-Series","X3","X1"))
max=max(BMWagg2[,"Value"])
n=5
for (i in c("3-Series","5-Series","X3","X1"))
{
BMWcar<-BMWagg2[BMWagg2$Type.Class==i,]
p[[n]]<-ggplot(BMWcar)+geom_bar(aes(x=reorder(Complaint,Value),y=Value),stat='identity',fill="#d3ba68",alpha=0.7)+ylim(0,max)+geom_text(aes(x=Complaint,y=0,label=Complaint),size=4,hjust=0)+coord_flip()+ theme_wsj()+theme(axis.text.y = element_blank(),axis.text.x = element_text(size = 7))
n=n+1}
p2<-grid.arrange(p[[5]],p[[6]],p[[7]],p[[8]],ncol = 1, nrow = 4)






Audi=data.frame(read_excel("Audi Online master sheet_201812.xlsx",sheet=1,col_names=TRUE))
Audi$Complaint=paste(Audi$QFS_Tier1, Audi$QFS_Tier3,sep=" ")
Audiagg<-ddply(Audi,.(Type.Class,Complaint),summarize,Value=length(Complaint))
Audiagg<-Audiagg[order(Audiagg$Value,decreasing=T),]
Audiagg1<-by(Audiagg,Audiagg['Type.Class'],head,n=3)
Audiagg2<-Reduce(rbind,Audiagg1)
Audiagg2<-Audiagg2[Audiagg2$Type.Class %in% c("A4L","A6L","Q5","Q3"),]
Audiagg2$Type.Class<-factor(Audiagg2$Type.Class, levels=c("A4L","A6L","Q5","Q3"))
max=max(Audiagg2[,"Value"])
n=9
for (i in c("A4L","A6L","Q5","Q3"))
{
Audicar<-Audiagg2[Audiagg2$Type.Class==i,]
p[[n]]<-ggplot(Audicar)+geom_bar(aes(x=reorder(Complaint,Value),y=Value),stat='identity',fill="#d3ba68",alpha=0.7)+ylim(0,max)+geom_text(aes(x=Complaint,y=0,label=Complaint),size=4,hjust=0)+coord_flip()+ theme_wsj()+theme(axis.text.y = element_blank(),axis.text.x = element_text(size = 7))
n=n+1
}
p2<-grid.arrange(p[[9]],p[[10]],p[[11]],p[[12]],ncol = 1, nrow = 4)






Lexus=data.frame(read_excel("LEXUS Online master sheet_201812.xlsx",sheet=1,col_names=TRUE))
Lexus$Complaint=paste(Lexus$QFS_Tier1, Lexus$QFS_Tier3,sep=" ")
Lexusagg<-ddply(Lexus,.(Type.Class,Complaint),summarize,Value=length(Complaint))
Lexusagg<-Lexusagg[order(Lexusagg$Value,decreasing=T),]
Lexusagg1<-by(Lexusagg,Lexusagg['Type.Class'],head,n=3)
Lexusagg2<-Reduce(rbind,Lexusagg1)
Lexusagg2<-Lexusagg2[Lexusagg2$Type.Class %in% c("IS","ES","NX","CT"),]
Lexusagg2$Type.Class<-factor(Lexusagg2$Type.Class, levels=c("IS","ES","NX","CT"))
max=max(Lexusagg2[,"Value"])
n=13
for (i in c("IS","ES","NX","CT"))
{
Lexuscar<-Lexusagg2[Lexusagg2$Type.Class==i,]
p[[n]]<-ggplot(Lexuscar)+geom_bar(aes(x=reorder(Complaint,Value),y=Value),stat='identity',fill="#d3ba68",alpha=0.7)+ylim(0,max)+geom_text(aes(x=Complaint,y=0,label=Complaint),size=4,hjust=0)+coord_flip()+ theme_wsj()+theme(axis.text.y = element_blank(),axis.text.x = element_text(size = 7))
n=n+1
}
p2<-grid.arrange(p[[13]],p[[14]],p[[15]],ncol = 1, nrow = 4)


p3<-grid.arrange(p[[1]],p[[5]],p[[9]],p[[13]],p[[2]],p[[6]],p[[10]],p[[14]],p[[3]],p[[7]],p[[11]],p[[15]],p[[4]],p[[8]],p[[12]],nrow = 4,ncol = 4)




#p<-ggplot(MBagg2)+geom_bar(aes(x=Complaint,y=Value),stat='identity',fill='yellow',alpha=0.5)
#p<-p+facet_wrap(~Carline,nrow=4,scales="free")+ylim(0,25)
#p<-p+geom_text(aes(x=Complaint,y=0,label=Complaint),hjust=0)
#p+coord_flip()+ theme_wsj() 