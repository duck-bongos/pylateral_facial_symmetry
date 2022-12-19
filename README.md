# pylateral_facial_symmetry
Like Bilateral, but Python, get it?

### Table of Contents
1. [Directory Walkthrough](#directory-walkthrough)
2. [Code Depenencies](#code-dependencies)
2. [Usage](#usage)
3. [Faces Directory](#altered-carbon-faces-directory)
4. [View Report](CSE_528_Project_Report.pdf)

### Directory Walkthrough
* :open_file_folder: [altered_carbon](#altered-carbon-faces-directory) image directory.
* :open_file_folder: mediapipe_annotated: Where input images, annotated with `mediapipe`'s landmarks, tesselations, and a yellow center line I added, are stored.
* :open_file_folder: results: Where the image and matrix results are stored. To locate a particular file you can navigate the directory with `results/<image_stem_name>/<calculation_type>.<extension>`. Also contains a script, `results/view_results.py` that print out matrices and generate `matplotlib` 3D renderings of the symmetry plane vertices in a `*.png` file.
* :fire: find_symmetry: The main code used to detect symmetry planes.
* :briefcase: LICENSE: A copy of my 3-Clause license. Free commercial use is NOT granted.
* :ledger: README: The document you are currently reading.
* :fire: mediapipe_dataset_utils.py: A module for building generic sets of `mediapipe` identifying landmarks.
* :pencil: CSE_528_Project_Report.pdf: The final report for this project. This document describes what approaches were taken and how. 


### Code Dependencies
The following Python packages were used in the completion of this project. These packages may have their own upstream dependencies.
```
matplotlib            3.5.3
mediapipe             0.9.0.1
numpy                 1.21.6
opencv-contrib-python 4.6.0.66
opencv-python         4.6.0.66
```
Note: The `dlib` package is mentioned in this README and the project report as it was used in a prior iteration of this project. `dlib` is not needed to use this code.

### Usage
0. Install all packages outlined in [code dependencies](#code-dependencies).
1. Download this repository or unzip this directory in a directory location of your choice. We now designate that directory location as `DIRHOME`.
2. cd `DIRHOME`
3. Decide whether you want to use the default directory, `DIRHOME/altered_carbon/straight_on_faces`, or a directory of your own. I recommend using images of faces taken with a straight-on camera angle, though that is not required.
4. If using the default directory, simply run `python find_symmetry.py`. Otherwise, run `python find_symmetry.py <path/to/target/directory>`.
5. View results. Matrices and coordinate points will be found in the `results` directory. Images annotated with landmarks and center lines will be found in `mediapipe_annotated`.


### Altered Carbon Faces Directory
I pulled images from actors in the show [Altered Carbon](https://en.wikipedia.org/wiki/Altered_Carbon_(TV_series)) because I like the show, the show has a lot of different lighting settings, and the cast is racial diverse. The hope is that this work will help test the capabilities and limitations of facial symmetry detection more generally. The images are stored under `altered_carbon/` organized in subdirectories named after the Altered Carbon character name (e.g. 'Poe'). The images in the subdirectories are named with the actor's name and a `_<index>` value to keep images unique. Images were pulled from a google search using the actor's name and an optional additional phrase "Altered Carbon" in the search. Not all images of characters were taken from the show. I do not own the rights to any images.

There are two non actor-specific directories under `altered_carbon`, `no_face_detected` and `straight_on_faces`. `no_face_detected` is from a prior experiment using [`dlib`](http://dlib.net/) to identify face markers. `dlib` was not able to detect a face in any of the images contained in this directory. `straight_on_faces` is used with the experiments we ran with [`mediapipe`](https://google.github.io/mediapipe/solutions/face_mesh). This is the default directory for running the `find_symmetry.py` module.