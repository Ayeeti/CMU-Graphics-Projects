from cmu_graphics import *
import random, math

def onAppStart(app):
    app.width = 600
    app.height = 600
    app.buildingCount = 10
    app.playerRadius = 15
    app.holeRadius = 25
    app.stepsPerSecond = 20
    startNewGame(app)
    app.titleScreen = True
    
def startNewGame(app):
    app.steps = 0
    app.nightMode = False 
    app.showStars = False
    app.starCx, app.starCy = 0,0
    app.starPositions = []
    changeStarPositions(app)
        
    app.showBlimp = True
    app.blimpWidth = 80
    app.blimpHeight = 40
    app.blimpCx = 0
    app.blimpCy = 230
    app.buildingHeights = [random.randrange(50, 250) for _ in range(app.buildingCount)]
    colors = ['gainsboro', 'lightGray', 'silver','darkGray', 'gray', 'dimGray']
    app.buildingColors = [random.choice(colors) for _ in range(app.buildingCount)]
    
    #place players
    app.buildingWidth = (app.width/app.buildingCount)
    app.windowWidth = math.floor(app.buildingWidth * (3/4))
    app.windowHeight = 20
    app.spaceBetweenWindows = 30
    cx0 = app.buildingWidth/2
    cy0 = app.height - app.buildingHeights[0] - app.playerRadius
    cx1 = app.width - app.buildingWidth/2
    cy1 = app.height - app.buildingHeights[-1] - app.playerRadius
    app.player = [(cx0, cy0, 'blue'), (cx1, cy1, 'pink')]
    app.currentPlayer = 0
    app.showBlot = False
    app.holes = []
    app.gameOver = False
    
def onKeyPress(app, key):
    if app.titleScreen and key == 's':
        app.titleScreen = False
    if not app.gameOver and not app.titleScreen:
        if key == 'c':
            app.nightMode = not app.nightMode
    if key =='n':
            startNewGame(app)


def onMousePress(app, mouseX, mouseY):
    
    if not app.gameOver and not app.titleScreen:
        if app.showBlot:
            return
        dy = 3 + (app.height - mouseY) * 25 /app.height
        dx = 3 + (mouseX) * 25 / app.width
        
        if app.currentPlayer == 0:
            app.dx, app.dy = dx, -dy  
        else:
            dx = 3 + (app.width - mouseX) * 25 / app.width
            app.dx, app.dy = -dx, -dy
        app.showBlot = True
        app.blotCx, app.blotCy, app.blotColor = app.player[app.currentPlayer]

def onStep(app):
    if not app.gameOver and not app.titleScreen:
        app.steps += 1
        
        #show stars
        if (app.steps % 80) == 0:
            app.starPositions = []
            changeStarPositions(app)
            app.showStars = True
        elif (app.steps % 100) == 0:
            app.showStars = False
            
        #move blimp
        if (app.steps % 5) == 0:
            app.blimpCx += 20
            if app.blimpCx == app.width:
                app.blimpCx = 0
       
        if app.showBlot:
            app.blotCx += app.dx
            app.blotCy += app.dy
            app.dy += 0.7 #for gravity
            #check if off board
            if ((app.blotCy < 0) or (app.blotCx > app.width) or
                 (app.blotCx < 0)):
                     app.showBlot = False
                     app.currentPlayer = 1 - app.currentPlayer
            else:
                #check if hit a other player
                cx0, cy0, color = app.player[(1-app.currentPlayer)]
                if distance(cx0, cy0, app.blotCx, app.blotCy) <= app.playerRadius:
                    app.gameOver = True
                    
                #check if hit blimp
                if ((app.blimpCx - app.blimpWidth/2 <= app.blotCx + app.playerRadius <= app.blimpCx + app.blimpWidth/2) and 
                   (app.blimpCy - app.blimpHeight/2 < app.blotCy + app.playerRadius < app.blimpCy + app.blimpHeight/2)):
                       app.gameOver = True
                
                # check if hit building
                for i in range(app.buildingCount):
                    left, top, width, height = getBuildingBounds(app,i)
                    #check if hit hole
                    for cx, cy, in app.holes:
                        if distance(cx, cy, app.blotCx, app.blotCy) <= 2*app.playerRadius:
                            return
                    if ((left <= app.blotCx <= left + width) and
                         (top <= app.blotCy <= top + height)):
                             app.showBlot = False
                             #we just hit a building
                             app.holes.append((app.blotCx, app.blotCy))
                             app.currentPlayer = 1 - app.currentPlayer

def redrawAll(app):
    
    if app.titleScreen:
        drawRect(0,0, app.width, app.height, fill = 'white')
        drawLabel('Welcomine to Blob Shooter in the City!', app.width/2, app.height/4, size = 30)
        drawLabel('This is a two player game where each player is trying to hit the other with their blob.',app.width/2, app.height/4 + 50,  size = 15, align = 'center')
        drawLabel('Click on screen to shoot and depending on your mouse position, your blot with have a', app.width/2, app.height/4 + 70,  size = 15, align = 'center')
        drawLabel('certain upward and downward speed. The further up the app you click the more upward', app.width/2, app.height/4 + 90,  size = 15, align = 'center')
        drawLabel('speed you have and vice versa. You can press c to turn on and off night mode.', app.width/2, app.height/4 + 110,  size = 15, align = 'center')
        drawLabel('Be sure to avoid the blimp because hitting causes that player to lose instantly.', app.width/2, app.height/4 + 130,  size = 15, align = 'center')
        drawLabel('Press s to start playing!', app.width/2, app.height/2 + 50, fill = 'red' ,size = 30, align = 'center')
        
    else:
        if not app.nightMode:
            backgroundColor = 'papayaWhip'
        else:
            backgroundColor = 'midnightBlue'
        drawRect(0,0, app.width, app.height, fill = backgroundColor)    
        
         #drawStars
        if app.showStars and app.nightMode:
            for starCx, starCy in app.starPositions:
                drawStar(starCx, starCy, 20, 5, fill = 'gold')
    
        drawLabel(f'BlotShooter in Blot City!', app.width/2, 20, fill = 'lightgreen', size = 20, bold = True)
        
        #draw blimp    
        if app.showBlimp:
            drawRect(app.blimpCx, app.blimpCy, 20, 20, align = 'right')
            drawOval(app.blimpCx, app.blimpCy - 20, app.blimpWidth, app.blimpHeight,align = 'center', fill = 'violet')
        
        #draw buildings
        for i in range(app.buildingCount):
            windowCx = 0
            windowCy = 0
            height = app.buildingHeights[i]
            color = app.buildingColors[i]
            left, top, width, height = getBuildingBounds(app,i)
            drawRect(left, top, width, height, fill = color, border = 'black', borderWidth = 2)
            
            #draw windows
            for i in range(10):
                windowCx = left + app.buildingWidth/2
                windowCy = top + (app.spaceBetweenWindows * (i+ 1))
                if (windowCy + app.windowHeight) > app.height:
                    break
                else:
                    drawRect(windowCx, windowCy, app.windowWidth, app.windowHeight, fill = 'yellow', align = 'center')
                    drawLine(windowCx, windowCy - app.windowHeight/2, windowCx, windowCy + app.windowHeight/2)
                    drawLine(windowCx - app.windowWidth/2, windowCy , windowCx + app.windowWidth/2, windowCy )
       
        #draw hole
        for cx, cy, in app.holes:
            drawCircle(cx, cy, app.holeRadius, fill = backgroundColor)
        
        #drawBlot
        if app.showBlot:
            drawCircle(app.blotCx, app.blotCy, app.playerRadius, fill = app.blotColor)
        
        #draw players
        for player in range(len(app.player)):
            cx, cy, color = app.player[player]
            drawCircle(cx, cy, app.playerRadius, fill = color)
        #draw players turn
        drawLabel(f'Current Player: {app.currentPlayer}', app.width/2, 50, fill = 'lightgreen', size = 20)
        
        if app.gameOver:
            drawLabel('Game Over', app.width/2, 150, fill = 'lightgreen', size = 50)
            drawLabel(f'Player {1- app.currentPlayer} Wins!', app.width/2, 200, fill = 'lightgreen', size = 30)
            
    
def changeStarPositions(app):
    for _ in range(10):
        app.starCx, app.starCy = random.randrange(10, app.width), random.randrange(70, 300)
        app.starPositions.append((app.starCx, app.starCy))
    

def getBuildingBounds(app, i):
    width = app.width/app.buildingCount
    height = app.buildingHeights[i]
    left = i * width
    top = app.height - height
    return left, top, width, height
    
def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5
    
    
def main():
    runApp()
main()




