import os
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from scipy.stats import linregress


from mediapipe_maps import CUSTOM_CONTOURS_GRAPH, IDX_SET, SYMMETRY_SPEC
from mp_map_ts import LEFT_IDX, RIGHT_IDX, CORR_POINTS, create_dataset

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


# For static images:
IMAGE_FILES = [
    "altered_carbon/dig_301/Dina_Shihabi_1.jpeg",
    "altered_carbon/kovacs_prime/Will_Yun_Lee_2.jpg",
    "altered_carbon/kristin_ortega/Martha_Higareda_0.jpeg",
    "altered_carbon/miriam_bancroft/Kristin_Lehman_0.jpeg",
    "altered_carbon/poe/Chris_Conner_1.jpg",
    "altered_carbon/reileen_kawahara/Dichen_Lachman_0.jpg",
    "altered_carbon/samir_abboud/Waleed_Zuaiter_0.jpeg",
    "altered_carbon/vernon_elliot/Ato_Essandoh_0.jpeg",
]


LEFT = set()
RIGHT = set()

"""
for idx in sel_set:
        tmp = set()
        lms = []
        for tess in edge_pairs:
            if idx in tess:
                i, j = tess
                if i in sel_set and j in sel_set:
                    continue

                elif idx == i:
                    if landmarks[i].x < landmarks[j].x:
                        tmp.add(j)
                        lms.append(tess)

                elif idx == j:
                    if landmarks[j].x < landmarks[i].x:
                        tmp.add(i)
                        lms.append(tess)

                else:
                    print(f"FUCK {tess}")

        RIGHT.update(tmp)
        create_face_sets(landmarks, tmp, lms, direction)
"""

"""
def create_face_sets(landmarks, sel_set, edge_pairs):
    if len(LEFT) == (468 - 28) // 2 and len(RIGHT) == (468 - 28) // 2:
        return

    for idx in sel_set:
        for e, tess in enumerate(edge_pairs):
            if idx in tess:
                print(e, tess)
                i, j = tess
                if i in sel_set and j in sel_set:
                    continue

                elif idx == i:
                    if landmarks[i].x > landmarks[j].x:
                        LEFT.add(j)
                        return create_face_sets(
                            landmarks, sel_set.union(LEFT), edge_pairs
                        )

                    else:
                        RIGHT.add(j)
                        return create_face_sets(
                            landmarks, sel_set.union(RIGHT), edge_pairs
                        )

                elif idx == j:
                    if landmarks[j].x > landmarks[i].x:
                        LEFT.add(i)
                        return create_face_sets(
                            landmarks, sel_set.union(LEFT), edge_pairs
                        )

                    else:
                        RIGHT.add(i)
                        return create_face_sets(
                            landmarks, sel_set.union(RIGHT), edge_pairs
                        )

                else:
                    print(f"FUCK {tess}")

"""
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
) as face_mesh:
    for idx, fname in enumerate(IMAGE_FILES):
        fn = Path(fname)
        image = cv2.imread(fname)
        # Convert the BGR image to RGB before processing.
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print and draw face mesh landmarks on the image.
        if not results.multi_face_landmarks:
            continue

        annotated_image = image.copy()
        for face_landmarks in results.multi_face_landmarks:
            # Closed form computation:
            # ----------------------------------------------------------
            X, Y = create_dataset(CORR_POINTS, face_landmarks.landmark)

            THETA = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
            y_hat = X.dot(THETA)
            SSE = np.sum(np.square(y_hat - Y))  # SSE
            rSSE = np.round(SSE)  # rounded SSE
            print(f"Sum of squared errors for {fn.stem}: {SSE}")
            # ----------------------------------------------------------

            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
            )
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
            )
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=CUSTOM_CONTOURS_GRAPH,
                landmark_drawing_spec=None,
                connection_drawing_spec=SYMMETRY_SPEC,
            )
            try:
                cv2.imwrite(
                    "mediapipe_annotated/" + fn.stem + ".png",
                    annotated_image,
                )

            except Exception as e:
                print(e)
