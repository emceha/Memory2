import random

monsters = []
m2check = set()

warmup = True
gameover = False

hold = millis()
strt = millis()

def setup():    
    size(600, 600)
    noStroke()
    imageMode(CENTER)
    
    global blank
    blank = loadImage('data/blank.png')
    
    global tile
    tile = loadImage('data/background.jpg')
    tile.resize(600, 600)
    tile.loadPixels()
                
    populateBoard()


def draw():
    global warmup
    background(tile)

    if not gameover:
        if millis() - strt < 8000:
            stroke(230, 20, 20)
            fill(220, 20, 20);
            rect(0, 590, width - frameCount * 1.3, 5)
        else:
            warmup = False
        checkForPair()
  
    for monster in monsters:
        monster.update()

        
def checkForPair():
    global gameover
    if len(m2check) > 1 and (millis() - hold) > 600:
        m1, m2 = m2check.pop(), m2check.pop()
        if m1.face == m2.face:
            m1.found = m2.found = True 
            if all([m.found for m in monsters]):
                gameover = True


def populateBoard():
    for n in range(18):
        face = loadImage("data/%s.png" % n);
        monsters.append(Monster(face))
        monsters.append(Monster(face))

    random.shuffle(monsters)
    
    mx = (width - 6 * blank.width) / 2
    my = (height - 6 * blank.height) / 2
    hh = blank.height / 2
    hw = blank.width / 2

    for p, m in enumerate(monsters):
        m.x = (p % 6) * blank.width +  mx + hw
        m.y = (p // 6) * blank.height + my + hh


def mousePressed():
    global m2check, hold
    if not gameover and not warmup:
        mx, my = mouseX, mouseY
        for m in monsters:
            if m in m2check or m.found:
                continue
            if m.isOver(mx, my):
                if len(m2check) < 2:
                    m2check.add(m)
                    hold = millis()


class Monster():
    def __init__(self, face):
        self.face = face
        self.found = False

    def update(self):
        if self in m2check or gameover:
            cx = random.randint(-1, 1)
            cy = random.randint(-1, 1)
            image(self.face, self.x + cx, self.y + cy)
        elif self.found or warmup:
            image(self.face, self.x, self.y)
        else:
            image(blank, self.x, self.y)

    def isOver(self, mx, my):
        if dist(self.x, self.y, mx, my) < 40:
            return True
        return False
