# pylateral_facial_symmetry
Like Bilateral, but Python, get it?


### Pipeline
0. Add (http://dlib.net/files/data/)[ibug_300W_large_face_landmark_dataset]
1. Run `train_shape_predictor.py ibug_300W_large_face_landmark_dataset`
2. Run `landmark_detection.py <trained_model_path>.dat <faces directory>`

### Altered Carbon Faces Directory
I pulled images from actors in the show (https://en.wikipedia.org/wiki/Altered_Carbon_(TV_series))[Altered Carbon] because I like the show, the show has a lot of different lighting settings, and the cast is racial diverse. The hope is that this work will help test the capabilities and limitations of facial symmetry detection more generally. The images are stored under `altered_carbon/` organized in subdirectories named after the Altered Carbon character name. The images in the subdirectories are named with the actor's name and a `_<index>` value to keep images unique. Not all images of characters were taken from the show. I do not own the rights to any images.