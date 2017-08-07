add_library("sound")
import random


def setup():
    size(600, 600)
    noStroke()
    imageMode(CENTER)
    
    global ticktock
    ticktock = SoundFile(this,"sounds/tick.ogg")
    
    global gameoversnd
    gameoversnd = SoundFile(this,"sounds/zone.ogg")
    
    global matchsnd
    matchsnd = SoundFile(this,"sounds/lock.ogg")
    
    global nomatchsnd
    nomatchsnd = SoundFile(this,"sounds/nomatch.ogg")
    
    global blank
    blank = loadImage('imgs/blank_a.png')
    
    global tile
    tile = loadImage('imgs/background.jpg')
    
    tile.resize(600, 600)
    tile.loadPixels()
    
    global clicks
    clicks = 0
    
    global hold
    hold = millis()
    
    global lastmon 
    lastmon = Monster(blank)
     
    global gameover
    gameover = False

    global warmup
    warmup = True 
    
    global monsters
    monsters = []
    populateBoard()
    
    global startgame
    startgame = millis()
    
    ticktock.play()

    
def draw():
    global hold, gameover, warmup
    background(tile)
    
    if warmup and millis() - startgame < 8000:
        stroke(230, 20, 20)
        fill(220, 20, 20);
        rect(0, 590, width - frameCount * 1.3, 5)
    else:
        warmup = False
        
    if gameover:
        if millis() - hold > 3500:
            shuffleMonsters()
            hold = millis()
    
    n = 0    
    for m in monsters:
        m.update()
        n += m.show
        if not gameover and n == 36:
            gameover = True
            gameoversnd.play()
        

def cleanClicks():
    for m in monsters:
        m.click = 0


def mousePressed():
    global clicks, hold, lastmon
    
    if not gameover and not warmup and millis() - hold > 600:        
        mx, my = mouseX, mouseY
        
        for m in monsters:
            if m.isOver(mx, my):
                if m.show == 0 and m.click == 0:
                    clicks += 1
                    m.click = clicks
                    if clicks > 1:
                        if m.face == lastmon.face:
                            m.show = 1
                            lastmon.show = 1
                            matchsnd.play()
                        else:
                            nomatchsnd.play() 
                        clicks = 0
                        hold = millis()
                    else:
                        lastmon = m
                break
    
                                    
def mouseWheel(event):
    if gameover:
        shuffleMonsters()
    
    
def shuffleMonsters():
    pos = []
    for m in monsters:
        pos.append((m.x, m.y))
        
    random.shuffle(pos)
    for p, m in enumerate(monsters):
        m.x, m.y = pos[p]
    
    
def populateBoard():
    for n in range(18):
        face = loadImage("imgs/%s.png" % n);
        monsters.append(Monster(face))
        monsters.append(Monster(face))
    
    random.shuffle(monsters)
    
    mx = (width - 6 * blank.width) / 2
    my = (height - 6 * blank.height) / 2
    hh = blank.height / 2
    hw = blank.width / 2
    
    for p, m in enumerate(monsters):
        m.x, m.y = (p % 6) * blank.width +  mx + hw, (p / 6) * blank.height + my + hh 


class Monster(object):
    def __init__(self, face, x = 0, y = 0):
        self.face = face
        self.x = x
        self.y = y
        self.show = 0
        self.click = 0
            
    def update(self):
        if gameover or self.click > 0:
            cx = random.choice([-1, 0, 1])
            cy = random.choice([-1, 0, 1])
            image(self.face, self.x + cx, self.y + cy)
            if self.click > 1: 
                if millis() - hold > 500:
                    cleanClicks()
        
        elif warmup or self.show:    
            image(self.face, self.x, self.y)
        
        else:
            image(blank, self.x, self.y)   
        
    def isOver(self, mx, my):
        if(sqrt(sq(self.x - mx) + sq(self.y - my)) < 40):
            return True
        else:
            return False
        
        