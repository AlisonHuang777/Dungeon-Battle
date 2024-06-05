import pygame as pg
from pygame.locals import *
from os.path import join,exists
from math import floor,ceil,sqrt,sin,cos,pi
from random import random,randint,randrange,uniform,choice,choices,sample
def readLayout(id):
    memory1=open(join('dgbt_data','layout',id+'.txt')).read().split('\n')
    memory2=[]
    for item in memory1:
        memory2.append(item.split())
    memory1.clear()
    for i in range(len(memory2[0])):
        memory1.append([])
        for j in range(len(memory2)):
            memory1[-1].append(memory2[j][i])
    return(memory1)
def construct1dList(length,item):
    array=[]
    for _ in range(length):
        array.append(item)
    return(array)
def construct2dList(length,depth,item):
    array=[]
    for i in range(length):
        array.append([])
        for _ in range(depth):
            array[i].append(item)
    return(array)
def getHitbox(posX,posY,size=1.0):
    hitbox=[False,False,False,False]
    if levelLayout[floor(posX+size)][floor(posY+size)] in BLOCKABLE:
        hitbox[0]=True
    if levelLayout[floor(posX)][floor(posY+size)] in BLOCKABLE:
        hitbox[1]=True
    if levelLayout[floor(posX)][floor(posY)] in BLOCKABLE:
        hitbox[2]=True
    if levelLayout[floor(posX+size)][floor(posY)] in BLOCKABLE:
        hitbox[3]=True
    return(tuple(hitbox))
def blockingAdjust(posX,posY,size=1.0):
    hitbox=getHitbox(posX,posY,size)
    if   hitbox==(True,False,False,False):
        if posX%1>posY%1:
            return(posX,floor(posY))
        elif posX%1<posY%1:
            return(floor(posX),posY)
        else:
            return(floor(posX),floor(posY))
    elif hitbox==(False,True,False,False):
        if 1-posX%1>posY%1:
            return(posX,floor(posY))
        elif 1-posX%1<posY%1:
            return(ceil(posX),posY)
        else:
            return(ceil(posX),floor(posY))
    elif hitbox==(False,False,True,False):
        if 1-posX%1>1-posY%1:
            return(posX,ceil(posY))
        elif 1-posX%1<1-posY%1:
            return(ceil(posX),posY)
        else:
            return(ceil(posX),ceil(posY))
    elif hitbox==(False,False,False,True):
        if posX%1>1-posY%1:
            return(posX,ceil(posY))
        elif posX%1<1-posY%1:
            return(floor(posX),posY)
        else:
            return(floor(posX),ceil(posY))
    elif hitbox==(True,False,False,True):
        return(floor(posX),posY)
    elif hitbox==(False,True,True,False):
        return(ceil(posX),posY)
    elif hitbox==(True,True,False,False):
        return(posX,floor(posY))
    elif hitbox==(False,False,True,True):
        return(posX,ceil(posY))
    elif hitbox==(False,True,False,True):
        if   posX>round(posX) or posY>round(posY):
            return(floor(posX),floor(posY))
        elif posX<round(posX) or posY<round(posY):
            return(ceil(posX),ceil(posY))
        else:
            return(posX,posY)
    elif hitbox==(True,False,True,False):
        if   posX<round(posX) or posY>round(posY):
            return(ceil(posX),floor(posY))
        elif posX>round(posX) or posY<round(posY):
            return(floor(posX),ceil(posY))
        else:
            return(posX,posY)
    elif hitbox==(True,True,False,True):
        return(floor(posX),floor(posY))
    elif hitbox==(True,True,True,False):
        return(ceil(posX),floor(posY))
    elif hitbox==(False,True,True,True):
        return(ceil(posX),ceil(posY))
    elif hitbox==(True,False,True,True):
        return(floor(posX),ceil(posY))
    else:
        return(posX,posY)
def reflectingAdjust(posX,posY,deltaX,deltaY,size=1.0):
    hitbox=getHitbox(posX,posY,size)
    dx=0
    dy=0
    if hitbox.count(True)==1:
        if   hitbox[0]:
            dx=posX%1
            dy=posY%1
        elif hitbox[1]:
            dx=1-posX%1
            dy=posY%1
        elif hitbox[2]:
            dx=1-posX%1
            dy=1-posY%1
        elif hitbox[3]:
            dx=posX%1
            dy=1-posY%1
        if dx>dy:
            return(deltaX,-deltaY)
        elif dx<dy:
            return(-deltaX,deltaY)
        else:
            return(-deltaX,-deltaY)
    elif hitbox==(True,False,False,True) or hitbox==(False,True,True,False):
        return(-deltaX,deltaY)
    elif hitbox==(True,True,False,False) or hitbox==(False,False,True,True):
        return(deltaX,-deltaY)
    elif hitbox.count(False)==1:
        return(-deltaX,-deltaY)
    else:
        return(deltaX,deltaY)
def distance(x1,y1,x2,y2):
    return(sqrt((x1-x2)**2+(y1-y2)**2))
def generateDelta(oriX,oriY,endX,endY):
    return((endX-oriX)/distance(oriX,oriY,endX,endY),(endY-oriY)/distance(oriX,oriY,endX,endY))
def rotateDelta(deltaValue,deg):
    return(deltaValue[0]*cos(deg/180*pi)-deltaValue[1]*sin(deg/180*pi),deltaValue[0]*sin(deg/180*pi)+deltaValue[1]*cos(deg/180*pi))
def entityVisible(x1,y1,x2,y2,r):
    if distance(x1,y1,x2,y2)>r:
        return(False)
    else:
        dx=(x2-x1)/r
        dy=(y2-y1)/r
        for i in range(1,ceil(r+1)):
            if levelLayout[int(x1+0.5+dx*i)][int(y1+0.5+dy*i)] in BLOCKABLE:
                return(False)
        return(True)
def wander(posX,posY,tgtX,tgtY):
    if random()>0.8:
        return(0,0)
    tgtX+=uniform(-1.0,1.0)
    tgtY+=uniform(-1.0,1.0)
    dx=(tgtX-posX)/distance(posX,posY,tgtX,tgtY)
    dy=(tgtY-posY)/distance(posX,posY,tgtX,tgtY)
    return(dx,dy)
def damagePlayer(amount):
    amount-=playerData['def']
    if amount<=0:
        return(None)
    playerData['shield_regen_cd']=180
    playerData['red_cd']=10
    for _ in range(amount):
        if   playerData['shield']>0:
            playerData['shield']-=1
        elif playerData['hp']>0:
            playerData['hp']-=1
        else:
            break
def render(textureId,posX,posY,flipped=False):
    screenWidth,screenHeight=pg.display.get_window_size()
    blitX=screenWidth //2+TEXTURE_RESOLUTION*(posX-playerData['x'])-TEXTURE_RESOLUTION//2
    blitY=screenHeight//2+TEXTURE_RESOLUTION*(posY-playerData['y'])-TEXTURE_RESOLUTION//2
    if blitX+TEXTURE_RESOLUTION>0 and blitX<screenWidth and blitY+TEXTURE_RESOLUTION>0 and blitY<screenHeight:
        if flipped:
            screen.blit(TEXTURE[textureId+'_flipped'],(blitX,blitY))
        else:
            screen.blit(TEXTURE[textureId],(blitX,blitY))
pg.init()
pg.display.set_caption('Dungeon Battle')
screen=pg.display.set_mode(flags=FULLSCREEN)
clock=pg.time.Clock()
active=True
TICKRATE=60#adjustable
MOVEMENT_TICKRATE_ADJUSTS_BY_FPS=False#adjustable
SHOW_FPS=True
FONT=pg.font.Font(join('dgbt_data','font.ttf'),30)
TEXTURE={}
TEXTURE_RESOLUTION=64#adjustable
TEXTURE_VARIANTS={'wall':(2,2,1),'floor':(7,2,1),'portal':6,'gunner_foe_blue':4,'gunner_foe_green':4,'gunner_foe_yellow':4}#Tuple: Possibility weights (Adjustable); Any integer: Animation frames (Not adjustable)
TILE_TEXTURE_ID={'#':'wall','_':'floor','-':'door_open','+':'door_closed','$':'treasure','S':'treasure_looted','@':'portal'}
CHUNK_SIZE=25
LEVEL_DEPTH=3#adjustable
ROOM_VARIANTS={}
BLOCKABLE=('#','+')
diffculty=-1
score=-30
generateNewLevel=True
levelChunkData=[]
levelChunkSize=(0,0)
levelLayout=[]
levelSize=(0,0)
roomGenerationOrigin=[0,0]
roomGenerationDirection=[]
mergingRoomLayout=[]
mergingRoomSize=(0,0)
textureVariationSelection=[]
treasureLoot=['hp','shield','atk','atk_sep','def','score']
treasureLocation=[]
portalLocation=(0,0)
playerData={'x':0.0,'y':0.0,'hp':10,'hp_max':10,'shield':5,'shield_max':5,'atk':2,'atk_sep':30,'atk_cd':0,'def':0,'spd':8.0,'shield_regen_cd':0,'red_cd':0}
entityData=[]
blackScreenTransition=0
inBattle=False
spawnableTile=[]
keyPressed=None
cursorPosition=(0,0)
mouseLeftButtonPressed=False
fps=0
movementTickrate=TICKRATE
animationTick=0
if True:#load texture
    TEXTURE['status_interface']=pg.transform.scale(pg.image.load(join('dgbt_data','texture','status_interface.png')),(256,128)).convert()
    for fileName in ('door_open','door_closed','treasure','treasure_looted','unknown'):
        TEXTURE[fileName]=pg.transform.scale(pg.image.load(join('dgbt_data','texture',fileName+'.png')),(TEXTURE_RESOLUTION,TEXTURE_RESOLUTION)).convert()
    for fileName in ('foe_spawnpoint','player_bullet','foe_bullet_blue','foe_bullet_green','foe_bullet_yellow'):
        TEXTURE[fileName]=pg.transform.scale(pg.image.load(join('dgbt_data','texture',fileName+'.png')),(TEXTURE_RESOLUTION,TEXTURE_RESOLUTION)).convert_alpha()
    for fileName in ('player','player_red','player_attack','player_attack_red','player_dead','melee_foe_idle','melee_foe_attack','melee_foe_dead','gunner_foe_blue_dead','gunner_foe_green_dead','gunner_foe_yellow_dead'):
        TEXTURE[fileName]=pg.transform.scale(pg.image.load(join('dgbt_data','texture',fileName+'.png')),(TEXTURE_RESOLUTION,TEXTURE_RESOLUTION)).convert_alpha()
        TEXTURE[fileName+'_flipped']=pg.transform.flip(TEXTURE[fileName],True,False).convert_alpha()
    index=0
    weightArray=[]
    for key in TEXTURE_VARIANTS.keys():
        while exists(join('dgbt_data','texture',key+str(index)+'.png')):
            TEXTURE[key+str(index)]=pg.transform.scale(pg.image.load(join('dgbt_data','texture',key+str(index)+'.png')),(TEXTURE_RESOLUTION,TEXTURE_RESOLUTION)).convert()
            index+=1
        if type(TEXTURE_VARIANTS[key])==int:
            if TEXTURE_VARIANTS[key]<index:
                TEXTURE_VARIANTS[key]=1
        elif len(TEXTURE_VARIANTS[key])!=index:
            TEXTURE_VARIANTS[key]=[]
            for index in range(index):
                TEXTURE_VARIANTS[key].append(index)
        else:
            index=0
            for weight in TEXTURE_VARIANTS[key]:
                for _ in range(weight):
                    weightArray.append(index)
                index+=1
            TEXTURE_VARIANTS[key]=tuple(weightArray)
            weightArray.clear()
        index=0
    del weight
    del weightArray
    for fileName in ('gunner_foe_blue','gunner_foe_green','gunner_foe_yellow'):
        for index in range(TEXTURE_VARIANTS[fileName]):
            TEXTURE[fileName+str(index)+'_flipped']=pg.transform.flip(TEXTURE[fileName+str(index)],True,False).convert_alpha()
    index=0
    del fileName
for key in ('battle','treasure'):#load room variants
    ROOM_VARIANTS[key]=0
    while exists(join('dgbt_data','layout',key+str(index)+'.txt')):
        ROOM_VARIANTS[key]+=1
        index+=1
    index=0
del key
while active:
    if generateNewLevel:#generate new level
        levelChunkData.clear()
        levelLayout=construct2dList(CHUNK_SIZE,CHUNK_SIZE,'.')
        mergingRoomLayout=readLayout('spawn')
        mergingRoomSize=(len(mergingRoomLayout),len(mergingRoomLayout[0]))
        for blockX in range(mergingRoomSize[0]):
            for blockY in range(mergingRoomSize[1]):
                levelLayout[(CHUNK_SIZE-mergingRoomSize[0])//2+blockX][(CHUNK_SIZE-mergingRoomSize[1])//2+blockY]=mergingRoomLayout[blockX][blockY]
        levelSize=(len(levelLayout),len(levelLayout[0]))
        levelChunkData.append([{'type':'spawn','x':(CHUNK_SIZE-mergingRoomSize[0])//2,'y':(CHUNK_SIZE-mergingRoomSize[1])//2,'width':mergingRoomSize[0],'height':mergingRoomSize[1]}])
        levelChunkSize=(len(levelChunkData),len(levelChunkData[0]))
        playerData['x'],playerData['y']=float((CHUNK_SIZE-1)//2),float((CHUNK_SIZE-1)//2)
        roomGenerationOrigin=[0,0]
        for generation in range(LEVEL_DEPTH):
            roomGenerationDirection=[0,1,2,3]
            if roomGenerationOrigin[0]+1<levelChunkSize[0] and levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]!=None:
                roomGenerationDirection.remove(0)
            if roomGenerationOrigin[0]-1>=0 and levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]!=None:
                roomGenerationDirection.remove(1)
            if roomGenerationOrigin[1]+1<levelChunkSize[1] and levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]!=None:
                roomGenerationDirection.remove(2)
            if roomGenerationOrigin[1]-1>=0 and levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]!=None:
                roomGenerationDirection.remove(3)
            roomGenerationDirection=sample(roomGenerationDirection,min(choices((1,2,3),cum_weights=(3,5,6))[0],len(roomGenerationDirection)))
            if 0 in roomGenerationDirection:
                if roomGenerationOrigin[0]+1>=levelChunkSize[0]:
                    levelChunkData.append(construct1dList(levelChunkSize[1],None))
                    levelChunkSize=(len(levelChunkData),len(levelChunkData[0]))
                    for _ in range(CHUNK_SIZE):
                        levelLayout.append(construct1dList(levelSize[1],'.'))
                    levelSize=(len(levelLayout),len(levelLayout[0]))
                if levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]==None:
                    if generation==LEVEL_DEPTH-1 and roomGenerationDirection[0]==0:
                        levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]={'type':'portal'}
                        mergingRoomLayout=readLayout('portal')
                    else:
                        levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]={'type':choices(('battle','treasure'),cum_weights=(2,3))[0]}
                        mergingRoomLayout=readLayout(levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['type']+str(randrange(ROOM_VARIANTS[levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['type']])))
                    mergingRoomSize=(len(mergingRoomLayout),len(mergingRoomLayout[0]))
                    levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['x']=(roomGenerationOrigin[0]+1)*CHUNK_SIZE+(CHUNK_SIZE-mergingRoomSize[0])//2
                    levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['y']= roomGenerationOrigin[1]   *CHUNK_SIZE+(CHUNK_SIZE-mergingRoomSize[1])//2
                    levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['width'],levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['height']=mergingRoomSize
                    if levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['type']=='battle':
                        levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['waves']=randint(1,3)
                    for blockX in range(levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['width']):
                        for blockY in range(levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['height']):
                            levelLayout[levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['x']+blockX][levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['y']+blockY]=mergingRoomLayout[blockX][blockY]
                    for delta in range(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['x']+levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['width'],levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['x']):
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+2]='#'
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+1]='_'
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2  ]='_'
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2-1]='_'
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2-2]='#'
                    for delta in (-1,0,1):
                        levelLayout[levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['x']+levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['width']-1][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+delta]='-'
                        levelLayout[levelChunkData[roomGenerationOrigin[0]+1][roomGenerationOrigin[1]]['x']][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+delta]='-'
            if 1 in roomGenerationDirection:
                if roomGenerationOrigin[0]-1<0:
                    levelChunkData.insert(0,construct1dList(levelChunkSize[1],None))
                    levelChunkSize=(len(levelChunkData),len(levelChunkData[0]))
                    roomGenerationOrigin[0]+=1
                    for _ in range(CHUNK_SIZE):
                        levelLayout.insert(0,construct1dList(levelSize[1],'.'))
                    levelSize=(len(levelLayout),len(levelLayout[0]))
                    for array in levelChunkData:
                        for data in array:
                            if data==None:
                                continue
                            data['x']+=CHUNK_SIZE
                    playerData['x']+=CHUNK_SIZE
                if levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]==None:
                    if generation==LEVEL_DEPTH-1 and roomGenerationDirection[0]==1:
                        levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]={'type':'portal'}
                        mergingRoomLayout=readLayout('portal')
                    else:
                        levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]={'type':choices(('battle','treasure'),cum_weights=(2,3))[0]}
                        mergingRoomLayout=readLayout(levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['type']+str(randrange(ROOM_VARIANTS[levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['type']])))
                    mergingRoomSize=(len(mergingRoomLayout),len(mergingRoomLayout[0]))
                    levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['x']=(roomGenerationOrigin[0]-1)*CHUNK_SIZE+(CHUNK_SIZE-mergingRoomSize[0])//2
                    levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['y']= roomGenerationOrigin[1]   *CHUNK_SIZE+(CHUNK_SIZE-mergingRoomSize[1])//2
                    levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['width'],levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['height']=mergingRoomSize
                    if levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['type']=='battle':
                        levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['waves']=randint(1,3)
                    for blockX in range(levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['width']):
                        for blockY in range(levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['height']):
                            levelLayout[levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['x']+blockX][levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['y']+blockY]=mergingRoomLayout[blockX][blockY]
                    for delta in range(levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['x']+levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['width'],levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['x']):
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+2]='#'
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+1]='_'
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2  ]='_'
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2-1]='_'
                        levelLayout[delta][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2-2]='#'
                    for delta in (-1,0,1):
                        levelLayout[levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['x']+levelChunkData[roomGenerationOrigin[0]-1][roomGenerationOrigin[1]]['width']-1][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+delta]='-'
                        levelLayout[levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['x']][roomGenerationOrigin[1]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+delta]='-'
            if 2 in roomGenerationDirection:
                if roomGenerationOrigin[1]+1>=levelChunkSize[1]:
                    for index in range(levelChunkSize[0]):
                        levelChunkData[index].append(None)
                    levelChunkSize=(len(levelChunkData),len(levelChunkData[0]))
                    for index in range(levelSize[0]):
                        for _ in range(CHUNK_SIZE):
                            levelLayout[index].append('.')
                    levelSize=(len(levelLayout),len(levelLayout[0]))
                if levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]==None:
                    if generation==LEVEL_DEPTH-1 and roomGenerationDirection[0]==2:
                        levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]={'type':'portal'}
                        mergingRoomLayout=readLayout('portal')
                    else:
                        levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]={'type':choices(('battle','treasure'),cum_weights=(2,3))[0]}
                        mergingRoomLayout=readLayout(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['type']+str(randrange(ROOM_VARIANTS[levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['type']])))
                    mergingRoomSize=(len(mergingRoomLayout),len(mergingRoomLayout[0]))
                    levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['x']=(CHUNK_SIZE-mergingRoomSize[0])//2+ roomGenerationOrigin[0]   *CHUNK_SIZE
                    levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['y']=(CHUNK_SIZE-mergingRoomSize[1])//2+(roomGenerationOrigin[1]+1)*CHUNK_SIZE
                    levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['width'],levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['height']=mergingRoomSize
                    if levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['type']=='battle':
                        levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['waves']=randint(1,3)
                    for blockX in range(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['width']):
                        for blockY in range(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['height']):
                            levelLayout[levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['x']+blockX][levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['y']+blockY]=mergingRoomLayout[blockX][blockY]
                    for delta in range(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['y']+levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['height'],levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['y']):
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+2][delta]='#'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+1][delta]='_'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2  ][delta]='_'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2-1][delta]='_'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2-2][delta]='#'
                    for delta in (-1,0,1):
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+delta][levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['y']+levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['height']-1]='-'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+delta][levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]+1]['y']]='-'
            if 3 in roomGenerationDirection:
                if roomGenerationOrigin[1]-1<0:
                    for index in range(levelChunkSize[0]):
                        levelChunkData[index].insert(0,None)
                    levelChunkSize=(len(levelChunkData),len(levelChunkData[0]))
                    roomGenerationOrigin[1]+=1
                    for index in range(levelSize[0]):
                        for _ in range(CHUNK_SIZE):
                            levelLayout[index].insert(0,'.')
                    levelSize=(len(levelLayout),len(levelLayout[0]))
                    for array in levelChunkData:
                        for data in array:
                            if data==None:
                                continue
                            data['y']+=CHUNK_SIZE
                    playerData['y']+=CHUNK_SIZE
                if levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]==None:
                    if generation==LEVEL_DEPTH-1 and roomGenerationDirection[0]==3:
                        levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]={'type':'portal'}
                        mergingRoomLayout=readLayout('portal')
                    else:
                        levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]={'type':choices(('battle','treasure'),cum_weights=(2,3))[0]}
                        mergingRoomLayout=readLayout(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['type']+str(randrange(ROOM_VARIANTS[levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['type']])))
                    mergingRoomSize=(len(mergingRoomLayout),len(mergingRoomLayout[0]))
                    levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['x']=(CHUNK_SIZE-mergingRoomSize[0])//2+ roomGenerationOrigin[0]   *CHUNK_SIZE
                    levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['y']=(CHUNK_SIZE-mergingRoomSize[1])//2+(roomGenerationOrigin[1]-1)*CHUNK_SIZE
                    levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['width'],levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['height']=mergingRoomSize
                    if levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['type']=='battle':
                        levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['waves']=randint(1,3)
                    for blockX in range(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['width']):
                        for blockY in range(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['height']):
                            levelLayout[levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['x']+blockX][levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['y']+blockY]=mergingRoomLayout[blockX][blockY]
                    for delta in range(levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['y']+levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['height'],levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['y']):
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+2][delta]='#'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+1][delta]='_'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2  ][delta]='_'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2-1][delta]='_'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2-2][delta]='#'
                    for delta in (-1,0,1):
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+delta][levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['y']+levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]-1]['height']-1]='-'
                        levelLayout[roomGenerationOrigin[0]*CHUNK_SIZE+(CHUNK_SIZE-1)//2+delta][levelChunkData[roomGenerationOrigin[0]][roomGenerationOrigin[1]]['y']]='-'
            if   roomGenerationDirection[0]==0:
                roomGenerationOrigin[0]+=1
            elif roomGenerationDirection[0]==1:
                roomGenerationOrigin[0]-=1
            elif roomGenerationDirection[0]==2:
                roomGenerationOrigin[1]+=1
            elif roomGenerationDirection[0]==3:
                roomGenerationOrigin[1]-=1
        treasureLocation.clear()
        for blockX in range(levelSize[0]):
            for blockY in range(levelSize[1]):
                if   levelLayout[blockX][blockY]=='$':
                    treasureLocation.append((blockX,blockY))
                elif levelLayout[blockX][blockY]=='@':
                    portalLocation=(blockX,blockY)
        textureVariationSelection.clear()
        for _ in range(levelSize[0]*levelSize[1]):
            textureVariationSelection.append(randrange(100))
        if playerData['hp']>0:
            diffculty+=1
            score+=30
            playerData['hp']=min(playerData['hp']+playerData['hp_max']*0.3,playerData['hp_max'])
        else:
            diffculty=0
            score=0
            playerData['hp']=playerData['hp_max']
        playerData['shield']=playerData['shield_max']
        playerData['spd']=8.0
        playerData['atk_cd']=0
        playerData['shield_regen_cd']=0
        playerData['red_cd']=0
        inBattle=False
        spawnableTile.clear()
        entityData.clear()
        generateNewLevel=False
    keyPressed=pg.key.get_pressed()
    for event in pg.event.get():#detect QUIT event & toggle fps display
        if event.type==QUIT or keyPressed[K_ESCAPE]:
            active=False
            break
        if event.type==KEYDOWN and event.key==K_f:
            SHOW_FPS=not SHOW_FPS
    else:
        if (distance(playerData['x'],playerData['y'],portalLocation[0],portalLocation[1])<=0.5 or playerData['hp']<=0) and blackScreenTransition==TICKRATE:
            blackScreenTransition=-TICKRATE
        if blackScreenTransition!=TICKRATE:
            blackScreenTransition+=1
        if blackScreenTransition==0:
            generateNewLevel=True
        for index in range(len(treasureLocation)):#loot treasure
            if treasureLocation[index]==None:
                continue
            if distance(treasureLocation[index][0],treasureLocation[index][1],playerData['x'],playerData['y'])<=0.5:
                levelLayout[treasureLocation[index][0]][treasureLocation[index][1]]='S'
                treasureLocation[index]=None
                score+=5+diffculty
                if playerData['atk_sep']==3:
                    treasureLoot.remove('atk_sep')
                treasureLoot=choices(treasureLoot,k=randint(1,1+diffculty//2))
                if 'hp' in treasureLoot:
                    if playerData['hp']==playerData['hp_max']:
                        playerData['hp']+=(diffculty+1)*2
                        playerData['hp_max']+=(diffculty+1)*2
                    else:
                        playerData['hp']=min(playerData['hp']+floor(0.2*playerData['hp_max']),playerData['hp_max'])
                if 'shield' in treasureLoot:
                    playerData['shield']+=1+diffculty
                    playerData['shield_max']+=1+diffculty
                if 'atk' in treasureLoot:
                    playerData['atk']+=1+diffculty
                if 'atk_sep' in treasureLoot:
                    playerData['atk_sep']-=3
                if 'def' in treasureLoot:
                    playerData['def']+=1
                if 'score' in treasureLoot:
                    score+=5*diffculty
                treasureLoot=['hp','shield','atk','atk_sep','def','score']
        if levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['type']=='battle' and playerData['x']>=levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['x']+1 and playerData['x']+1<=levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['x']+levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['width']-1 and playerData['y']>=levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['y']+1 and playerData['y']+1<=levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['y']+levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['height']-1 and levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['waves']>0:#start battle
            inBattle=True
            playerData['spd']=4.0
            for blockX in range(levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['x'],levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['x']+levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['width']):
                for blockY in range(levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['y'],levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['y']+levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['height']):
                    if levelLayout[blockX][blockY]=='-':
                        levelLayout[blockX][blockY]='+'
                    if levelLayout[blockX][blockY]=='_':
                        spawnableTile.append((blockX,blockY))
        if inBattle:#spawn wave & end battle
            for data in entityData:
                if data['type'] in ('foe_spawnpoint','melee_foe','gunner_foe'):
                    if data['type']=='foe_spawnpoint' or data['phase']!='dead':
                        break
            else:
                if levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['waves']>0:
                    levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['waves']-=1
                    for location in choices(spawnableTile,k=min(3+diffculty,len(spawnableTile))):
                        entityData.append({'type':'foe_spawnpoint','x':location[0],'y':location[1],'cd':60,'data':choice(({'type':'melee_foe','hp':10+3*diffculty,'atk':3+diffculty,'atk_sep':30,'def':diffculty//3,'spd':min(5.0+0.5*diffculty,10.0),'range':10.0+diffculty,'idle_dur':max(90-6*diffculty,30),'attack_dur':min(120+6*diffculty,300),'attack_charge':30},{'type':'gunner_foe','hp':8+2*diffculty,'atk':2+diffculty//2,'atk_sep':max(60-6*diffculty,6),'def':diffculty//4,'spd':min(2.0+0.1*diffculty,5.0),'range':10.0+1.5*diffculty,'idle_dur':max(120-12*diffculty,30),'attack_dur':min(60+6*diffculty,120),'wander_cd':0,'shots':1+diffculty//5,'bullet_spd':7.0+0.3*diffculty,'bullet_reflect':diffculty//7,'texture':'blue'},{'type':'gunner_foe','hp':6+floor(1.5*diffculty),'atk':1+diffculty//3,'atk_sep':max(90-6*diffculty,12),'def':diffculty//4,'spd':min(1.5+0.1*diffculty,4.0),'range':7.0+1.0*diffculty,'idle_dur':max(180-12*diffculty,60),'attack_dur':min(30+6*diffculty,90),'wander_cd':0,'shots':min(3+2*(diffculty//5),12),'bullet_spd':6.0+0.2*diffculty,'bullet_reflect':diffculty//7,'texture':'green'},{'type':'gunner_foe','hp':7+1*diffculty,'atk':3+floor(diffculty*1.5),'atk_sep':max(90-6*diffculty,30),'def':diffculty//4,'spd':min(2.0+0.1*diffculty,4.0),'range':12.0+2.0*diffculty,'idle_dur':max(210-12*diffculty,90),'attack_dur':min(30+12*diffculty,150),'wander_cd':0,'shots':1,'bullet_spd':9.0+0.5*diffculty,'bullet_reflect':1+diffculty//4,'texture':'yellow'})),'disabled':False})
                else:
                    inBattle=False
                    playerData['spd']=8.0
                    spawnableTile.clear()
                    for blockX in range(levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['x'],levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['x']+levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['width']):
                        for blockY in range(levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['y'],levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['y']+levelChunkData[floor(playerData['x']/CHUNK_SIZE)][floor(playerData['y']/CHUNK_SIZE)]['height']):
                            if levelLayout[blockX][blockY]=='+':
                                levelLayout[blockX][blockY]='-'
        if blackScreenTransition==TICKRATE:#player behavior
            if   keyPressed[K_d] and not keyPressed[K_a] and keyPressed[K_s]==keyPressed[K_w]:
                playerData['x']+=playerData['spd']/movementTickrate
            elif keyPressed[K_a] and not keyPressed[K_d] and keyPressed[K_s]==keyPressed[K_w]:
                playerData['x']-=playerData['spd']/movementTickrate
            elif keyPressed[K_s] and not keyPressed[K_w] and keyPressed[K_d]==keyPressed[K_a]:
                playerData['y']+=playerData['spd']/movementTickrate
            elif keyPressed[K_w] and not keyPressed[K_s] and keyPressed[K_d]==keyPressed[K_a]:
                playerData['y']-=playerData['spd']/movementTickrate
            elif keyPressed[K_d] and keyPressed[K_s] and not keyPressed[K_a] and not keyPressed[K_w]:
                playerData['x']+=playerData['spd']*0.707106781186547/movementTickrate
                playerData['y']+=playerData['spd']*0.707106781186547/movementTickrate
            elif keyPressed[K_a] and keyPressed[K_s] and not keyPressed[K_d] and not keyPressed[K_w]:
                playerData['x']-=playerData['spd']*0.707106781186547/movementTickrate
                playerData['y']+=playerData['spd']*0.707106781186547/movementTickrate
            elif keyPressed[K_a] and keyPressed[K_w] and not keyPressed[K_d] and not keyPressed[K_s]:
                playerData['x']-=playerData['spd']*0.707106781186547/movementTickrate
                playerData['y']-=playerData['spd']*0.707106781186547/movementTickrate
            elif keyPressed[K_d] and keyPressed[K_w] and not keyPressed[K_a] and not keyPressed[K_s]:
                playerData['x']+=playerData['spd']*0.707106781186547/movementTickrate
                playerData['y']-=playerData['spd']*0.707106781186547/movementTickrate
            playerData['x'],playerData['y']=blockingAdjust(playerData['x'],playerData['y'])
            cursorPosition=pg.mouse.get_pos()
            mouseLeftButtonPressed=pg.mouse.get_pressed()[0]
            if playerData['shield_regen_cd']==0:
                if playerData['shield']<playerData['shield_max']:
                    playerData['shield']+=1
                    playerData['shield_regen_cd']=60
            else:
                playerData['shield_regen_cd']-=1
            if playerData['atk_cd']==0:
                if mouseLeftButtonPressed:
                    entityData.append({'type':'player_bullet','dmg':playerData['atk'],'spd':7.5,'reflect':0,'range':100,'disabled':False})
                    entityData[-1]['dx'],entityData[-1]['dy']=generateDelta(screen.get_width()//2,screen.get_height()//2,cursorPosition[0],cursorPosition[1])
                    entityData[-1]['x']=playerData['x']+entityData[-1]['dx']/2+0.375
                    entityData[-1]['y']=playerData['y']+entityData[-1]['dy']/2+0.375
                    playerData['atk_cd']=playerData['atk_sep']
            else:
                playerData['atk_cd']-=1
            if playerData['red_cd']!=0:
                playerData['red_cd']-=1
        for data in entityData:#entities behavior
            if   data['type']=='foe_spawnpoint':
                if data['disabled']:
                    continue
                if data['cd']==0:
                    data['data']['x'],data['data']['y']=data['x'],data['y']
                    data['data']['dx'],data['data']['dy'],data['data']['phase'],data['data']['atk_cd'],data['data']['phase_cd']=0.0,0.0,'idle',0,0
                    entityData.append(data['data'])
                    data['disabled']=True
                else:
                    data['cd']-=1
            elif data['type']=='melee_foe':
                if data['phase']=='dead':
                    continue
                if data['hp']<=0:
                    data['phase']='dead'
                    score+=1+diffculty
                    continue
                if data['phase']=='idle' and data['phase_cd']==0 and entityVisible(data['x'],data['y'],playerData['x'],playerData['y'],data['range']):
                    data['phase']='attack'
                    data['phase_cd']=data['attack_dur']
                    data['dx'],data['dy']=generateDelta(data['x'],data['y'],playerData['x'],playerData['y'])
                if data['phase']=='attack' and data['phase_cd']==0:
                    data['phase']='idle'
                    data['phase_cd']=data['idle_dur']
                if data['phase']=='attack' and data['phase_cd']<=data['attack_dur']-data['attack_charge']:
                    data['x']+=data['dx']*data['spd']/movementTickrate
                    data['y']+=data['dy']*data['spd']/movementTickrate
                    data['dx'],data['dy']=reflectingAdjust(data['x'],data['y'],data['dx'],data['dy'])
                if data['atk_cd']==0 and distance(playerData['x'],playerData['y'],data['x'],data['y'])<=0.5:
                    data['atk_cd']=data['atk_sep']
                    damagePlayer(data['atk'])
                if data['phase_cd']!=0:
                    data['phase_cd']-=1
                if data['atk_cd']!=0:
                    data['atk_cd']-=1
                data['x'],data['y']=blockingAdjust(data['x'],data['y'])
            elif data['type']=='gunner_foe':
                if data['phase']=='dead':
                    continue
                if data['hp']<=0:
                    data['phase']='dead'
                    score+=1+diffculty
                    continue
                if data['phase']=='idle' and data['phase_cd']==0 and entityVisible(data['x'],data['y'],playerData['x'],playerData['y'],data['range']):
                    data['phase']='attack'
                    data['phase_cd']=data['attack_dur']
                if data['phase']=='attack' and data['phase_cd']==0:
                    data['phase']='idle'
                    data['phase_cd']=data['idle_dur']
                if data['atk_cd']==0:
                    if data['phase']=='attack':
                        for index in range(data['shots']):
                            entityData.append({'type':'foe_bullet','dmg':data['atk'],'spd':data['bullet_spd'],'reflect':data['bullet_reflect'],'range':data['range']*2,'texture':data['texture'],'disabled':False})
                            entityData[-1]['dx'],entityData[-1]['dy']=rotateDelta(generateDelta(data['x'],data['y'],playerData['x'],playerData['y']),30*index-15*(data['shots']-1))
                            entityData[-1]['x']=data['x']+entityData[-1]['dx']/2+0.375
                            entityData[-1]['y']=data['y']+entityData[-1]['dy']/2+0.375
                        data['atk_cd']=data['atk_sep']
                else:
                    data['atk_cd']-=1
                if data['wander_cd']==0:
                    data['wander_cd']=randint(45,75)
                    if entityVisible(data['x'],data['y'],playerData['x'],playerData['y'],data['range']):
                        data['dx'],data['dy']=wander(data['x'],data['y'],playerData['x']+(data['x']-playerData['x'])/distance(data['x'],data['y'],playerData['x'],playerData['y'])*data['range']*0.5,playerData['y']+(data['y']-playerData['y'])/distance(data['x'],data['y'],playerData['x'],playerData['y'])*data['range']*0.5)
                    else:
                        data['dx'],data['dy']=wander(data['x'],data['y'],data['x'],data['y'])
                else:
                    data['wander_cd']-=1
                if data['phase_cd']!=0:
                    data['phase_cd']-=1
                data['x']+=data['dx']*data['spd']/movementTickrate
                data['y']+=data['dy']*data['spd']/movementTickrate
                data['dx'],data['dy']=reflectingAdjust(data['x'],data['y'],data['dx'],data['dy'])
                data['x'] ,data['y'] =blockingAdjust  (data['x'],data['y'])
            elif data['type'] in ('player_bullet','foe_bullet'):
                if data['disabled']:
                    continue
                if data['x']<0 or data['x']>levelSize[0]+1 or data['y']<0 or data['y']>levelSize[1]+1:
                    data['disabled']=True
                    continue
                if True in getHitbox(data['x'],data['y'],0.25):
                    if data['reflect']!=0:
                        data['reflect']-=1
                        data['dx'],data['dy']=reflectingAdjust(data['x'],data['y'],data['dx'],data['dy'])
                    else:
                        data['disabled']=True
                if data['type']=='player_bullet':
                    for data_ in entityData:
                        if data_['type'] in ('foe_spawnpoint','player_bullet','foe_bullet'):
                            continue
                        if distance(data['x']+0.125,data['y']+0.125,data_['x']+0.5,data_['y']+0.5)<=0.5 and data_['phase']!='dead':
                            data_['hp']-=max(data['dmg']-data_['def'],1)
                            data['disabled']=True
                elif distance(data['x']+0.125,data['y']+0.125,playerData['x']+0.5,playerData['y']+0.5)<=0.5:
                    damagePlayer(data['dmg'])
                    data['disabled']=True
                data['x']+=data['dx']*data['spd']/movementTickrate
                data['y']+=data['dy']*data['spd']/movementTickrate
                data['range']-=1
        for index in range(len(entityData)):
            if 'disabled' in entityData[index].keys() and entityData[index]['disabled']:
                entityData[index]=None
        while None in entityData:
            entityData.remove(None)
        screen.fill((255,255,255))
        for blockX in range(levelSize[0]):#render tiles
            for blockY in range(levelSize[1]):
                if levelLayout[blockX][blockY]=='.':
                    continue
                elif levelLayout[blockX][blockY] not in TILE_TEXTURE_ID.keys():
                    render('unknown',blockX,blockY)
                elif TILE_TEXTURE_ID[levelLayout[blockX][blockY]] not in TEXTURE_VARIANTS.keys():
                    render(TILE_TEXTURE_ID[levelLayout[blockX][blockY]],blockX,blockY)
                elif type(TEXTURE_VARIANTS[TILE_TEXTURE_ID[levelLayout[blockX][blockY]]])==int:
                    render(TILE_TEXTURE_ID[levelLayout[blockX][blockY]]+str(animationTick//(60//TEXTURE_VARIANTS[TILE_TEXTURE_ID[levelLayout[blockX][blockY]]])),blockX,blockY)
                else:
                    render(TILE_TEXTURE_ID[levelLayout[blockX][blockY]]+str(TEXTURE_VARIANTS[TILE_TEXTURE_ID[levelLayout[blockX][blockY]]][textureVariationSelection[blockX+blockY*levelSize[0]]%len(TEXTURE_VARIANTS[TILE_TEXTURE_ID[levelLayout[blockX][blockY]]])]),blockX,blockY)
        for data in entityData:#render entities
            if   data['type']=='foe_spawnpoint':
                render('foe_spawnpoint',data['x'],data['y'])
            elif data['type']=='melee_foe':
                if   data['phase']=='dead':
                    render('melee_foe_dead'  ,data['x'],data['y'],data['dx']<0)
                elif data['phase']=='attack':
                    render('melee_foe_attack',data['x'],data['y'],data['dx']<0)
                else:
                    render('melee_foe_idle'  ,data['x'],data['y'],data['dx']<0)
            elif data['type']=='gunner_foe':
                if data['phase']=='dead':
                    render('gunner_foe_'+data['texture']+'_dead',data['x'],data['y'],data['dx']<0)
                else:
                    render('gunner_foe_'+data['texture']+str(animationTick//(60//TEXTURE_VARIANTS['gunner_foe_'+data['texture']])),data['x'],data['y'],data['dx']<0)
            elif data['type']=='foe_bullet':
                render('foe_bullet_'+data['texture'],data['x'],data['y'])
            elif data['type']=='player_bullet':
                render('player_bullet',data['x'],data['y'])
        if playerData['hp']<=0:
            render('player_dead',playerData['x'],playerData['y'],cursorPosition[0]<screen.get_width()//2 and blackScreenTransition==TICKRATE)
        else:
            render('player'+'_attack'*int(playerData['atk_cd']!=0)+'_red'*int(playerData['red_cd']!=0),playerData['x'],playerData['y'],cursorPosition[0]<screen.get_width()//2 and blackScreenTransition==TICKRATE)
        screen.blit(TEXTURE['status_interface'],(0,0))
        pg.draw.rect(screen,(194,40 ,74 ),pg.Rect(56,16,ceil(180*playerData['hp']    /playerData['hp_max'])    ,16))
        pg.draw.rect(screen,(112,129,130),pg.Rect(56,52,ceil(180*playerData['shield']/playerData['shield_max']),16))
        screen.blit(FONT.render(str(score),False,(222,174,89)),(104,88))
        if blackScreenTransition!=TICKRATE:#black Screen Transition
            pg.draw.rect(screen,(0,0,0),pg.Rect(0,0,screen.get_width(),round((TICKRATE-abs(blackScreenTransition))*(screen.get_height()/TICKRATE/2))))
            pg.draw.rect(screen,(0,0,0),pg.Rect(0,screen.get_height()//2+round(abs(blackScreenTransition)*(screen.get_height()/TICKRATE/2)),screen.get_width(),round((TICKRATE-abs(blackScreenTransition))*(screen.get_height()/TICKRATE/2))))
            pg.draw.rect(screen,(0,0,0),pg.Rect(0,0,round((TICKRATE-abs(blackScreenTransition))*(screen.get_width()/TICKRATE/2)),screen.get_height()))
            pg.draw.rect(screen,(0,0,0),pg.Rect(screen.get_width()//2+round(abs(blackScreenTransition)*(screen.get_width()/TICKRATE/2)),0,round((TICKRATE-abs(blackScreenTransition))*(screen.get_width()/TICKRATE/2)),screen.get_height()))
        if SHOW_FPS:
            screen.blit(FONT.render(str(round(fps)),False,(0,0,0)),(screen.get_width()-FONT.size(str(round(fps)))[0],3))
        pg.display.flip()
        clock.tick(TICKRATE)
        fps=clock.get_fps()
        if MOVEMENT_TICKRATE_ADJUSTS_BY_FPS:
            movementTickrate=max(fps,1)
        animationTick+=1
        if animationTick==60:
            animationTick=0
pg.quit()