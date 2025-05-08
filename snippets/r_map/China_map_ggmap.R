# setwd('./Visualization')
# https://www.littlemissdata.com/blog/maps

library(ggmap)
library(ggplot2)
library(maps)
library(mapdata)

usa <- map_data("usa")
ggplot() +
  geom_polygon(data = usa, aes(x=long, y = lat, group = group), fill = NA, color = "red") +
  coord_fixed(1.3)