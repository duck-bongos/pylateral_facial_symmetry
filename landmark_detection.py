import glob
import os
from pathlib import Path
from queue import Queue
import shutil
import sys

from cv2 import (
    circle,
    destroyAllWindows,
    imread,
    imshow,
    imwrite,
    resize,
    waitKey,
    INTER_AREA,
)
import dlib
import numpy as np


if len(sys.argv) != 3:
    print(
        "Give the path to the trained shape predictor model as the first "
        "argument and then the directory containing the facial images.\n"
        "For example, if you are in the python_examples folder then "
        "execute this program by running:\n"
        "    ./face_landmark_detection.py shape_predictor_68_face_landmarks.dat ../examples/faces\n"
        "You can download a trained facial shape predictor from:\n"
        "    http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    )
    exit()

predictor_path = sys.argv[1]
faces_folder_path = sys.argv[2]

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
# win = dlib.image_window()


suffixes = ("*.jpg", "*.jpeg", "*.png")
fnames_faces = Queue()
for s in suffixes:
    l = list(Path(faces_folder_path).rglob(s))
    for thing in l:
        fnames_faces.put(str(thing))


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)

    for i in range(68):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    return coords


def annotate_image(img, lm):
    # img = image
    # lm = landmarks
    img = img.copy()
    for (x, y) in lm:
        # try the cv2 way
        circle(img, (x, y), 2, (0, 255, 255), -1)

    return img


def halve_image(img):
    resized = img.copy()
    h, w, _ = resized.shape
    h = h // 2
    w = w // 2
    dim = (w, h)

    resized = resize(resized, dim, interpolation=INTER_AREA)
    return resized


while not fnames_faces.empty():
    print(f"Queue size:\t{fnames_faces.qsize()}\n")

    f = fnames_faces.get()
    if "no_face_detected" in f:
        continue
    print("Processing file: {}".format(f))
    # img = dlib.load_rgb_image(f)
    cvimg = imread(f)

    # win.clear_overlay()
    # win.set_image(img)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(cvimg, 1)

    print("Number of faces detected: {}".format(len(dets)))

    #
    if len(dets) > 0 and "resized" in f:
        # overwrite original file
        new_fname = f.replace("_resized", "")
        if "twice" in f:
            new_fname = new_fname.replace("_twice", "")

        # overwrite original image name with new image content
        imwrite(new_fname, cvimg)

        # delete resized file:
        os.remove(f)

    # if you don't detect a face, let's do something about it
    if len(dets) == 0 and "resized" not in f:
        # rename the file to include "resized"
        print(
            f"\nWARNING!\n{'-'*30}\nFace not detected. Resizing by halving the image's height and width.\n"
        )
        curr = os.getcwd()
        curr_dirpath = f.split("/")[-2]
        fname = f.split("/")[-1]
        fname_resized = fname.replace(".", "_resized.")
        fname_new = curr + "/altered_carbon/" + curr_dirpath + "/" + fname_resized
        fnames_faces.put(fname_new)

        # resize the file
        resized = halve_image(cvimg)

        # now add the file to the directory
        imwrite(fname_new, resized)
        continue

    elif len(dets) == 0 and "twice" not in f:
        # rename the file a second time to include "twice"
        print(
            f"\nWARNING!\n{'-'*30}\n Face not detected ~AGAIN~. Resizing by halving the image's height and width.\n"
        )
        curr = os.getcwd()
        curr_dirpath = f.split("/")[-2]
        fname = f.split("/")[-1]
        fname_resized = fname.replace(".", "_twice.")
        fname_new = curr + "/altered_carbon/" + curr_dirpath + "/" + fname_resized
        fnames_faces.put(fname_new)

        # resize the file
        resized = halve_image(cvimg)

        # now add the file to the directory
        imwrite(fname_new, resized)
        continue

    elif len(dets) == 0 and "twice" in f and "resized" in f:
        curr = os.getcwd()
        new_dir = curr + "/altered_carbon/no_face_detected/"
        fname = f.split("/")[-1]
        fname_new = new_dir + fname
        shutil.copyfile(f, fname_new)
        assert os.path.exists(fname_new)
        # imshow("Altered Carbon Landmarks", cvimg)
        # waitKey(0)
        continue

    for k, d in enumerate(dets):
        print(
            "Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                k, d.left(), d.top(), d.right(), d.bottom()
            )
        )
        # Get the landmarks/parts for the face in box d.
        shape = predictor(cvimg, d)
        landmarks = shape_to_np(shape)
        # print("Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))

        # Draw the face landmarks on the screen.

        # 1. (self: _dlib_pybind11.image_window, center: _dlib_pybind11.point, radius: float, color: _dlib_pybind11.rgb_pixel=rgb_pixel(255,0,0)) -> None
        # 2. (self: _dlib_pybind11.image_window, center: _dlib_pybind11.dpoint, radius: float, color: _dlib_pybind11.rgb_pixel=rgb_pixel(255,0,0)) -> None
        new_image = annotate_image(cvimg, landmarks)

    fname_landmark_img = Path(faces_folder_path) / Path("landmarks") / Path(f).name
    if not os.path.exists(str(fname_landmark_img)):
        imwrite(str(fname_landmark_img), new_image)
    # imshow("Output", new_image)
    # waitKey(0)
    destroyAllWindows()
    # win.add_overlay(dets)
    # dlib.hit_enter_to_continue()


print(f"\nCLEANUP\n{'-'*30}")
# remove duplicates
dirname_no_face_detected = Path(faces_folder_path).glob("**/*")
for fname in dirname_no_face_detected:
    if "resized" in str(fname):
        # remame no_face_detected files
        if "no_face_detected" in str(fname):
            tmp = str(fname).replace("_resized_twice", "")
            tmpimg = imread(tmp)
            imwrite(tmp, tmpimg)
        os.remove(fname)

print(f"\nSuccess!\n{'-'*30}")
