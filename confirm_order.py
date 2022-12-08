import numpy as np

fpath_test_npy = "/Users/dan/all_developing/sbu/cg/pylateral_facial_symmetry/annotated/landmarks/Chris_Conner_1.npy"
fpath_test_txt = (
    "/Users/dan/all_developing/sbu/cg/pylateral_facial_symmetry/np_landmarks.txt"
)

arr = np.load(fpath_test_npy)

txt_arr = np.zeros((68, 2), "int")
with open(fpath_test_txt) as txt:
    lines = txt.readlines()
    for i, line in enumerate(lines):
        if i > 0:
            txt_arr[i - 1] = (int(line[4:7]), int(line[8:11]))
print(np.equal(txt_arr, arr).all())
