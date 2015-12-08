import numpy as np
import cv2
from distance import distance
from config import *
import random
import os

def nothing(x):
    pass

def processLine(fileName, autoFlag):

    cv2.namedWindow('sliders')
    cv2.namedWindow('sliders2')
    cv2.namedWindow('sliders3')
    cv2.resizeWindow("sliders", 1000, 350)
    cv2.resizeWindow("sliders2", 1000, 350)
    cv2.resizeWindow("sliders3", 1000, 50)

    cv2.createTrackbar('Horizontal Threshold','sliders',5,100,nothing)
    cv2.createTrackbar('Vertical Threshold','sliders',105,200,nothing)

    cv2.createTrackbar('a','sliders',90,100,nothing)
    cv2.createTrackbar('b','sliders',80,500,nothing)

    cv2.createTrackbar('Canny Threshold 1','sliders',102,300,nothing)
    cv2.createTrackbar('Canny Threshold 2','sliders',60,300,nothing)

    cv2.createTrackbar('Rho','sliders2',46,360,nothing)
    cv2.createTrackbar('Theta','sliders2',160,360,nothing)

    cv2.createTrackbar('Minimum Line Length','sliders2',1,300,nothing)
    cv2.createTrackbar('Maximum Line Gap','sliders2',50,300,nothing)

    cv2.createTrackbar('Note Threshold','sliders2',30,100,nothing)
    cv2.createTrackbar('Picture Scale','sliders2',1000,4000,nothing)

    cv2.createTrackbar('Final Threshold', 'sliders3',65,100,nothing)

    #cap = cv2.VideoCapture(0)

    template = cv2.imread(os.path.join(basedir, 'app', 'Python_OMR', 'note2.png'),0)
    w, h = template.shape[::-1]

    contProc = True
    saveFile = False
    notes = []
    tupleResult = []

    roughGuess = False

    scaleChanged = True
    thresholdChanged = True
    settingsChanged = True

    while(contProc):
        settingsChanged = scaleChanged | thresholdChanged
        # Capture frame-by-frame
        frameIn = cv2.imread(fileName)

        picScale = cv2.getTrackbarPos('Picture Scale','sliders2')/1000.0
        frame = cv2.resize(frameIn, (0,0), fx=picScale, fy=picScale) 

        #ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        a = 1+(2*cv2.getTrackbarPos('a','sliders'))
        if a == 1:
            a = 3
        b = -cv2.getTrackbarPos('b','sliders')

        bw = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, a, b)
    
        vertical = bw.copy()
        horizontal = bw.copy()

        horizThresh = cv2.getTrackbarPos('Horizontal Threshold','sliders')
        if horizThresh == 0:
            horizThresh = 1
        vertThresh = cv2.getTrackbarPos('Vertical Threshold','sliders')
        if vertThresh == 0:
            vertThresh = 1

        canny1 = cv2.getTrackbarPos('Canny Threshold 1','sliders')
        canny2 = cv2.getTrackbarPos('Canny Threshold 2','sliders')

        # extract lines
        horizontalsize = horizontal.shape[1] / horizThresh
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize,1))
        horizontal = cv2.erode(horizontal, horizontalStructure)
        horizontal = cv2.dilate(horizontal, horizontalStructure)

        # extract notes and other markings
        verticalsize = vertical.shape[0] / vertThresh
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1,verticalsize))
        vertical = cv2.erode(vertical, verticalStructure)
        vertical = cv2.dilate(vertical, verticalStructure)
        vertical = cv2.bitwise_not(vertical)
        vertical = cv2.GaussianBlur(vertical,(3,3),0)

        vertical_edges = cv2.Canny(vertical,canny1,canny2,apertureSize = 3)


        template_edges = cv2.Canny(template,canny1,canny2,apertureSize = 3)
        res = cv2.matchTemplate(vertical_edges,template_edges,cv2.TM_CCOEFF_NORMED)
        #res = cv2.matchTemplate(vertical,template,cv2.TM_CCOEFF_NORMED)
        threshold = cv2.getTrackbarPos('Note Threshold','sliders2')/100.0
        loc = np.where( res >= threshold)

        # filter redundant hits
        locReduced = []

        if loc is not None:
            for pt in zip(*loc[::-1]):
                x1,y1 = pt
                contains = False
                if locReduced is not None:
                    for locR in locReduced:
                        cx1,cy1 = locR
                        if distance((x1,y1),(cx1,cy1)) < 10.0:
                            contains = True
                            break
                if not contains:
                    locReduced.append((x1,y1))
                    
        # sort hits from left to right
        thresholdFinal = cv2.getTrackbarPos('Final Threshold','sliders3')/100.0
        locReducedFinal = []

        if locReduced is not None:
            locReduced = sorted(locReduced,key=lambda l:l[0])
            for i in range(len(locReduced)):
                loc = locReduced[i]
                newLoc = (int(loc[0]+w/2.0),int(loc[1]+h/2.0))
                locReduced[i] = newLoc
                cv2.circle(frame, (locReduced[i][0],locReduced[i][1]), 5, (0,0,255))

                # extract and filter subimages
                subim = vertical[(locReduced[i][1]-h/2):(locReduced[i][1]+h/2), (locReduced[i][0]-w/2):(locReduced[i][0]+w/2)].copy()
                filterResRaw = cv2.matchTemplate(subim,template,cv2.TM_CCOEFF_NORMED)
                filterResFinal = np.where( filterResRaw >= thresholdFinal)
                if filterResFinal is not None:
                    tempLocs = []
                    for filteredRes in zip(*filterResFinal[::-1]):
                        x1,y1 = filteredRes
                        newLoc = (int(x1+w/2.0),int(y1+h/2.0))
                        tempLocs.append(newLoc)
                    if len(tempLocs)>0:
                        cv2.circle(frame, (locReduced[i][0],locReduced[i][1]), 5, (0,255,0))
                        cv2.rectangle(frame, (locReduced[i][0]-w/2,locReduced[i][1]-h/2), (locReduced[i][0]+w/2,locReduced[i][1]+h/2), (255,200,0), 2)
                        locReducedFinal.append(locReduced[i])


        # get line calculation variables
        rho = np.pi/(cv2.getTrackbarPos('Rho','sliders2')+0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        theta = cv2.getTrackbarPos('Theta','sliders2')

        minLength = cv2.getTrackbarPos('Minimum Line Length','sliders2')
        maxGap = cv2.getTrackbarPos('Maximum Line Gap','sliders2')

        # calculate lines and get rid of redundant lines
        linesReduced = []

        lines = cv2.HoughLinesP(horizontal,1,rho,theta,minLineLength=minLength,maxLineGap=maxGap)
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                contains = False
                if linesReduced is not None:
                    for lineR in linesReduced:
                        cx1,cy1,cx2,cy2 = lineR
                        if distance((0,y1),(0,cy1)) < 5.0:
                            contains = True
                            break
                if not contains:
                    linesReduced.append((x1,y1,x2,y2))
                  
        # get y values of lines
        barYs = []
          
        if linesReduced is not None:
            linesReduced = sorted(linesReduced,key=lambda l:l[1])
            testtemp = 0
            for line in linesReduced:
                testtemp += 1
                x1,y1,x2,y2 = line
                cv2.line(frame, (x1,y1),(x2,y2),(0,255,0),2)
                barYs.append(y1)

        # calculate average distance between lines
        avgDist = 0.0

        if barYs is not None:
            if len(barYs) != 1:
                for i in range(len(barYs)-1):
                    avgDist += barYs[i+1]-barYs[i]
                avgDist /= len(barYs)-1

        errorTol = 0.25
        lineError = int(round(avgDist*errorTol, 0))
        
        # adjust picture scaling for accurate note detection
        multiplier = ((h-2.75)*1000)/(avgDist)
        if roughGuess is False:
            cv2.setTrackbarPos('Picture Scale', 'sliders2', int(round((multiplier*picScale),0)))
            roughGuess = True
            scaleChanged = True
        else:
            if multiplier > 1000:
                cv2.setTrackbarPos('Picture Scale', 'sliders2', int(round((1000*picScale)+1,0)))
                scaleChanged = True
            elif multiplier < 1000:
                cv2.setTrackbarPos('Picture Scale', 'sliders2', int(round((1000*picScale)-1,0)))
                scaleChanged = True
            else:
                scaleChanged = False

        # adjust vertical threshold more more accurate note detection
        linesCheck = cv2.HoughLinesP(vertical_edges,1,rho,theta,minLineLength=minLength,maxLineGap=maxGap)
        if linesCheck is not None:
            linesFlag = False
            for line in linesCheck:
                x1,y1,x2,y2 = line[0]
                cv2.line(frame, (x1,y1),(x2,y2),(255,0,0),2)
                for i in range(len(barYs)):
                    if distance((0,y1),(0,barYs[i])) < 5.0:
                        linesFlag = True
            if linesFlag:
                vertThreshAdj = vertThresh-1
                cv2.setTrackbarPos('Vertical Threshold','sliders', int(round(vertThreshAdj,0)))
                thresholdChanged = True
            else:
                thresholdChanged = False

        # calculate note location based on line locations
        if locReducedFinal is not None:
            for loc in locReducedFinal:
                result = None
                x1,y1 = loc
                if y1 < (barYs[0]-lineError):
                    numLines = (barYs[0]-y1)/float(avgDist)
                    for i in range(1,13):
                        distCalc = i*.5;
                        if distance((0,numLines),(0,distCalc)) < errorTol:
                            result = -i
                    #ledgerlineUp
                elif y1 > (barYs[len(barYs)-1]+lineError):
                    numLines = (y1-barYs[len(barYs)-1])/float(avgDist)
                    for i in range(1,13):
                        distCalc = i*.5;
                        if distance((0,numLines),(0,distCalc)) < errorTol:
                            result = i+8
                    #ledgerlineDown
                else:
                    for i in range(len(barYs)):
                        if distance((0,y1),(0,barYs[i])) <= lineError:
                            result = 2*i
                        elif distance((0,y1),(0,barYs[i]+avgDist*.5)) <= lineError:
                            result = (2*i)+1
                if result is not None:
                    result -= 5
                    result = -result
                    noteLetter = (result)%7
                    noteLetter += 97
                    octave = result/7
                    octave += 4
                    noteResult = ""
                    noteResult += chr(noteLetter)
                    noteResult += str(octave)
                    cv2.putText(frame,noteResult,(x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2,cv2.LINE_AA)
                    if saveFile == True:
                        contProc = False
                        notes.append(noteResult)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        cv2.imshow('frame2',template)
        cv2.imshow('frame3',horizontal)
        cv2.imshow('frame4',vertical)

        settingsChanged = scaleChanged | thresholdChanged
        if settingsChanged & autoFlag:
            saveFile = True

        if saveFile == True:
            outFile = open('Notes.txt','w')
            for i in range(len(notes)):
                temp = []
                temp.append(notes[i])
                temp.append(4)
                temp = tuple(temp)
                outFile.write(notes[i]+"\n")
                tupleResult.append(temp)
            outFile.close()

        if cv2.waitKey(1) & 0xFF == ord('s'):
            saveFile = True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        

    # When everything done, release the capture

    #cap.release()
    cv2.destroyAllWindows()
    if saveFile == True:
        return tupleResult

#result = processLine('testLine.jpg', False)
#if result is not None:
#    result = list(result)
#    for i in range(len(result)):
#        print result[i]