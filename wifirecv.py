import cv2
import urllib.request
import numpy as np
import time

 
url='http://10.42.0.35/cam-hi.jpg'
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
 
count=0
 
 
while True:
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
    
    cv2.imshow("live transmission", frame)
 
    key=cv2.waitKey(5)
    
    if key==ord('k'):
        count+=1
        t=str(count)+'.png'
        cv2.imwrite(t,frame)
        print("image saved as: "+t)
        
        
    if key==ord('q'):
        break
    else:
        continue
 
cv2.destroyAllWindows()