import cv2
import numpy as np
import os

refPt = []
cropping = False
image = []

def click_and_crop(event, x, y, flags, param):
    global refPt, cropping, image
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        image = np.array(image)
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

# fname = input("Enter file name: ")
def main_func(name_of_file, type_of_file, destination):
    global image
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(APP_ROOT, 'static', 'user-upload')
    image = cv2.imread(destination)
    print('type in click and crop', type(image))
    image = cv2.resize(image, (540,420))
    image = np.array(image)
    print('type in click and crop', type(image))
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)
    count = 0

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()
        elif key == ord("c"):
            if len(refPt) == 2:
                roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                cv2.imshow("ROI", roi)
                print('here')
                print(target + "/" + str(count) + "-" + name_of_file + '.jpeg')
                cv2.imwrite(target + "/" + name_of_file + "/" + str(count) + "-" + name_of_file + '.jpeg', roi)
                count += 1
                cv2.waitKey(0)
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()