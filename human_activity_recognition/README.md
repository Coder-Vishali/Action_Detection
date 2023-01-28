# human-activity-recognition

Our project consists of three auxiliary files:

**action_recognition_kinetics.txt:** The class labels for the Kinetics dataset.

**resnet-34_kinetics.onx:** Rre-trained and serialized human activity recognition convolutional neural network trained on the Kinetics dataset.

**example_activities.mp4:** A compilation of clips for testing human activity recognition.


We will review two Python scripts, each of which accepts the above three files as input:

**human_activity_reco.py:** Our human activity recognition script which samples N frames at a time to make an activity classification prediction.

**human_activity_reco_deque.py**: A similar human activity recognition script that implements a rolling average queue. This script is slower to run; however, I’m providing the implementation so that you can learn from and experiment with it.
