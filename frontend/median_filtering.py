import cv2

def median_subtract(noisy_img):
    noisy_img = cv2.cvtColor(noisy_img, cv2.COLOR_BGR2GRAY)
    background=cv2.medianBlur(noisy_img, 25)  # Kernel size is 25
    result=cv2.subtract(background, noisy_img)
    result=cv2.bitwise_not(result) # reverse foreground and bg color ( make fg as black and bg as white)
    thresh = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] 
    # 2nd parameter min threshold value, 3rd parameter - max threshold value, 4th param - binary as well as otsu
    return (thresh, background)