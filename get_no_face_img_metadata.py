import cv2
from pathlib import Path

NO_FACE_DIRPATH = "/Users/dan/all_developing/sbu/cg/pylateral_facial_symmetry/altered_carbon/no_face_detected"

faces = [str(f) for f in Path(NO_FACE_DIRPATH).glob("**/*")]

# how big is each image?
for fpath_img in faces:
    face = cv2.imread(fpath_img)
    name = fpath_img.split("/")[-1]
    print(name, face.shape)
