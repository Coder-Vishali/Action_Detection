import os
import cv2
import numpy as np
import pathlib
from pathlib import Path

dataset_directory = r"gms"
folder = os.path.join(os.getcwd(), dataset_directory)
print("Data Directory: ", folder)

frame_directory = "gms_frames"
frames_path = os.path.join(os.getcwd(),frame_directory)
if not os.path.isdir(frames_path):
    print("creating folder: " + frames_path)
    os.makedirs(frames_path)

# Count the files in the given image folder
for class_path in pathlib.Path(folder).iterdir():
    print("\nClass path: ", class_path)
    class_frame_path = os.path.join(frame_directory, str(class_path).rsplit('\\', 1)[1])
    print("class_frame_path", class_frame_path)
    for path in pathlib.Path(class_path).iterdir():
        if path.is_file():
            # print("Video path: ", path)
            counter = 0
            cap = cv2.VideoCapture(os.path.normpath(path))
            ret, frame1 = cap.read()
            prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
            hsv = np.zeros_like(frame1)
            hsv[...,1] = 255

            # print("Folder name: ", str(path).rsplit('\\', 1)[1].rsplit('.', 1)[0])
            folder_path = os.path.join(class_frame_path, str(path).rsplit('\\', 1)[1].rsplit('.', 1)[0])
            if not os.path.isdir(folder_path):
                print("creating folder: " + folder_path)
                os.makedirs(folder_path)

            print("folder_path", folder_path)


            while(1):
                ret, frame2 = cap.read()
                if not ret:
                    break
                next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            
                # Normalize horizontal and vertical components
                horz = cv2.normalize(flow[..., 0], None, 0, 255, cv2.NORM_MINMAX)
                vert = cv2.normalize(flow[..., 1], None, 0, 255, cv2.NORM_MINMAX)
                horz = horz.astype('uint8')
                vert = vert.astype('uint8')
            
                mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                hsv[...,0] = ang*180/np.pi/2
                hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
                rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
            
                # cv2.imshow('frame2', rgb) # optical hsv
                # Show the components as images
                # cv2.imshow('Horizontal Component', horz)
                # cv2.imshow('Vertical Component', vert)
                # cv2.imwrite('opticalfb.png', frame2)
                outfile = os.path.join(folder_path, 'img_' + str(counter) + '.jpg')
                cv2.imwrite(outfile, rgb)
                outfile = os.path.join(folder_path, 'flow_x_' + str(counter) + '.jpg')
                cv2.imwrite(outfile, horz)
                outfile = os.path.join(folder_path, 'flow_y_' + str(counter) + '.jpg')
                cv2.imwrite(outfile, vert)
                # Increment counter to go to next frame
                counter += 1
                prvs = next


            cap.release()
            cv2.destroyAllWindows()
