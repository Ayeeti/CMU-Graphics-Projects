from cmu_graphics import *
import copy, string, itertools, random


####################################################
# onAppStart: called only once when app is launched
####################################################

def onAppStart(app):
    app.gameName = 'SUPERSET'
    app.width = 1000
    app.height = 600
    app.rectLeft = 200
    app.rectTop = 170
    app.rectWidth = 120
    app.rectHeight = 180
    app.spaceBetweenRect = 45
    app.cardLabelX = 260
    app.cardLabelY = 260
    app.dims = [3, 3, 3, 3]
    app.targetBoardSize = 8
    app.allThemes = ['Letters', 'Standard', 'Special', 'On the Move']
    app.theme = app.allThemes[0]
    app.stepsPerSecond = 20
    app.playScreenTimeScore = 0
    app.diamondWidth = 84
    app.diamondHeight = 42
    app.moveDotR = 15
    app.moveDotCx = 0
    app.moveDotCy = 0
    app.dx = 5
    app.titleRectWidth = 100
    app.titleRectHeight = 160
    app.spaceBetweenCardGroup = 20
    newGame(app)
    

def newGame(app):
    app.playScreenCounter = 0
    app.playScreenTimeScore = 0
    app.board, app.foundSet = getRandomBoardWithSet(app.dims, app.targetBoardSize)
    app.cardStates = [False, False, False, False, False, False, False, False]
    app.wrongOrCorrect = None
    app.roundsLeft = 4
    app.lives = 2
    app.gameWon = None

def newBoard(app):
    app.wrongOrCorrect = None
    app.board, app.foundSet = getRandomBoardWithSet(app.dims, app.targetBoardSize)
    app.cardStates = [False, False, False, False, False, False, False, False]
    app.gameWon = None
    

####################################################
# Code used by multiple screens
####################################################

def onKeyPressHelper(app, key):
    if   key == 'd': setActiveScreen('setDimsScreen')
    elif key == 't': setActiveScreen('setThemeScreen')
    elif key == '?': setActiveScreen('helpScreen')
    elif key == 'p': setActiveScreen('playScreen')

def drawScreenTitle(app, screenTitle):
    drawLabel('SuperSet!', app.width/2, 20, size=30, bold=True)
    drawLabel(screenTitle, app.width/2, 50, size=16, bold=True)

####################################################
# helpScreen
####################################################

def helpScreen_redrawAll(app):
    for i in range(8):
        if i <= 4:
            for j in range(3):
                drawRect(app.width/(5.5) + (i * 150) + (j * app.spaceBetweenCardGroup) , app.height/3 - (j*16), app.titleRectWidth, 
                            app.titleRectHeight , fill = 'fireBrick', border = 'black', align = 'center', opacity =  (33*j))
            
            drawRect(app.width/(5.5) + (i * 150), app.height/3 , app.titleRectWidth, app.titleRectHeight , fill = 'fireBrick', 
                        border = 'black', align = 'center')
            drawLabel(app.gameName[i], app.width/5.5 + (i * 150), app.height/3, border = 'black',size = 50)
        elif i > 4:
            for j in range(3):
                drawRect(app.width/(5.5) + ((i-4) * 150) + (j * app.spaceBetweenCardGroup) , app.height/3  - (j*16) + 250, app.titleRectWidth, 
                            app.titleRectHeight , fill = 'fireBrick', border = 'black', align = 'center', opacity =  (33*j))
            drawRect(app.width/5.5 + ((i-4) * 150), app.height/3 + 250, app.titleRectWidth, app.titleRectHeight , fill = 'fireBrick', 
                        border = 'black',  align = 'center')
            drawLabel(app.gameName[i], app.width/5.5 + ((i-4) * 150), app.height/3 + 250, border = 'black', size = 50)
            
    drawLabel('Press D for Setting Dimensions', app.width/5, 570)
    drawLabel('Press T for Setting Themes', app.width*(2/5), 570)
    drawLabel('Press ? for Help Screen', app.width*(3/5), 570)
    drawLabel('Press P for Play Screen', app.width*(4/5), 570)
    drawLabel('In Super Set, you want to choose a group of 3 or 4 cards where all the attributes of the cards are the same or different.', app.width/2, 40)
    drawLabel('To have more fun, you can change the dimensions of the game which adds more attributes to the cards.', app.width/2, 60)

def helpScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)

####################################################
# setDimsScreen
####################################################

def setDimsScreen_onScreenActivate(app):
    app.lessDims = False
    app.one5 = False
    app.dim2Big = False
    app.editedDims = copy.copy(app.dims)

def setDimsScreen_redrawAll(app):
    drawScreenTitle(app, 'Set Dimensions Screen')
    drawLabel(f'Current Dimensions:{app.dims}', app.width/2, 100, size = 16)
    drawLabel('Use digits 3-5 and backspace to type the new dimesions', app.width/2, 150, size = 16)
    drawLabel('Press enter to set the new dimensions', app.width/2, 170, size = 16)
    drawLabel(f'New Dimensions: {app.editedDims}', app.width/2, 200, size = 16)
    
    if app.lessDims:
        drawLabel('Must have at least 2 features!', app.width/2, 250, size = 16, fill = 'red')
    elif app.one5:
        drawLabel('Dims have have at most one 5 (or app is too slow)', app.width/2, 250, size = 16, fill = 'red')
    elif app.dim2Big:
        drawLabel('Dims must sum to 15 or less (or app is too slow)', app.width/2, 250, size = 16, fill = 'red')
    else:
        return None


def setDimsScreen_onKeyPress(app, key):
    allowedDigits = ['3','4','5']
    
    if key in allowedDigits:
        app.editedDims.append(int(key))
    if key == 'backspace':
        app.lessDims = False
        app.one5 = False
        app.dim2Big = False
        app.editedDims = app.editedDims[:-1]
    if key == 'enter':
        if len(app.editedDims) < 2:
            app.lessDims = True
        elif app.editedDims.count(5) > 1:
            app.one5 = True
        elif sum(app.editedDims) > 15:
            app.dim2Big = True
        else:
            app.dims = app.editedDims
            if dimsTooLargeForTheme(app): #if dims greater than a theme, then switch to letters
                app.theme = app.allThemes[0]
            newBoard(app)
            setActiveScreen('playScreen')
    
    onKeyPressHelper(app, key)
    
def dimsTooLargeForTheme(app):
    if app.theme == 'Standard':
        if (4 in app.dims) or (5 in app.dims):
            return True
    if app.theme == 'Special':
        if 5 in app.dims:
            return True
    if app.theme == 'On the Move':
        if (4 in app.dims) or (5 in app.dims):
            return True
    return False
            
####################################################
# setThemeScreen
####################################################

def setThemeScreen_redrawAll(app):
    drawScreenTitle(app, 'Set Theme Screen')
    drawLabel(f'Current Theme: {app.theme}', app.width/2, 100, size = 16)
    drawLabel('Use digits or arrows to see the new theme', app.width/2, 150, size = 16)
    
    for i in range(len(app.allThemes)):
        if app.theme == app.allThemes[i]:
            color = 'red'
        else:
            color = 'black'
        drawLabel(f'Theme {i}: {app.allThemes[i]}' , 50, 170 + i * 20, size = 16, align = 'left', fill = color)

def setThemeScreen_onKeyPress(app, key):
    if dimsTooLargeForTheme(app): #if dims greater than a theme, then switch to letters
                app.theme = app.allThemes[0]
    allowedKeys = ['0', '1', '2', '3']
    if key == 'up':
        switchTheme(app, 'up')
    if key == 'down':
        switchTheme(app, 'down')
    if key in allowedKeys:
        app.theme = app.allThemes[int(key)]
    if key == 'r': 
        app.theme = app.allThemes[random.randrange(0,4)]
        
    onKeyPressHelper(app, key)
    
def switchTheme(app, direction):
    for i in range(len(app.allThemes)):
        if app.theme == app.allThemes[i]:
            if (0 <= i < (len(app.allThemes) - 1)) and direction == 'down':
                i += 1
                app.theme = app.allThemes[i]
                break
            elif (0 < i <= (len(app.allThemes) - 1)) and direction == 'up':
                i -= 1
                app.theme = app.allThemes[i]
                break 
            else:
                return

####################################################
# playScreen
####################################################


def playScreen_redrawAll(app):
    dashes = None
    drawScreenTitle(app, 'Play Screen')
    
    drawLabel(f'dims = {app.dims}', app.width*(1/6), 110, size=16)
    drawLabel(f'theme = {app.theme}', app.width*(2/6), 110, size=16)
    drawLabel(f'rounds left = {app.roundsLeft}', app.width*(3/6), 110, size=16)
    drawLabel(f'lives left = {app.lives}', app.width*(4/6), 110, size=16)
    drawLabel(f'elapsed time = {app.playScreenTimeScore}', app.width*(5/6), 110, size = 16)
    drawLabel('Press h for a hint!', 25, 200, size = 16, align = 'left')
    drawLabel(f'Choose {min(app.dims)} cards!', app.width/2, 80, size = 16)
    
    
    for i in range(app.targetBoardSize): 
        
        #game over screens
        if app.gameWon: 
            drawLabel(f'You won in {app.playScreenTimeScore} seconds!', app.width/2, app.height/2, size = 50, bold = True)
            drawLabel(f'Press n to play a new game!', app.width/2, app.height/2 + 40, size = 16)
        elif app.gameWon == False:
            drawLabel(f'Game Over :(((', app.width/2, app.height/2, size = 50, bold = True)
            drawLabel(f'Press n to play a new game!', app.width/2, app.height/2 + 40, size = 16)
        
        else:
            #bordercolor based on states
            if app.cardStates[i]: #if clicked, gold border
                dashes = True
                border = 'gold'
                if app.wrongOrCorrect: #all correct
                    drawLabel('Correct!', app.width/2, 130, fill = 'green', size = 16)
                    drawLabel('Press any key or the mouse to continue', app.width/2, 150, fill = 'green', size = 16)
                    border = 'green'
                elif app.wrongOrCorrect == False: #all wrong
                    border = 'red'
                    drawLabel('Incorrect!', app.width/2, 130, fill = 'red', size = 16)
                    drawLabel('Press any key or the mouse to continue', app.width/2, 150, fill = 'red', size = 16)
            if app.cardStates[i] == False: #if not clicked then black border
                dashes = False
                border = 'black'
                
            #draw cards
            if i < 5:
                drawRect(app.rectLeft + i * 150, app.rectTop, app.rectWidth, app.rectHeight,
                         fill = None, border = border, borderWidth = 6, dashes = dashes)
            if i >= 5:
                drawRect(app.rectLeft + (i- 5) * 150, app.rectTop + app.spaceBetweenRect + app.rectHeight,
                         app.rectWidth, app.rectHeight, fill = None, border = border, 
                         borderWidth = 6, dashes = dashes)
                     
    
        if app.gameWon == None:#draw themes
            if app.theme == 'Letters':
                drawCardsInLettersTheme(app, i)
            elif app.theme == 'Standard':
                drawCardsInStandardTheme(app, i)
            elif app.theme == 'Special':
                drawCardsInSpecialTheme(app, i)
            elif app.theme == 'On the Move':
                drawCardsInMoveTheme(app,i)


def playScreen_onKeyPress(app, key):
    if app.gameWon == None:
        if app.wrongOrCorrect == None:
            if key == 'n':
                newGame(app)
            onKeyPressHelper(app, key)
            
        if key == 'h' and app.wrongOrCorrect != True:
            giveHint(app)
        
        if app.wrongOrCorrect != None:
            newBoard(app)
            
        checkSet(app)
    else:
        newGame(app)
    
def giveHint(app):
    app.playScreenTimeScore += 15
    cardsPressed = []
    for i in range(len(app.cardStates)):
        if app.cardStates[i] == True:
            cardsPressed.append(app.board[i])
    app.foundSet.sort()
    cardsPressed.sort()
    
    for card in cardsPressed:
        counter = 0
        if card not in app.foundSet:
            app.cardStates[getCardIndex(app, card)] = False
            return
        break
    for card in app.foundSet:
        if card not in cardsPressed:
            app.cardStates[getCardIndex(app, card)] = True
            return

def playScreen_onMousePress(app, mouseX, mouseY):
    counter = 0
    counter += 1
    
    if app.wrongOrCorrect != None:
        if counter >= 1:
            newBoard(app)
    
    #new board after playing a round + check is cards pressed
    #are correct or wrong
    checkSet(app)


def pressOnCard(app, mouseX, mouseY):
    #only press on certain num of cards and check if the correct number of cards are pressed and proceed
    if app.cardStates.count(True) != min(app.dims):
        for i in range(app.targetBoardSize):
            x0, y0, x1, y1 = getCardBounds(app, i)
            if (x0 <= mouseX <= x1) and (y0 <= mouseY <= y1):
                app.cardStates[i] = not app.cardStates[i]
                return True, i, app.cardStates
        return False, i, app.cardStates
        
        
def playScreen_onStep(app):
    
    if dimsTooLargeForTheme(app):
        app.theme = app.allThemes[0]
        
    #increment timer by once per second on home screen
    app.playScreenCounter += 1
    
    if (app.playScreenCounter % 20) == 0:
        if not app.gameWon:
            app.playScreenTimeScore += 1
            
    app.dx += 5

def checkSet(app):
    cardsPressed = []
    if app.cardStates.count(True) == len(app.foundSet):
        for i in range(len(app.cardStates)):
            if app.cardStates[i] == True:
                cardsPressed.append(app.board[i])
        if isSet(cardsPressed):
            app.roundsLeft -= 1
            app.wrongOrCorrect = True
        else:
            app.wrongOrCorrect = False
            app.roundsLeft -= 1
            app.lives -= 1
            
        if app.lives == 0:
            app.gameWon = False
        if app.roundsLeft == 0:
            app.gameWon = True
        
 
#draw cards Letters style
def drawCardsInLettersTheme(app, i):
    if i < 5:
        x0, y0, x1, y1, = getCardBounds(app, i)
        drawLabel(app.board[i], x0 + app.rectWidth/2, y0 + app.rectHeight/2, 
                    fill = 'black', size = 28, bold = True)
    if i >= 5:
        x0, y0, x1, y1, = getCardBounds(app, i)
        drawLabel(app.board[i], x0 + app.rectWidth/2, y0 + app.rectHeight/2, 
                    fill = 'black', size = 28, bold = True)
                    
def drawCardsInStandardTheme(app, i):
    card2Num = []
    for letter in app.board[i]:
        card2Num.append((ord(letter) - ord('A')))
    color, shape, numOfShapes, opacity = standardCharacteristics(app, card2Num) 
    
    if shape == 'oval':
        drawStandardOval(app, numOfShapes, color, opacity, i)
    if shape == 'star':
        drawStandardStar(app, numOfShapes, color, opacity, i)
    if shape == 'diamond':
        drawStandardDiamond(app, numOfShapes, color, opacity, i)
        
def drawStandardOval(app,numOfShapes, color, fillOpacity, i):
    x0, y0, x1, y1 = getCardBounds(app, i)
   
    for i in range(numOfShapes):
        drawOval(x0 + app.rectWidth/2, y0 + ((i + 1/2) * (app.rectHeight/numOfShapes)), 82, 42, 
                 fill = None, border = color )
        drawOval(x0 + app.rectWidth/2, y0 + ((i + 1/2) * (app.rectHeight/numOfShapes)), 82, 42, 
                     opacity = fillOpacity, fill = color, border = color )
        
def drawStandardStar(app,numOfShapes, color, fillOpacity, i):
    
    x0, y0, x1, y1 = getCardBounds(app, i)
    for i in range(numOfShapes):
        #drawOutline
        drawStar(x0 + app.rectWidth/2, y0 + ((i + 1/2) * (app.rectHeight/numOfShapes)), 25.2, 5, 
                 fill = None, border = color)
        #draw opacity
        drawStar(x0 + app.rectWidth/2, y0 + ((i + 1/2) * (app.rectHeight/numOfShapes)), 25.2, 5, 
                 fill = color, opacity = fillOpacity)
        
def drawStandardDiamond(app, numOfShapes, color, fillOpacity, i):
    x0, y0, x1, y1 = getCardBounds(app, i)
    for i in range(numOfShapes):
        topX = x0 + app.rectWidth/2 
        topY = y0 + ((i + 1/2) * (app.rectHeight/numOfShapes)) - app.diamondHeight/2
        #draw outline
        drawPolygon(topX, topY, topX + app.diamondWidth/2, topY + app.diamondHeight/2, 
                    topX, topY + app.diamondHeight,
                    topX - app.diamondWidth/2, topY + app.diamondHeight/2, 
                    fill = None, border = color)
        #draw opacity
        drawPolygon(topX, topY, topX + app.diamondWidth/2, topY + app.diamondHeight/2, 
                    topX, topY + app.diamondHeight,
                    topX - app.diamondWidth/2, topY + app.diamondHeight/2, 
                    fill = color, opacity = fillOpacity)
        
def standardCharacteristics(app, card):
    numOfShapes = 1
    opacity = 100
    counter = 0
    for v in card:
        counter += 1
        if counter == 1:
            if v == 0: color = 'red'
            elif v == 1: color = 'green'
            elif v == 2: color = 'blue'
        elif counter == 2:
            if v == 0: shape = 'oval'
            elif v == 1: shape = 'star'
            elif v == 2: shape = 'diamond'
        elif counter == 3:
            if v == 0: numOfShapes = 1
            elif v == 1: numOfShapes = 2
            elif v == 2: numOfShapes = 3
        elif counter == 4:
            if v == 0: opacity = 0
            elif v == 1: opacity = 25
            elif v == 2: opacity = 100
    return color, shape, numOfShapes, opacity

def drawCardsInSpecialTheme(app,i):
    card2Num = []
    for letter in app.board[i]:
        card2Num.append((ord(letter) - ord('A')))
    shape, color, speed, border = specialCharacteristics(app, card2Num) 
    
    if shape == 'square':
        drawSpecialSquare(app, shape, color, speed, border, i)
    if shape == 'triangle':
        drawSpecialTriangle(app, shape, color, speed, border, i)
    if shape == 'pentagon':
        drawSpecialPentagon(app, shape, color, speed, border, i)
    if shape == 'hexagon':
        drawSpecialHexagon(app, shape, color, speed, border, i)
        
def drawSpecialSquare(app, shape, color, speed, shapeBorder, i):
    x0, y0, x1, y1 = getCardBounds(app, i)
    if shapeBorder == 'lines':
        drawRect(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 60, 60, fill = color, border = 'black', 
                 rotateAngle = (app.playScreenCounter * speed),dashes = True, align = 'center' )
    elif shapeBorder == 5:
        drawRect(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 60, 60,fill = color, border = 'black', 
                 borderWidth = shapeBorder, rotateAngle = (app.playScreenCounter * speed), align = 'center')
    elif shapeBorder == None:
        drawRect(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 60, 60,fill = color, border = None, 
                 rotateAngle = (app.playScreenCounter * speed), align = 'center')
    else:
        drawRect(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 60, 60,fill = color, border = shapeBorder, 
                 rotateAngle = (app.playScreenCounter * speed), align = 'center')
        
def drawSpecialTriangle(app, shape, color, speed, shapeBorder, i):
    x0, y0, x1, y1 = getCardBounds(app, i)
    if shapeBorder == 'lines':
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 3,fill = color, border = 'black', 
                            rotateAngle = (app.playScreenCounter * speed), dashes = True, align = 'center' )
    elif shapeBorder == 5:
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 3,fill = color, border = 'black', 
                            borderWidth = shapeBorder, rotateAngle = (app.playScreenCounter * speed), align = 'center')
    elif shapeBorder == None:
         drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 3,fill = color, 
                            border = None, rotateAngle = (app.playScreenCounter * speed), align = 'center')
    else:
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 3, fill = color, 
                            border = shapeBorder, rotateAngle = (app.playScreenCounter * speed), align = 'center')
        
def drawSpecialPentagon(app, shape, color, speed, shapeBorder, i):
    x0, y0, x1, y1 = getCardBounds(app, i)
    if shapeBorder == 'lines':
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 5,fill = color, 
                            border = 'black', rotateAngle = (app.playScreenCounter * speed), dashes = True, align = 'center' )
    elif shapeBorder == 5:
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 5, fill = color, border = 'black', 
                            borderWidth = shapeBorder, rotateAngle = (app.playScreenCounter * speed), align = 'center')
    elif shapeBorder == None:
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 5, fill = color,
                            border = None, rotateAngle = (app.playScreenCounter * speed), align = 'center')
    else:
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 5, fill = color, 
                            border = shapeBorder, rotateAngle = (app.playScreenCounter * speed), align = 'center')
        
def drawSpecialHexagon(app, shape, color, speed, shapeBorder, i):
    x0, y0, x1, y1 = getCardBounds(app, i)
    if shapeBorder == 'lines':
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 6,fill = color, border = 'black', 
                            rotateAngle = (app.playScreenCounter * speed), dashes = True, align = 'center' )
    elif shapeBorder == 5:
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 6, fill = color,border = 'black', 
                            borderWidth = shapeBorder, rotateAngle = (app.playScreenCounter * speed), align = 'center')
    elif shapeBorder == None:
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 6, fill = color,border = None, 
                            rotateAngle = (app.playScreenCounter * speed), align = 'center')
    else:
        drawRegularPolygon(x0 + app.rectWidth/2, y0 + app.rectHeight/2, 40, 6,fill = color, border = shapeBorder, 
                            rotateAngle = (app.playScreenCounter * speed), align = 'center')
        
def specialCharacteristics(app, card):
    speed = 5
    border = 'black'
    counter = 0
    for v in card:
        counter += 1
        if counter == 1:
            if v == 0: color = 'orange'
            elif v == 1: color = 'pink'
            elif v == 2: color = 'cyan'
            elif v == 3: color = 'purple'
        elif counter == 2:
            if v == 0: shape = 'square'
            elif v == 1: shape = 'triangle'
            elif v == 2: shape = 'pentagon'
            elif v == 3: shape = 'hexagon'
        elif counter == 3:
            if v == 0: speed = 5
            elif v == 1: speed = -5
            elif v == 2: speed = 10
            elif v == 3: speed = -10
        elif counter == 4:
            if v == 0: border = None
            elif v == 1: border = 'black'
            elif v == 2: border = 5
            elif v == 3: border = 'lines'
    return shape, color, speed, border
    
def drawCardsInMoveTheme(app,i):
    card2Num = []
    for letter in app.board[i]:
        card2Num.append((ord(letter) - ord('A')))
    gradient, movement, gradDirection, numOfShapes = moveCharacteristics(app, card2Num) 
    drawMoveCircles(app, gradient, movement, gradDirection, numOfShapes, i)
    
    
def drawMoveCircles(app, colorGradient, movement, gradDirection, numOfShapes, i):
    x0, y0, x1, y1 = getCardBounds(app, i)
    
    left = x0 + ((app.dx * movement) % app.rectWidth)
    
    if left + app.moveDotR >= x0 + app.rectWidth:
        left = x0 + ((app.dx * movement) % app.rectWidth)
    
    if colorGradient == 'roy':
        for i in range(numOfShapes):
            top = y0 + ((i + 1/2) * (app.rectHeight/numOfShapes))
            drawCircle(left, top, app.moveDotR, fill = gradient('red', 'orange', 'yellow', start = gradDirection))
    elif colorGradient == 'greenBlue':
        for i in range(numOfShapes):
            top = y0 + ((i + 1/2) * (app.rectHeight/numOfShapes))
            drawCircle(left, top, app.moveDotR, fill = gradient('lightGreen', 'lightBlue', 'royalBlue', start = gradDirection))
        
    elif colorGradient == 'purPink':
        for i in range(numOfShapes):
            top = y0 + ((i + 1/2) * (app.rectHeight/numOfShapes))
            drawCircle(left, top, app.moveDotR, fill = gradient('lightPink', 'purple', 'indigo', start = gradDirection))
    

def moveCharacteristics(app, card):
    numOfShapes = 1
    movement = 1
    counter = 0
    for v in card:
        counter += 1
        if counter == 1:
            if v == 0: gradient = 'roy'
            elif v == 1: gradient = 'greenBlue'
            elif v == 2: gradient = 'purPink'
        elif counter == 2:
            if v == 0: gradDirection = 'left'
            elif v == 1: gradDirection = 'right'
            elif v == 2: gradDirection = 'top'
        elif counter == 3:
            if v == 0: movement = 0.3
            elif v == 1: movement = -0.3
            elif v == 2: movement = 0.7
        elif counter == 4:
            if v == 0: numOfShapes = 1
            elif v == 1: numOfShapes = 2
            elif v == 2: numOfShapes = 3
    return gradient, movement, gradDirection, numOfShapes
    

def getCardBounds(app, i):
    if i < 5:
        x0 = app.rectLeft + i * 150
        y0 = app.rectTop
        x1 = x0 + app.rectWidth
        y1 = y0 + app.rectHeight
        return x0, y0, x1, y1
    elif i >= 5:
        x0 = app.rectLeft + (i - 5) * 150
        y0 = app.rectTop + app.spaceBetweenRect + app.rectHeight
        x1 = x0 + app.rectWidth
        y1 = y0 + app.rectHeight
        return x0, y0, x1, y1

def getCardIndex(app, card):
    for i in range(len(app.board)):
        if app.board[i] == card:
            return i
###############################################
# Functions copied from console-based app
###############################################

def stringProduct(L):
    resultTuples = list(itertools.product(*L))
    resultStrings = [''.join(t) for t in resultTuples]
    return resultStrings

def combinations(L, n):
    return [list(v) for v in itertools.combinations(L, n)]

def allSame(L):
    seen = [L[0]]
    for v in L:
        if v not in seen:
            return False
    return True

def allDiffer(L):
    seen = []
    for v in L:
        if v in seen:
            return False
        else:
            seen.append(v)
    return True

def isSet(cards):
    compareCards = []
    cardSection = []
    rows, cols = len(cards), len(cards[0])
    for col in range(cols):     #put first element of each card in a 2D for easier comparison
        for row in range(rows):
            cardSection.append(cards[row][col])
        compareCards.extend([cardSection])
        cardSection = []
    
    for row in range(len(compareCards)):      #checking if cards are all same or all diff
        sameOrDiff = checkSetState(compareCards, row)
        if sameOrDiff == 'same':
            if allSame(compareCards[row]) == False:
                return False
        elif sameOrDiff == 'diff':
            if allDiffer(compareCards[row]) == False:
                return False
    return True
                
def checkSetState(compareCards, row): #helper for isSet
    if compareCards[row][0] == compareCards[row][1]:
        return 'same'
    else:
        return 'diff'


def makeSuperSetDeck(dims):
    allDims = []     
    dimNum = []
    for v in dims:
        for i in range(int(v)):
            dimNum.append(chr(ord('A') + i))
        allDims.extend([dimNum])
        dimNum = []
    return stringProduct(allDims)


def boardContainsSelection(board, selection):
    for v in selection:
        if v not in board:
            return False
    return True

def checkSelectionIsSet(board, selection, cardsPerSet):
    if board == []:
        return 'Empty board!'
    elif len(selection) != cardsPerSet:
        return 'Wrong number of cards!'
    elif checkDuplicates(selection):
        return 'Some of those cards are duplicates!'
    elif boardContainsSelection(board, selection):
        if isSet(selection):
            return True
        else:
            return 'Those cards do not form a set!'
    elif boardContainsSelection(board, selection) == False:
        return 'Some of those cards are not on the board!'
    
def checkDuplicates(selection): #helper for checkSelectionIsSet
    for i in range(len(selection)):
        if selection.count(selection[i]) != 1:
            return True
    return False
    
  
def findFirstSet(board, cardsPerSet):
    possCombinations = combinations(board, cardsPerSet)
    for v in possCombinations:
        if isSet(v):
            return v
    return None


def dealUntilSetExists(deck, cardsPerSet):
    newDeck = []
    for v in deck:
        if findFirstSet(newDeck, cardsPerSet) == None:
            newDeck.append(v)
        else:
            return sorted(findFirstSet(newDeck, cardsPerSet))

def getRandomBoardWithSet(dims, targetBoardSize):
    board = []
    newSuperSetDeck = makeSuperSetDeck(dims)
    random.shuffle(newSuperSetDeck)
    foundSet = dealUntilSetExists(newSuperSetDeck, min(dims))
    board.extend(foundSet)
    for v in newSuperSetDeck:
        if targetBoardSize == len(board):
            break
        elif v not in board:
            board.append(v)
                
    board.sort()
    return (board, foundSet)

####################################################
# main function
####################################################

def main():
    runAppWithScreens(initialScreen='helpScreen')

main()
