library(worldfootballR)
library(plyr)
library(readxl)
library(reshape)

allaSpelare <- read_excel("../data/spelarmappning.xlsx")
allaSpelare <- data.frame(allaSpelare)

fbData<-data.frame()
for(i in 1:nrow(allaSpelare)){
  
  if(!is.na(allaSpelare[i, "FB_URL"])){
  
  print(allaSpelare$Namn[i])
  print(allaSpelare$id[i])
  
  
  tempPlaying_time<-data.frame((matrix(ncol = 3, nrow = 0)))
  colnames(tempPlaying_time)<-c("player_url","Season","Comp")
  tempShooting<-data.frame((matrix(ncol = 3, nrow = 0)))
  colnames(tempShooting)<-c("player_url","Season","Comp")
  tempMisc<-data.frame((matrix(ncol = 3, nrow = 0)))
  colnames(tempMisc)<-c("player_url","Season","Comp")
  
  playing_time<-fb_player_season_stats(allaSpelare[i, "FB_URL"], stat_type="playing_time")
  if(nrow(playing_time)>0 & ncol(playing_time)>3){
    tempPlaying_time<-melt(playing_time,id=c("player_url","Season","Comp"))
  }
  
  shooting<-fb_player_season_stats(allaSpelare[i, "FB_URL"], stat_type="shooting")
  if(nrow(shooting)>0 & ncol(shooting)>3){
    tempShooting<-melt(shooting,id=c("player_url","Season","Comp"))
  }
  
  misc<-fb_player_season_stats(allaSpelare[i, "FB_URL"], stat_type="misc")
  if(nrow(misc)>0 & ncol(misc)>3){
    tempMisc<-melt(misc,id=c("player_url","Season","Comp"))
  }
  
  tempDf<-rbind(tempPlaying_time,tempShooting)
  tempDf<-rbind(tempDf,tempMisc)
  
  fbData<-rbind(fbData,tempDf)
  }
}

#Det finns en del överlappande information i player_time, shooting och misc
fbDataOut<-unique(fbData)

write.csv(x=fbDataOut,file="fbdata.csv")

tmData<-data.frame()
for(i in 1:nrow(allaSpelare)){
  if(!is.na(allaSpelare$TM_URL[i])){
    print(allaSpelare$Namn[i])
    print(allaSpelare$id[i])
    
    tempBio<-data.frame((matrix(ncol = 3, nrow = 0)))
    colnames(tempBio)<-c("URL","variable","value")
                        
    player_bio <- tm_player_bio(player_url = allaSpelare$TM_URL[i] )
    
    player_bio <- as.data.frame(player_bio)
    
    tempBio<-melt(player_bio,id=c("URL"))
    
    tmData<-rbind(tmData,tempBio)
  }
}

tmDataOut<-unique(tmData)
write.csv(x=tmDataOut,file="tmdata.csv")
