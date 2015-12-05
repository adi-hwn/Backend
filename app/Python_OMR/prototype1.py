import numpy as np
import cv2

def nothing(x):
    pass

def main():
    # Create a window
    cv2.namedWindow('sliders')

    cv2.createTrackbar('Canny Threshold 1','sliders',102,300,nothing)

    cv2.createTrackbar('Canny Threshold 2','sliders',60,300,nothing)

    cv2.createTrackbar('Rho','sliders',46,360,nothing)

    cv2.createTrackbar('Theta','sliders',160,360,nothing)

    cv2.createTrackbar('Minimum Line Length','sliders',1,300,nothing)

    cv2.createTrackbar('Maximum Line Gap','sliders',50,300,nothing)

    cv2.createTrackbar('Note Threshold','sliders',67,100,nothing)

    cv2.createTrackbar('Note Scale','sliders',100,400,nothing)

    #cap = cv2.VideoCapture(0)
    
    templateIn = cv2.imread('note.jpg',0)
    

    while(True):
        # Capture frame-by-frame
        frame = cv2.imread('C-Major.jpg')
        #ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        canny1 = cv2.getTrackbarPos('Canny Threshold 1','sliders')
        canny2 = cv2.getTrackbarPos('Canny Threshold 2','sliders')

        rho = np.pi/(cv2.getTrackbarPos('Rho','sliders')+0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        theta = cv2.getTrackbarPos('Theta','sliders')

        minLength = cv2.getTrackbarPos('Minimum Line Length','sliders')
        maxGap = cv2.getTrackbarPos('Maximum Line Gap','sliders')

        noteScale = cv2.getTrackbarPos('Note Scale','sliders')/100.0
        template = cv2.resize(templateIn, (0,0), fx=noteScale, fy=noteScale) 
        w, h = template.shape[::-1]

        closePoints = []

        edges = cv2.Canny(gray,canny1,canny2,apertureSize = 3)
        lines = cv2.HoughLinesP(edges,1,rho,theta,minLineLength=minLength,maxLineGap=maxGap)
        if lines != None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(frame, (x1,y1),(x2,y2),(0,255,0),2)
                closePoints.append([x1,y1])
                closePoints.append([x2,y2])

        rets, labels, centers = cv2.kmeans(np.array(closePoints,dtype=np.float32),10,None,(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10),1,cv2.KMEANS_PP_CENTERS)
        centers = centers.tolist()
        for centerPoint in centers:
            cv2.circle(frame, (int(centerPoint[0]),int(centerPoint[1])), 5, (255,0,0))


        #template_edges = cv2.Canny(template,canny1,canny2,apertureSize = 3)
        #res = cv2.matchTemplate(edges,template_edges,cv2.TM_CCOEFF_NORMED)
        #threshold = cv2.getTrackbarPos('Note Threshold','sliders')/100.0
        #loc = np.where( res >= threshold)
        #for pt in zip(*loc[::-1]):
        #    cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        res = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = cv2.getTrackbarPos('Note Threshold','sliders')/100.0
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        ## Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # When everything done, release the capture
    #cap.release()
    cv2.destroyAllWindows()

main()