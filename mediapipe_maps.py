"""https://github.com/google/mediapipe/blob/a908d668c730da128dfa8d9f6bd25d519d006692/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png"""

from mediapipe.python.solutions.drawing_utils import DrawingSpec
from mediapipe.python.solutions.face_mesh import FACEMESH_TESSELATION

SYMMETRY_SPEC = DrawingSpec(color=(48, 255, 255), thickness=2, circle_radius=2)

IDX_SET = {
    10,
    151,
    9,
    8,
    168,
    6,
    197,
    195,
    5,
    4,
    1,
    19,
    94,
    2,
    164,
    0,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    200,
    199,
    175,
    152,
}


CUSTOM_CONTOURS_GRAPH = frozenset(
    {
        (10, 151),
        (151, 9),
        (9, 8),
        (8, 168),
        (168, 6),
        (6, 197),
        (197, 195),
        (195, 5),
        (5, 4),
        (4, 1),
        (19, 94),
        (94, 2),
        (2, 164),
        (164, 0),
        (0, 11),
        (11, 12),
        (12, 13),
        (13, 14),
        (14, 15),
        (15, 16),
        (16, 17),
        (17, 18),
        (18, 200),
        (200, 199),
        (199, 175),
        (175, 152),
    }
)
