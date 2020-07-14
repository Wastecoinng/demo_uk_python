# # img = cv2.imread('barcode.png')

# # for barcode in decode(img):
# #     print(barcode.data)
# #     myData = barcode.data.decode('utf-8')
# #     print(myData)
import cv2 
from pyzbar.pyzbar import decode
key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
while True:
    try:
        check, frame = webcam.read()
        print(check) #prints true as long as the webcam is running
        print(frame) #prints matrix values of each framecd 
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'): 
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            webcam.release()
            img_new = cv2.imread('saved_img.jpg')
            img_new = cv2.imshow("Captured Image", img_new)
            decodedImg = decode(img_new)
            print(decodeImg)
            cv2.waitKey(1650)
            cv2.destroyAllWindows()
            print("Processing image...")
            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            print("Converting RGB image to grayscale...")
            gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            print("Converted RGB image to grayscale...")
            print("Resizing image to 28x28 scale...")
            img_ = cv2.resize(gray,(28,28))
            print("Resized...")
            img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
            print("Image saved!")
        
            break
        elif key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
        
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
# key = cv2. waitKey(1)
# webcam = cv2.VideoCapture(0)
# while True:
#     try:
#         check, frame = webcam.read()
#         print(check) #prints true as long as the webcam is running
#         print(frame) #prints matrix values of each framecd 
#         cv2.imshow("Capturing", frame)
#         key = cv2.waitKey(1)
#         if key == ord('s'): 
#             cv2.imwrite(filename='saved_img.jpg', img=frame)
#             webcam.release()
#             img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
#             img_new = cv2.imshow("Captured Image", img_new)
#             cv2.waitKey(1650)
#             cv2.destroyAllWindows()
#             print("Processing image...")
#             img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
#             print("Converting RGB image to grayscale...")
#             gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
#             print("Converted RGB image to grayscale...")
#             print("Resizing image to 28x28 scale...")
#             img_ = cv2.resize(gray,(28,28))
#             print("Resized...")
#             img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
#             print("Image saved!")
        
#             break
#         elif key == ord('q'):
#             print("Turning off camera.")
#             webcam.release()
#             print("Camera off.")
#             print("Program ended.")
#             cv2.destroyAllWindows()
#             break
        
#     except(KeyboardInterrupt):
#         print("Turning off camera.")
#         webcam.release()
#         print("Camera off.")
#         print("Program ended.")
#         cv2.destroyAllWindows()
#         break
    
# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode

# # img = cv2.imread('barcode.png')

# # for barcode in decode(img):
# #     print(barcode.data)
# #     myData = barcode.data.decode('utf-8')
# #     print(myData)

# # code = decode(img)
# # print(code)
# cap = cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)

# while True:
#     # success,img = cap.read()
#     # for barcode in decode(img):
#     #     print(barcode.data)
#     #     myData = barcode.data.decode('utf-8')
#     #     print(myData)
#     # cv2.imshow('Result', img)
#     # cv2.waitKey(1)

#     success,img = cap.read()
#     for barcode in decode(img):
#         myData = barcode.data.decode('utf-8')
#         print(myData) 
#         pts = np.array([barcode.polygon], np.int32)
#         pts = pts.reshape((-1,1,2))
#         cv2.polylines(img,[pts], True (255,0,255), 5)
#     cv2.imshow('Result', img)
#     cv2.waitKey(1)