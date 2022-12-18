import os
from pathlib import Path
import sys
from typing import Optional, Union


import cv2
import mediapipe as mp
import numpy as np


from mediapipe_dataset_utils import (
    CORR_POINTS,
    CUSTOM_CONTOURS_GRAPH,
    SYMMETRY_SPEC,
    create_dataset,
)

# mediapipe utils
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def get_target_directory_files(dirpath: Optional[Union[str, Path]] = None):
    """Retrieve all the images you wish to analyze.

    Recursively search for images in the subdirectory.

    args:
        dirpath (Optional[Union[str, Path]): The directory where images will be
                                                searched. If empty, will return
                                                an empty list.

    returns:
        List[str]: List of all the files in the directory and subdirectories.

    """
    all_files = []
    if dirpath is None:
        pass

    else:
        dirpath = Path(dirpath) if isinstance(dirpath, str) else dirpath

        img_suffixes = (".jpeg", ".png", ".jpg")
        for fname in dirpath.rglob("*"):
            if fname.suffix in img_suffixes:
                all_files.append(fname.as_posix())

    return all_files


def sum_sq_err(a: np.ndarray, b: np.ndarray, round: int = 0) -> float:
    """Calculates the sum of squared errors:

    Cost function denoted by J in notes.

    args:
        a (np.ndarray): A MxN numpy array.
        b (np.ndarray): A MxN numpy array.
        round (int): The number of decimal places to round the output to.
                        Defaults to no rounding.

    returns:
        float: The sum of squared errors.
    """
    sse = np.sum(np.square(a - b))
    if round > 0:
        sse = np.round(sse, round)
    return sse


if __name__ in "__main__":
    dirname_results = "results"
    fname_results = f"{dirname_results}/symmetry_results.txt"

    try:
        target_dirpath = sys.argv[1]
        image_files = get_target_directory_files(target_dirpath)
    except IndexError:
        image_files = get_target_directory_files("altered_carbon/straight_on_faces")

    # file to write the results. Delete previous results.
    with open(fname_results, "w") as sl:
        # write header
        sl.write(
            "fname_image|epochs|closed_form_error|gradient_descent_error|gd_minus_cf_error|\n"
        )

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
    ) as face_mesh:
        for idx, fname in enumerate(image_files):
            fn = Path(fname)
            image = cv2.imread(fname)

            # Convert the BGR image to RGB before processing.
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Print and draw face mesh landmarks on the image.
            if not results.multi_face_landmarks:
                continue

            annotated_image = image.copy()
            for face_landmarks in results.multi_face_landmarks:
                X, Y = create_dataset(CORR_POINTS, face_landmarks.landmark)

                # Closed form computation:
                # ----------------------------------------------------------
                THETA = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
                y_hat = X.dot(THETA)
                cf_sse = sum_sq_err(y_hat, Y, round=5)

                # ----------------------------------------------------------

                # Stochastic Gradient Descent Approach
                # ----------------------------------------------------------
                theta = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])  # theta null

                EPOCHS = 10000
                learning_rate = 0.0005  # alpha
                MOMENTUM = 0.9  # set momentum constant
                change = 0.0  # initialize
                prev_err_value = 0.0
                error_threshold = (
                    0.01  # epsilon break the loop if the error < threshold
                )

                for i in range(EPOCHS):
                    # derivative of cost function, sum_sq_err, w.r.t theta:
                    derivative = (2 * X).T.dot((X.dot(theta)) - Y)

                    if MOMENTUM > 0:
                        # calculate momentum
                        new_change = learning_rate * derivative + MOMENTUM * change

                        # update weights
                        theta = theta - new_change

                        # update change
                        change = new_change
                    else:
                        theta = theta - learning_rate * derivative

                    # calculate new plane
                    y_pred = X.dot(theta)

                    # recalculate cost with new weights
                    error = sum_sq_err(y_pred, Y, round=5)

                    if error < error_threshold:
                        print(f"Error threshold met at epoch {i}: {error}")
                        break

                    # early stopping
                    if abs(error - prev_err_value) < 1e-6:
                        break

                    prev_err_value = error
                # ----------------------------------------------------------

                # write out symmetry results
                with open(fname_results, "a") as sr:
                    sr.write(
                        f"{fn.stem}|{i}|{cf_sse}|{error}|{np.round(error - cf_sse, 5)}|\n"
                    )

                # write out symmetry planes
                # ----------------------------------------------------------
                # closed form
                results_subdir = Path(dirname_results) / Path(fn.stem)
                if not os.path.exists(results_subdir):
                    os.mkdir(results_subdir)

                np.save(results_subdir / Path("closed_form"), THETA)

                # gradient descent
                np.save(results_subdir / Path("gradient_descent"), theta)

                # ----------------------------------------------------------

                # Draw landmarks and tesselations on on faces
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
                if not cv2.imwrite(
                    "mediapipe_annotated/" + fn.stem + ".png",
                    annotated_image,
                ):
                    raise "No File Written"
