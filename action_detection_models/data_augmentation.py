import numpy as np
import albumentations as A
import cv2
import os
from datetime import datetime
from skimage.util import random_noise

# scale rotate  -1
# horizontal flip - 2
# blur - 3
# salt and pepper noise - 4
# saturation - 5

begin_time = datetime.now()
kernel2 = np.ones((5, 5), np.float32) / 25
folder = os.path.join(os.getcwd(), r'GMS\baggage_handling')
for count, filename in enumerate(os.listdir(folder)):
    begin_time_each = datetime.now()
    video_path = os.path.join(folder, filename)
    cap = cv2.VideoCapture(video_path)
    # Properties
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Augmentation - scale rotate
    transform_1 = A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.2)
    video_writer_1 = cv2.VideoWriter(f'output\{filename.split(".")[0]}_1.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Augmentation  - Horizontal flip
    transform_2 = A.HorizontalFlip(p=0.5)
    video_writer_2 = cv2.VideoWriter(f'output\{filename.split(".")[0]}_2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Augmentation  - blur
    transform_3 = A.OneOf([
            A.MotionBlur(p=0.2),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.Blur(blur_limit=3, p=0.1),
        ], p=0.2)
    video_writer_3 = cv2.VideoWriter(f'output\{filename.split(".")[0]}_3.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Augmentation  - salt and pepper noise
    video_writer_4 = cv2.VideoWriter(f'output\{filename.split(".")[0]}_4.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Augmentation  - saturation
    transform_5 = A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=0.1, val_shift_limit=0.1, p=0.3)
    video_writer_5 = cv2.VideoWriter(f'output\{filename.split(".")[0]}_5.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Loop through each frame
    for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break
        # Convert to gray
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # color conversion
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Augment an image
        transformed = transform_1(image=frame)
        video_writer_1.write(transformed["image"])

        # Augment an image
        transformed = transform_2(image=frame)
        video_writer_2.write(transformed["image"])

        # Augment an image
        frame = cv2.filter2D(src=frame, ddepth=-1, kernel=kernel2)
        video_writer_3.write(frame)

        # Augment an image
        frame = random_noise(frame, mode='s&p', amount=0.3)
        frame = np.array(255 * frame, dtype='uint8')
        video_writer_4.write(frame)

        # Augment an image
        transformed = transform_5(image=frame)
        video_writer_5.write(transformed["image"])

    print(f"Video name: {filename} \t FPS: {fps} \t Time: {datetime.now() - begin_time_each}")

    # Close down everything
    video_writer_1.release()
    video_writer_2.release()
    video_writer_3.release()
    video_writer_4.release()
    video_writer_5.release()
    cap.release()
    cv2.destroyAllWindows()

print("[INFO] Execution time to perform video augmentation: ", datetime.now() - begin_time)