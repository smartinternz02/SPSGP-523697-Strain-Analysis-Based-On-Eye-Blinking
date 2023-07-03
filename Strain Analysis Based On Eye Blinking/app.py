import datetime
import cv2
import dlib
import gtts
from imutils import face_utils
from scipy.spatial import distance as dist
from winotify import Notification,audio
from playsound import playsound
import random
from flask import Flask,Response,render_template
import numpy
import tkinter as tk
from tkinter import ttk

Detector=dlib.get_frontal_face_detector()
Predictor=dlib.shape_predictor('Shape_Predictor_68.dat')
Capture=cv2.VideoCapture(0)
EYE_AR_THRESH=0.22
EYE_FRAMES_MIN=2
EYE_FRAMES_MAX=5
EYE_THRESH=10


app=Flask(__name__)
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Urgent")
    style = ttk.Style(popup)
    style.theme_use('classic')
    style.configure('Test.TLabel', background='aqua')
    label = ttk.Label(popup, text=msg, style='Test.TLabel')
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()

def Eye_Aspect_Ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def Calc_EAR(frame,gray):
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    rects = Detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = Predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = Eye_Aspect_Ratio(leftEye)
        rightEAR = Eye_Aspect_Ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        #  Since eye blinking is performed by both eyes synchronously, the EAR of both eyes is averaged.
        ear = (leftEAR + rightEAR) / 2.0

        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        return ear

timediff=datetime.datetime.now()

def time_interval_passed():
    global timediff
    time_delta=datetime.datetime.now()-timediff
    seconds_passed=time_delta.total_seconds()
    if(seconds_passed>=60):
        timediff=datetime.datetime.now()
        return True

def NotifyLess():
    speech = gtts.gTTS("Hi You are Blinking Less than an Average Guy Blinks in a Minute...So just Blink Up")
    speech.save("output2.mp3")
    playsound("output2.mp3")
    popupmsg("Take Some Rest")
    benefits = [
        "Blinking keeps our eyes hydrated, preventing dryness and promoting optimal visual clarity.",
        "Through blinking, we naturally remove dust particles and debris, maintaining a clean and clear line of sight.",
        "Blinking is an essential part of eye hygiene, flushing out irritants and keeping our eyes comfortable.",
        "With each blink, we promote proper tear film distribution, ensuring efficient lubrication of our eyes.",
        "Blinking helps to reduce eye strain and eye fatigue, allowing us to sustain focus for longer periods.",
        "The act of blinking refreshes our eyes, revitalizing our visual perception and enhancing our awareness.",
        "By blinking, we prevent the eyes from becoming dry and itchy, providing relief and promoting comfort.",
        "Blinking is a natural mechanism that helps to regulate the brightness of the light we perceive.",
        "Through blinking, we maintain the integrity of our cornea, protecting it from potential damage or abrasions.",
        "Blinking is like a gentle reset button for our eyes, restoring their balance and promoting visual well-being.",
        "With every blink, we ensure a continuous supply of oxygen to our eyes, supporting their overall health.",
        "Blinking helps to reduce eye irritation and redness, keeping our eyes looking fresh and vibrant.",
        "The act of blinking provides a brief pause in our visual journey, allowing us to appreciate the beauty around us.",
        "Through blinking, we promote the natural production and flow of tears, contributing to eye health.",
        "Blinking is a natural reflex that helps to prevent the eyes from becoming dry and uncomfortable.",
        "With each blink, we protect our eyes from potential infections by washing away harmful microorganisms.",
        "Blinking helps to regulate the amount of light that enters our eyes, preventing overexposure and discomfort.",
        "The act of blinking gives our eyes a momentary break, reducing eye strain and promoting relaxation.",
        "Through blinking, we improve the overall comfort and well-being of our eyes, enhancing our quality of life.",
        "Blinking is an essential part of maintaining healthy vision, ensuring optimal eye function throughout the day.",
        "With every blink, we promote the even distribution of tears, preventing dry spots and maintaining clarity.",
        "Blinking acts as a natural defense mechanism, protecting our eyes from foreign objects and potential injuries.",
        "The act of blinking helps to regulate the moisture levels in our eyes, preventing dryness and irritation.",
        "Through blinking, we prevent the buildup of eye mucus, maintaining a clear and comfortable visual experience.",
        "Blinking is like a gentle massage for our eyes, relieving tension and promoting relaxation.",
        "With each blink, we create a protective barrier that shields our eyes from harmful environmental factors.",
        "Blinking helps to prevent eye fatigue and supports our ability to maintain focus and concentration.",
        "The act of blinking ensures that our eyes receive a constant supply of nutrients, promoting their vitality.",
        "Through blinking, we enhance the efficiency of our tear drainage system, maintaining optimal eye health.",
        "Blinking serves as a natural reflex that helps to prevent the eyes from becoming dry and irritated.",
        "With every blink, we allow our eyes to rest and recover, reducing strain and promoting visual comfort.",
        "Blinking is a natural mechanism that helps to protect the delicate tissues of our eyes from damage.",
        "The act of blinking helps to prevent the evaporation of tears, keeping our eyes moist and comfortable.",
        "Through blinking, we improve the stability of our tear film, ensuring a smooth and clear visual experience."]
    toast = Notification(app_id="Strain Alert",
                         title="Hey Man! You Are Blinking Less than the Average Guy Blinks in a Minute",
                         msg=benefits[random.randrange(0, len(benefits))],
                         duration="long",
                         icon='C:/Users/saic3/PycharmProjects/flaskProject/Pic.jpg')
    toast.set_audio(audio.LoopingAlarm2, loop=True)
    toast.add_actions(label="Just Blink Up!! Man Learn More About Blinking",
                      launch="https://www.spindeleye.com/blog/2017/03/the-importance-of-blinking/")
    toast.show()

def NotifyMore():
    speech = gtts.gTTS(
        "Hi You are Blinking More than an Average Guy Blinks in a Minute...Looks Like Stressed.. So I Advise You To Take Some Rest")
    speech.save("output1.mp3")
    playsound("output1.mp3")
    popupmsg("Take Rest For A While")
    disadvantages = [
        "Blinking can momentarily disrupt our focus and attention.",
        "Excessive blinking can be a sign of eye strain or fatigue.",
        "Frequent blinking may be associated with nervousness or anxiety.",
        "Rapid blinking can cause eye irritation and redness.",
        "Blinking can interrupt our visual perception, especially during critical moments.",
        "Prolonged periods of blinking can lead to missed visual information.",
        "Blinking may cause temporary blurring of vision.",
        "In certain situations, excessive blinking can be distracting to others.",
        "Frequent blinking can be a symptom of certain medical conditions or allergies.",
        "Blinking may contribute to a feeling of eye dryness or discomfort.",
        "Intense blinking can disrupt eye contact during social interactions.",
        "Rapid blinking can cause mascara or eye makeup to smudge.",
        "Excessive blinking may be perceived as a sign of nervousness or dishonesty.",
        "Blinking can temporarily obscure our view, especially when driving or operating machinery.",
        "Frequent blinking can be a result of digital eye strain from prolonged screen use.",
        "Rapid blinking may lead to eye fatigue and tiredness.",
        "Intense blinking can cause temporary sensitivity to light.",
        "Frequent blinking can interfere with concentration and productivity.",
        "Excessive blinking can draw unnecessary attention to the eyes.",
        "Blinking can momentarily interrupt the continuity of visual information during activities such as reading or studying.",
        "Rapid blinking can create a sense of visual instability or inconsistency.",
        "Frequent blinking can be a result of eye allergies or irritants in the environment.",
        "Blinking may cause temporary interruption of eye contact during important conversations.",
        "Excessive blinking can contribute to a sense of eye strain or eye heaviness.",
        "Intense blinking can disrupt the application of eye drops or contact lenses.",
        "Frequent blinking can be a symptom of certain eye disorders or conditions.",
        "Blinking can temporarily obstruct our view during precise tasks, such as threading a needle.",
        "Rapid blinking can cause eye makeup to smudge or smear.",
        "Excessive blinking can create a sense of self-consciousness or discomfort in social settings.",
        "Blinking may disrupt the flow of visual information during activities such as watching a movie or playing a video game.",
        "Frequent blinking can lead to temporary loss of visual continuity or smoothness.",
        "Intense blinking can cause temporary eye strain or eye fatigue.",
        "Blinking can temporarily obstruct our view of important details or objects.",
        "Excessive blinking can contribute to a sense of eye dryness or itchiness.",
        "Rapid blinking may create a sense of visual distraction or distortion.",
        "Frequent blinking can interfere with the effectiveness of eye-tracking technologies.",
        "Blinking can momentarily interrupt the accuracy of eye measurements during eye exams.",
        "Intense blinking can disrupt the visibility of subtle facial expressions.",
        "Excessive blinking can lead to a sense of self-consciousness or embarrassment.",
        "Blinking may cause temporary interruption of visual continuity during activities such as playing sports or driving.",
        "Frequent blinking can be a result of exposure to bright lights or glare.",
        "Rapid blinking can cause temporary changes in visual perception, such as flickering or dimming.",
        "Excessive blinking can contribute to a feeling of eye strain or eye tiredness.",
        "Blinking may cause temporary interruption of eye contact during important presentations or public speaking.",
        "Intense blinking can disrupt the application of eye makeup or cosmetic products.",
        "Frequent blinking can be a symptom of dry eye syndrome or other ocular surface disorders.",
        "Blinking can momentarily obstruct our view of fast-moving objects or events."
    ]
    toast = Notification(app_id="Strain Alerter(Desktop-Version)",
                         title="Hey Man! You Are Blinking More than the Average Guy Blinks in a Minute",
                         msg=disadvantages[random.randrange(0, len(disadvantages))],
                         duration="long",
                         icon='C:/Users/saic3/PycharmProjects/flaskProject/Pic.jpg')
    toast.set_audio(audio.LoopingAlarm6, loop=True)
    toast.add_actions(label="Just Blink Up!! You Might Be Suffering With Some More Stress So Try To Get Assistance",
                      launch="https://www.healthline.com/health/eye-health/eye-blinking")
    toast.show()



def GenerateFrames():
    Counter = 0
    totalBlinks = 0
    while True:
        sucess,frame=Capture.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        faces=Detector(gray)
        for face in faces:
            x1=face.left()
            x2=face.right()
            y1=face.top()
            y2=face.bottom()
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),4)
            landmarks=Predictor(gray,face)
            for n in range(36,48):
                x=landmarks.part(n).x
                y=landmarks.part(n).y
                cv2.circle(frame,(x,y),2,(255,189,113),-1)
        if time_interval_passed():
            if (totalBlinks < 12):
                NotifyLess()
                totalBlinks=0
            elif (totalBlinks > 36):
                NotifyMore()
                totalBlinks = 0
            totalBlinks = 0
        EAR = Calc_EAR(frame, gray)
        if EAR is not None:
            if EAR < EYE_AR_THRESH:
                Counter += 1
            else:
                if Counter >= EYE_FRAMES_MIN and Counter <= EYE_FRAMES_MAX:
                    totalBlinks += 1
                Counter = 0
            cv2.putText(frame, "Blinks: {}".format(totalBlinks), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                        2)
            cv2.putText(frame, "EAR: {:.2f}".format(EAR), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        ret,buffer=cv2.imencode(".jpg",frame)
        frame=buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +frame + b'\r\n')



@app.route('/')
def Base():
    return render_template("index.html")
@app.route('/Video')
def Video():
    return Response(GenerateFrames(),mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__=="__main__":
    app.run()