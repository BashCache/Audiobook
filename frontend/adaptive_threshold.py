import cv2

def adaptive_thresholding(noisy_img):
    noisy_img = cv2.cvtColor(noisy_img, cv2.COLOR_BGR2GRAY)
    adaptive_th=cv2.adaptiveThreshold(noisy_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,10)
    # 2nd parameter - maximum value of threshold 255 (white) 
    # 3rd parameter - Adaptive method - Either Gaussian or Mean ( Gaussian is preferable as it takes weieghted sum of neighbouring pixels)
    # 4th paramter - Threshold ttype - Binary (black and white)
    # 5th parameter - kernel size ( here 15*15 )
    # 6th parameter - constant value that needs to be subtracted (trial and errror method try for different values)
    return (adaptive_th)