from cmu_graphics import *
import random


# Project 2 Visual Selection Sort #

####################################################
####### Code used by multiple screens ##############
####################################################

def onKeyPressHelper(app, key):
    if   key == 'p': setActiveScreen('playScreen')
    elif key == 'b': setActiveScreen('startScreen')

####################################################
####### Starting Screen ############################
####################################################

def startScreen_redrawAll(app):
    drawRect(0,0,app.width, app.height, fill = 'aliceBlue')
    drawLabel('Visual Selection Sort', app.width/2, app.height/2 - 60, size=50, bold=True, fill = 'cornflowerBlue')
    drawLabel('Press P to Start!', app.width/2, app.height/2, size = 15, fill = 'cornFlowerBlue')
    
def startScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)

#################################################### 
####### Play Screen ################################
####################################################

def onAppStart(app):
    app.width = 720
    app.height = 600
    
    #window vars
    app.windowWidth = 560
    app.windowHeight = 400
    app.windowLeft = 80
    app.windowTop = 80
    
    #button vars
    app.buttonLeft = 70
    app.buttonTop = 500
    app.buttonWidth = 80
    app.buttonHeight = 50
    app.buttonOffset = 100
    app.buttonCoords = [(app.buttonLeft  + app.buttonOffset*i, app.buttonTop) for i in range(6)]
    app.buttonLabels = ['New Sort', 'Run', 'Pause', 'Step', 'Fast Mode', 'New Size']
    app.clickedButtons = [False] * len(app.buttonLabels)
    app.numOfBars = 16
    
    #steps
    app.stepsPerSecond = 20
    app.steps = 0
    
    #gameModes
    app.fastVer = False
    newSort(app, app.numOfBars)

#clicking newSort button or changing number of bars    
def newSort(app, numOfBars=5):
    app.barWidth = app.windowWidth/ (app.numOfBars + (2/3) + (2/3)*(app.numOfBars-1))
    app.bars = makeRandomBarHeightList(app.numOfBars)
    app.tempBars = ''
    app.barsLeftBottom = getBarLeftBottom(app)
    app.showNewSize = False
    
    #sorting variables
    app.maxBarI = None
    app.currentBarI = None
    app.lastSortedBar = app.numOfBars
    app.tempX, app.tempY = app.windowLeft + app.windowWidth/2 - app.barWidth/2, 460
    app.temp = False
    app.foundMax = False
    app.doneSort = False
    app.copies = 0
    app.comparisons = 0
    
    #auto sorting
    app.autoSort = False
    app.verType = 4 if app.fastVer else 10
    

def makeRandomBarHeightList(numOfBars): #make a random instances of bars all with different heights
    barLengths = []
    barObjects = []
    while len(barLengths) < numOfBars:
        possibleInt = random.randrange(1,numOfBars+1)
        if possibleInt not in barLengths: #ensure no duplicates
            barLengths.append(possibleInt)
    for length in barLengths:
        newBar = Bar(length)
        barObjects.append(newBar)
    return barObjects
        
class Bar:
    def __init__(self, height):
        self.height = height
        self.color = 'lightGreen'
        
    def __repr__(self):
        return f'bar{self.height}'
        
    def __eq__(self, other):
        if self.height == other.height:
            return True
            
    def __hash__(self):
        return hash(str(self))
        
    def isLarger(self, other):
        if isinstance(other, Bar):
            if self.height > other.height:
                return True
            elif self.height < other.height:
                return False

####################################################
## Drawing
####################################################

def playScreen_redrawAll(app):
    #drawBackground
    drawRect(0,0, app.width, app.height, fill = 'mintCream')
    
    #draw Visual Selection Sort Label
    drawLabel('Selection Sort Visualized!',app.windowLeft + app.windowWidth/2, app.windowTop/2, size = 32)
    
    #draw Window
    drawRect(app.windowLeft, app.windowTop, app.windowWidth, app.windowHeight, 
            fill = 'honeydew', border = 'darkOliveGreen', borderWidth = 1)
    
    #draw temp Label
    drawLabel('Temp',app.windowLeft+app.windowWidth/2, app.windowTop + 0.98*app.windowHeight, bold = True)
    
    #draw copies/comparisons
    drawLabel(f'Comparisons: {app.comparisons}', app.windowLeft +(1/3)*app.windowWidth, 575)
    drawLabel(f'Copies: {app.copies}', app.windowLeft +(2/3)*app.windowWidth, 575)
    
    #draw Buttons
    for i in range(6):
        rx, ry = app.buttonCoords[i]
        buttonName = app.buttonLabels[i]
            
        color = 'darkGreen' if app.clickedButtons[i] else 'darkSeaGreen' #change button color if pressed or not
        
        drawRect(rx, ry, app.buttonWidth, app.buttonHeight, fill = color)
        drawLabel(buttonName, rx + app.buttonWidth/2, ry + app.buttonHeight/2)
    
    #draw bars + rectangles
    
    if app.numOfBars <= 10: #cannot use same offset all the time otherwise, bars go off page
        barHeightOffset = 1.4
    elif 10 < app.numOfBars <= 20:
        barHeightOffset = 0.6
    else:
        barHeightOffset = (2/5) 
    
    for i in range(len(app.bars)): 
        rx, ry = app.barsLeftBottom[i]
        currentBar = app.bars[i]
        
        if app.temp: #if bar being copied, temporarily place the bar in the temp position
            if app.bars[app.maxBarI] == currentBar:
                drawRect(app.tempX, app.tempY, app.barWidth, currentBar.height * 10 * barHeightOffset, 
                        fill = currentBar.color, border = 'black', align = 'left-bottom', borderWidth = 1)
            else:
                drawRect(rx, ry, app.barWidth, currentBar.height * 10 * barHeightOffset, 
                        fill = currentBar.color, border = 'black', align = 'left-bottom', borderWidth = 1)
        else:
            drawRect(rx, ry, app.barWidth, currentBar.height * 10 * barHeightOffset, 
                        fill = currentBar.color, border = 'black', align = 'left-bottom', borderWidth = 1)
        
        # draw rects surrounding bars
        boxX, boxY = rx - 5, ry + 5 #offsets so rects are not drawn on top of bars 
        if app.maxBarI != None and app.maxBarI == i:
            drawRect(boxX, boxY, app.barWidth + 10, 200, fill = None, border = 'green', align = 'left-bottom')
            
            drawLabel('MAX', boxX+5 + (app.barWidth)/2, boxY + 16, fill = 'red', size = 10)
    
        if app.currentBarI != None and app.currentBarI == i:
            drawRect(boxX, boxY, app.barWidth + 10, 200, fill = None, border = 'green', align = 'left-bottom')
        
        #draw numbers below bars
        drawLabel(i+1, rx+app.barWidth/2, ry+12, bold = True)
        
    #draw resize canvas label
    if app.showNewSize:
        drawLabel(f'New Size: {app.tempBars}',590, 580, align = 'left')
        drawLabel(f'Enter a new size between 1-32',620, 560)
    
    
#drawing Bars
def getBarLeftBottom(app):
    app.barOffset = app.barWidth*(1/3) + app.windowLeft
    app.spaceBetweenBars = app.barWidth*(2/3)
    barBottomLeft = []
    for i in range(app.numOfBars):
       
        #draw bars
        rx = app.barOffset + app.barWidth*i + app.spaceBetweenBars*i
        ry = app.windowTop + app.windowHeight/2
        barBottomLeft.append((rx, ry))
        
    return barBottomLeft
    
    
####################################################
## Interacting with Buttons 
####################################################

def playScreen_onMousePress(app, mouseX, mouseY):
    for i in range(len(app.buttonCoords)):
        cx, cy = app.buttonCoords[i]
        if ((cx <= mouseX <= cx + app.buttonWidth) and (cy <= mouseY <= cy + app.buttonHeight)):
            buttonName = app.buttonLabels[i] #determine which button is clicked through name
            
            if buttonName == 'New Sort':
                clearButtons(app)           # "unclick" all other buttons
                app.autoSort = False        #stop taking steps automatically
                newSort(app)                
                
            if buttonName == 'Run':
                clearButtons(app)
                app.showNewSize = False #hide the text shown when choosing a new size
                app.autoSort = True
                app.clickedButtons[i] = app.autoSort #if autosorting, button should be clicked
            
            elif buttonName == 'Pause':
                clearButtons(app)
                app.showNewSize = False
                app.clickedButtons[i] = True
                app.autoSort = False
            
            elif buttonName == 'Step':
                clearButtons(app)
                app.showNewSize = False
                app.autoSort = False
                takeStep(app)
                app.clickedButtons[i] = True
            
            elif buttonName == 'Fast Mode': #only button that toggles 
                app.fastVer = not app.fastVer
                app.clickedButtons[i] = app.fastVer
            
            elif buttonName == 'New Size':
                clearButtons(app)
                app.autoSort = False
                app.showNewSize = True
                app.clickedButtons[i] = True
                
            app.verType = 2 if app.fastVer else 10 #if fast version clicked, change frequency of steps

def playScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)
    if app.showNewSize:
        if key.isdigit():
            app.tempBars += key
        if key == 'backspace':
            app.tempBars = app.tempBars[:-1]
        if key == 'enter':
            if app.tempBars != '' and 0 < int(app.tempBars) <= 32:
                app.numOfBars = int(app.tempBars)
                newSort(app, app.numOfBars)
                app.clickedButtons[-1] = False #"unclick" new sort button
    if key == 'g':
        app.numOfBars = 5
        newSort(app)
        app.autoSort = True
        
def clearButtons(app): #unclick all buttons except for the fast ver
    for j in range(6):
        if j != 4:
            app.clickedButtons[j] = False

####################################################
## Sorting
####################################################

def playScreen_onStep(app):
    app.steps += 1
    if app.autoSort:
        if app.steps % app.verType == 0:
            takeStep(app)

def swapBars(app):
    app.copies += 1
    if app.maxBarI == len(app.bars)-1: # if max is last bar, then just change the color of that bar
        app.lastSortedBar -= 1
        app.bars[app.maxBarI].color = 'black'
        return None
        
    #get heights of bars that are being compared    
    smallBar = app.bars[app.lastSortedBar-1]
    maxBar = app.bars[app.maxBarI]
    
    #get the already sorted bars
    alreadySorted = []
    for i in range(len(app.bars)):
        if app.bars[i].color == 'black':
            alreadySorted.append(app.bars[i])
    
    if smallBar == maxBar: #if max bar at end, no need to swap anything
        newBarOrder = app.bars[:app.lastSortedBar-1] + [maxBar] + alreadySorted
    else:
        newBarOrder = (app.bars[:app.maxBarI] + [smallBar] + 
                        app.bars[app.maxBarI+1:app.lastSortedBar-1] + [maxBar] + alreadySorted)
    
    app.bars = newBarOrder
    maxBar.color = 'black' 
    app.lastSortedBar -= 1

def takeStep(app):
    if not app.doneSort: #not done sorting
        if app.temp: # only if foundmax
            swapBars(app)
            if app.lastSortedBar <= 0: #if sorting is all done, remove boxes
                app.maxBarI = None
                app.currentBarI = None
                app.foundMax = False
                app.temp = False
                app.doneSort = True
                return
            
            app.foundMax = False #sorting not done
            app.temp = False
            
            if app.lastSortedBar-1 == 0: #reset currentBarI and maxBarI correctly
                app.maxBarI = 0
                app.currentBarI = 0
                app.foundMax = True
                
            else:
                app.maxBarI = 0
                app.currentBarI = 1
            
        elif app.foundMax:
            app.temp = True
            
        else:
            if app.lastSortedBar-1 == 0: # only one bar exception
                app.maxBarI = 0
                app.currentBarI = 0
                app.foundMax = True
            
            if app.maxBarI == None and app.lastSortedBar != 0: #changing indicies each iteration of the sort
                app.maxBarI = 0
                app.currentBarI = 1
                return
            
            #comparing bars
            currentBar, maxBar = app.bars[app.currentBarI], app.bars[app.maxBarI]
            
            if currentBar.isLarger(maxBar):
                app.maxBarI = app.currentBarI
                app.currentBarI = app.maxBarI + 1
                app.comparisons += 1
            elif maxBar.isLarger(currentBar):
                app.currentBarI += 1
                app.comparisons += 1
                
            if app.currentBarI == app.lastSortedBar: 
                app.currentBarI = None
                app.foundMax = True
                return
            
            
####################################################
## main function
####################################################

def main():
    runAppWithScreens(initialScreen='startScreen')

main()


