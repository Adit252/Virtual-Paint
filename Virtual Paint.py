
#The source code have been taken from Murtazas Workshop of Robotics and Ai.



import cv2
import numpy as np
#Setting up the webcam
wc = cv2.VideoCapture(0)
wc.open(0)
wc.set(3,640)       #width
wc.set(4,480)       #height
wc.set(10,150)

my_colors = [[107, 104, 65, 167, 222, 255],
             [0, 103, 158, 179, 255, 255]]    #writing all the trackbar values of different colors

myColorValues = [[164, 73, 164],                          #BGR FORMAT
                 [0, 0, 255]]

myPoints = []                     #[x, y, colorID]

def findcolor(image, my_colors, mycolorvalues):
    
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                       #hue saturation value model, make it easy to make color adjustments
    count = 0
    newpoints = []
    for color in my_colors:    
    
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult, (x,y), 10, mycolorvalues[count], cv2.FILLED)
        
        if x!= 0 and y!= 0 : newpoints.append([x, y, count])
        count += 1
        #cv2.imshow(str(color[0]), mask)                   # we have randomly assignned name so as to get diff. colors
    return newpoints

def getContours(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)    #2nd argument s best for outer 
    x,y,width,height = 0,0,0,0
    for cnt in contours :
        area = cv2.contourArea(cnt)
        if area > 600:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)    #last argument is 3
            peri = cv2.arcLength(cnt, True)             #True means the shape is closed
            
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, width, height = cv2.boundingRect(approx)          #this will give the shape and size of the bounding boxes
    return x + width//2, y
    
def drawOnScreen(mypoints, mycolorvalues): 
    for point in mypoints:
       cv2.circle(imgResult, (point[0],point[1]), 10, mycolorvalues[point[2]], cv2.FILLED)    
                         
# Read until video is completed
while(wc.isOpened()):
  # Capture frame-by-frame
  ret, image = wc.read()
  image = cv2.flip(image,1)
  imgResult = image.copy()
  if ret == True:

    # Display the resulting frame
    newPoints = findcolor(image, my_colors, myColorValues)                               #calling the functions in the webcam to get all the colors
    
    if len(newPoints)!= 0 :
       for point in newPoints:
          myPoints.append(point)
    if len(myPoints)!= 0 :
        drawOnScreen(myPoints, myColorValues)
    
    
    cv2.imshow('Result', imgResult)
    # Press Q on keyboard to  exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  
  # Break the loop
  else: 
    break

# When everything done, release the video capture object
wc.release()
# Closes all the frames
cv2.destroyAllWindows()


