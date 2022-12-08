"""Created a symmetry map from point to point such that we can identify which landmarks """

from pathlib import Path
import sys
from typing import Dict, List, Tuple, Union

import cv2
import numpy as np
import matplotlib.pyplot as plt

from maps import BILATERAL_MAP, SYMMETRY_MAP


def draw_equality_line(
    img: np.ndarray, line_map: dict, point_array: np.ndarray
) -> None:
    for k, v in line_map.items():
        top = point_array[k - 1]
        bottom = point_array[v - 1]

        cv2.line(img, top, bottom, (0, 0, 255), 2)
    cv2.imshow("Center Line", img)
    cv2.waitKey(0)


def grab_corresponding_points(
    img: np.ndarray,
    points_array: np.ndarray,
    points_map: Dict[int, int],
    target: Union[int, List[int]],
    line_color: Tuple[int, int, int] = (0, 255, 255),
):
    def __add_point(
        img: np.ndarray,
        points_array: np.ndarray,
        points_map: Dict[int, int],
        target: int,
        line_color: Tuple[int, int, int] = (0, 255, 255),
    ):
        l = target
        r = points_map[l]

        left = points_array[l - 1]
        right = points_array[r - 1]

        cv2.line(img, left, right, line_color, 2)

    img = img.copy()

    if isinstance(target, int):
        __add_point(
            img,
            points_array=points_array,
            points_map=points_map,
            target=target,
            line_color=line_color,
        )

    else:
        for idx in target:
            __add_point(
                img,
                points_array=points_array,
                points_map=points_map,
                target=idx,
                line_color=line_color,
            )

    return img


if __name__ in "__main__":
    jpeg = sys.argv[1]
    assert "annotated" in jpeg
    fname_jpeg = Path(jpeg)

    sfx = fname_jpeg.suffix
    npy = jpeg.replace("img", "landmarks")
    fname_npy = Path(npy.replace(sfx, ".npy"))

    a = cv2.imread(fname_jpeg.as_posix())
    arr = np.load(fname_npy.as_posix())

    # add example horizontal lines
    # to see where these points are coming from, view here:
    # https://ibug.doc.ic.ac.uk/media/uploads/images/annotpics/figure_68_markup.jpg
    targets = [1, 4, 8, 18, 22, 32, 37, 40, 51, 59]
    a = grab_corresponding_points(a, arr, SYMMETRY_MAP, targets)

    draw_equality_line(a, BILATERAL_MAP, arr)

