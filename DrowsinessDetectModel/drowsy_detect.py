import cv2 as cv
import numpy as np
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE = [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398] # facial landmarks for the left eye
RIGHT_EYE = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]

RIGHT_IRIS = [474,475,476,477] # facial landmarks for left iris
LEFT_IRIS = [469,470,471,472] # facial landmarks for right iris

L_H_LEFT = [33] # Right Eye -> right most landmark
L_H_RIGHT = [133] # Right Eye -> left most landmark

R_H_LEFT = [362] # Left Eye -> right most landmark
R_H_RIGHT = [263] # Left Eye -> left most landmark
MOUTH_OUTLINE = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146, 61]

# calculate distance between two eye landmarks
def euclidean_distance(point1,point2):
    x1,y1, = point1.ravel()
    x2,y2, = point2.ravel()
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance

def mouth_aspect_ratio(mouth_landmarks):
    # Calculate the distances between the mouth landmarks
    p2_p8 = euclidean_distance(mouth_landmarks[1], mouth_landmarks[7])
    p3_p7 = euclidean_distance(mouth_landmarks[2], mouth_landmarks[6])
    p4_p6 = euclidean_distance(mouth_landmarks[3], mouth_landmarks[5])
    p1_p5 = euclidean_distance(mouth_landmarks[0], mouth_landmarks[4])




    # Calculate the mouth aspect ratio including the inner mouth
    mouth_aspect_ratio = (p2_p8 + p3_p7 + p4_p6) / (1.5 * p1_p5)
    return mouth_aspect_ratio


# classify eye position based on iris ratio
def iris_position(iris_center, right_point, left_point):
    # calculate the eye position ratio (ratio of where the pupil is based on the whole eye)
    center_to_right_dist = euclidean_distance(iris_center, right_point)
    total_eye_dist = euclidean_distance(right_point,left_point)
    eye_pos_ratio = center_to_right_dist / total_eye_dist


    iris_position = ""

    # classify eye location
    if eye_pos_ratio <= 0.34:
        iris_position="right"
    elif eye_pos_ratio > 0.34 and eye_pos_ratio <= 0.66:
        iris_position="center"
    else:
        iris_position="left"

    return iris_position, eye_pos_ratio




#Open webcam
cap = cv.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    max_num_faces=4,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv.flip(frame,1)
        rgb_frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        img_height,img_width = frame.shape[:2]
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            #print(results.multi_face_landmarks[0].landmark)
            mesh_points=np.array([np.multiply([p.x,p.y], [img_width, img_height]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            #print(mesh_points.shape)
            cv.polylines(frame,[mesh_points[MOUTH_OUTLINE]], True, (255,255,0), 1, cv.LINE_AA) # creates line around left eye
            #cv.polylines(frame,[mesh_points[MOUTH]], True, (0,255,0), 1, cv.LINE_AA) # creates line around right eye
            
            
            # find circle area for the pupils (iris)
            (l_cx,l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx,r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx,l_cy],dtype=np.int32)
            center_right = np.array([r_cx,r_cy],dtype=np.int32)

            #draw circle (segment) the pupils in the webcam feed
            cv.circle(frame,center_left,int(l_radius),(255,0,255),1,cv.LINE_AA)
            cv.circle(frame,center_right,int(r_radius),(255,0,255),1,cv.LINE_AA)


            

            cv.circle(frame,mesh_points[R_H_RIGHT][0], 3, (255,255,255),-1,cv.LINE_AA)
            cv.circle(frame,mesh_points[R_H_LEFT][0], 3, (0,255,255),-1,cv.LINE_AA)

            cv.circle(frame,mesh_points[L_H_RIGHT][0], 3, (255,255,255),-1,cv.LINE_AA)
            cv.circle(frame,mesh_points[L_H_LEFT][0], 3, (0,255,255),-1,cv.LINE_AA)


            

            iris_pos, eye_position_ratio = iris_position(
                center_right,mesh_points[R_H_RIGHT],mesh_points[R_H_LEFT][0]
                )
            
            mar = mouth_aspect_ratio(mesh_points[MOUTH_OUTLINE])

            
            


            # Write out iris position and ratio

            # Draw the text with a thicker line
            cv.putText(frame, f"Iris pos: {iris_pos}", (40, 50), cv.FONT_HERSHEY_PLAIN, 3.5, (0, 255, 0), 3, cv.LINE_AA)

            # Draw the ratio on a new line at the bottom
            cv.putText(frame, f"Ratio: {eye_position_ratio:.2f}", (40, 120), cv.FONT_HERSHEY_PLAIN, 3.5, (0, 255, 0), 3, cv.LINE_AA)

            # Draw the ratio on a new line at the bottom
            cv.putText(frame, f"MAR Ratio: {mar:.2f}", (40, 170), cv.FONT_HERSHEY_PLAIN, 3.5, (0, 255, 0), 3, cv.LINE_AA)

            if mar <2:
                # Draw the ratio on a new line at the bottom
                cv.putText(frame, f"WAKEUP!", (40, 210), cv.FONT_HERSHEY_PLAIN, 3.5, (0, 255, 0), 3, cv.LINE_AA)


        cv.imshow('img', frame)
        key = cv.waitKey(1)
        if key ==ord('q'): #if user presses q, then quit
            break
cap.release()
cv.destroyAllWindows()
