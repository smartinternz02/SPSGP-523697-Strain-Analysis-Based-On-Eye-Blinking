# SPSGP-523697-Strain-Analysis-Based-On-Eye-Blinking
Strain Analysis Based On Eye Blinking
## Statement
Blinking is a reflex, which means your body does it automatically. Babies and children only blink about two times per minute. By the time you reach adolescence that increases to 14 to 17 times per minute.Detecting eye blinks is important for instance in systems that monitor a human operator vigilance,e.g. driver drowsiness, in systems that warn a computer user staring at the screen without blinking for a long time to prevent the dry eye and the computer vision syndromes, in human-computer interfaces that ease communication for disabled people. There should be an application that monitors to let the user know that he might get strained.A neural network model is built which alerts the user if eyes are getting strained. This model uses the integrated webcam to capture the face (eyes) of the person. It captures the eye movement and counts the number of times a person blinks. If blink count deviates from the average value (if the number of blinks is less or more), then an alert is initiated by playing an audio message along with a popup message is displayed on the screen appropriately.
## How To Use



To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/smartinternz02/SPSGP-523695-Strain-Analysis-Based-On-Eye-Blinking.git

# Go into the repository
$ cd SPSGP-523695-Strain-Analysis-Based-On-Eye-Blinking
$ cd Project Files

# Create a Python Virtual Conda Environment and activate it: 
$ python -m venv ./venv
$ python -m pip install --upgrade pip
$ pip install --upgrade setuptools wheel

# Install dependencies
$ pip install -r requirements.txt

# Run the app
$ python app_eye.py

#Run the Web App:
$ python app.py
# Copy the IP Address on a web browser and use the application to see blink detection in real-time

```


## Approach

The blink detector computes a metric called the eye aspect ratio (EAR), introduced by Soukupová and Čech in their 2016 paper, Real-Time Eye Blink Detection Using Facial Landmarks[1]. The eye aspect ratio makes for an elegant algorithm that involves a very simple calculation based on the ratio of distances between facial landmarks of the eyes. 

Each eye is represented by 6 (x, y)-coordinates, starting at the left-corner of the eye, and then working clockwise around the remainder of the region:

![blink_detection_6_landmarks](https://user-images.githubusercontent.com/37685052/91079233-6ccfdf00-e661-11ea-8804-25269701d328.jpg) 

Based on this image, we can see find a relation between the width and the height of these coordinates. We can then derive an equation that reflects this relation called the eye aspect ratio (EAR): 

![blink_detection_equation](https://user-images.githubusercontent.com/37685052/91079328-8a04ad80-e661-11ea-90b7-01d89fad71d2.png)

The eye aspect ratio is approximately constant while the eye is open, but will rapidly fall to zero when a blink is taking place. Using this simple equation, we can avoid image processing techniques and simply rely on the ratio of eye landmark distances to determine if a person is blinking. A frame threshold range is used to ensure that the person actually blinked and that their eyes are not closed for a long time.

![blink_detection_plot](https://user-images.githubusercontent.com/37685052/91079315-87a25380-e661-11ea-9f03-9c32bee8f9cc.jpg)

In this project, I have used existing Deep Learning models that detect faces and facial landmarks from images/video streams. These return the coordinates of the facial features like left eye, right eye, nose, etc. which have been used to calculate EAR. Blinking rate is monitored per minute.


## Demo 

1. You can view a demo of this project here : https://youtu.be/dhH9OXlo34E
2. The Project Demo Can Also Be Accessed Through Drive Using:https://drive.google.com/file/d/1iyaNwaMJrpBo3LTv2JgQMPI9Tt7rRjfU/view?usp=sharing 

### References

1. [Research Paper: Real-Time Eye Blink Detection Using Facial Landmarks](http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)
2. [Facial and Landmark Recognition Models](http://dlib.net/)
3. [Eye Health knowledge](https://visionsource.com/blog/are-you-blinking-enough/)

## Extras
    1. Output ScreenShots are Kept in Project Files Output_Screeshots Folder
    2. Installation Video To Run and Configure Desktop Based App Is Provided
    3. All Flask static and Templates are Available With Required Images
    4. Assignment Folder Has Assignments(1,2,3)
    5. Both Document Version and PDF Version of Project Report is Given
    6. Doc in Project Files PDF Outside
