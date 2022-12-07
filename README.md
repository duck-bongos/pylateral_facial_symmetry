# pylateral_facial_symmetry
Like Bilateral, but Python, get it?


### Pipeline
0. Add (http://dlib.net/files/data/)[ibug_300W_large_face_landmark_dataset]
1. Run `train_shape_predictor.py ibug_300W_large_face_landmark_dataset`
2. Run `landmark_detection.py <trained_model_path>.dat <faces directory>`
