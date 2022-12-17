"""Created a symmetry map from point to point such that we can identify which landmarks """

from pathlib import Path
import sys
from typing import Dict, List, Optional, Tuple, Union

import cv2
from matplotlib.patches import Polygon
import numpy as np
from PIL import Image, ImageDraw

from dlib_maps import (
    BILATERAL_MAP,
    LEFT_HALF_OUTLINE_LANDMARKS,
    OUTLINE_HALF_FACE_LEFT,
    OUTLINE_HALF_FACE_RIGHT,
    SYMMETRY_MAP,
)


def get_mask_outline(
    img: np.array, landmarks: List[int], points_array: np.ndarray, fname=Optional[str]
):

    msk_outline = [points_array[l - 1] for l in landmarks]
    image = Image.new("L", (img.shape[1], img.shape[0]), 0)
    ImageDraw.Draw(image).polygon([(y, x) for y, x in msk_outline], outline=1, fill=255)
    mask = np.array(image)
    if fname:
        cv2.imwrite(fname, mask)

    return mask


def draw_corresponding_points(
    img: np.ndarray,
    points_array: np.ndarray,
    points_map: Dict[int, int],
    line_color: Tuple[int, int, int] = (0, 255, 255),
):
    img = img.copy()

    for k, v in points_map.items():
        source = points_array[k - 1]
        dest = points_array[v - 1]

        cv2.line(img, source, dest, line_color, 2)

    # cv2.imshow("Diff", mask); cv2.waitKey(0)
    #  = (255, 0, 255)

    return img


def construct_half_face(
    img: np.ndarray,
    points_array: np.ndarray,
    points_map: Dict[int, int],
    line_map: Optional[Dict[int, int]] = None,
    line_color: Tuple[int, int, int] = (0, 255, 255),
) -> None:
    """For display purposes only."""
    img = img.copy()
    # draw corresponding points first
    img = draw_corresponding_points(
        img=img,
        points_array=points_array,
        points_map=points_map,
        line_color=line_color,
    )

    # draw the bilateral line last
    if line_map:
        img = draw_corresponding_points(
            img=img,
            points_array=points_array,
            points_map=line_map,
            line_color=(0, 0, 255),
        )

    cv2.imshow("Half Face", img)
    cv2.waitKey(0)
    return


if __name__ in "__main__":
    jpeg = sys.argv[1]
    assert "annotated" in jpeg, "Please use an image annotated with landmarks."
    fname_jpeg = Path(jpeg)

    sfx = fname_jpeg.suffix
    npy = jpeg.replace("img", "landmarks")
    fname_npy = Path(npy.replace(sfx, ".npy"))

    a = cv2.imread(fname_jpeg.as_posix())
    arr = np.load(fname_npy.as_posix())

    # add example horizontal lines
    # to see where these points are coming from, view here:
    # https://ibug.doc.ic.ac.uk/media/uploads/images/annotpics/figure_68_markup.jpg
    mask = get_mask_outline(a, LEFT_HALF_OUTLINE_LANDMARKS, arr, fname="left_mask.jpeg")

    # create_bounding box
    top_y_idx = np.where(np.argmax(mask, 1) > 0)[0][0]
    bottom_y_idx = np.where(np.argmax(mask, 1) > 0)[0][-1]
    left_most_x_idx = np.where(np.argmax(mask, 0) > 0)[0][0]
    right_most_x_idx = np.where(np.argmax(mask, 0) > 0)[0][-1]

    tl = (left_most_x_idx, top_y_idx)
    tr = (right_most_x_idx, top_y_idx)
    bl = (left_most_x_idx, bottom_y_idx)
    br = (right_most_x_idx, bottom_y_idx)

    y_diff = bottom_y_idx - top_y_idx
    x_diff = right_most_x_idx - left_most_x_idx

    box = mask[top_y_idx:bottom_y_idx, left_most_x_idx:right_most_x_idx]
    cv2.imwrite("box.jpeg", box)

    bx = box.copy()
    bx = cv2.flip(bx, 1)

    mask[
        top_y_idx:bottom_y_idx, right_most_x_idx + 1 : right_most_x_idx + 1 + x_diff
    ] = bx
    cv2.imwrite("flip_mask.jpeg", mask)

    # cv2.line(mask, tl, tr, (255, 255, 255), 1)
    # cv2.line(mask, tl, bl, (255, 255, 255), 1)
    # cv2.line(mask, br, tr, (255, 255, 255), 1)
    # cv2.line(mask, bl, br, (255, 255, 255), 1)

    aa = a.copy()
    masked = aa * mask[..., None] * mask[..., None]
    masked = masked.astype(np.uint8)

    cv2.imshow("Mirrored face", masked)
    cv2.waitKey(0)

    construct_half_face(
        a,
        arr,
        points_map=SYMMETRY_MAP,
        line_map=None,
        line_color=(0, 255, 255),
    )
