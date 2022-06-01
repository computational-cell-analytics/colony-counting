import os
from glob import glob

import imageio
import numpy as np
from tqdm import trange
from pycocotools.coco import COCO


def view_in_napari(coco, file_path, annotations):
    import napari

    bounding_boxes = []
    for ann in annotations:
        bbox = ann["bbox"]
        # coco bounding box format is x0, y0, width, height
        # napari format is [x0, y0], [x1 = x0 + widht, y1 = y1 + height]
        bounding_boxes.append(
            np.array([
                [bbox[1], bbox[0]],
                [bbox[1] + bbox[3], bbox[0] + bbox[2]]
            ])
        )

    image = imageio.imread(file_path)

    v = napari.Viewer()
    v.add_image(image)
    v.add_shapes(bounding_boxes,
                 shape_type="rectangle",
                 edge_width=4,
                 edge_color="coral",
                 face_color="transparent")
    napari.run()


def main(view=False):
    folder = "/home/pape/Work/data/bacterial-colony-counting/test"

    annotations = os.path.join(folder, "_annotations.coco.json")
    coco = COCO(annotations)
    category_ids = coco.getCatIds()
    n_images = len(glob(os.path.join(folder, "*.jpg")))
    print("Number of images", n_images)

    for image_id in trange(n_images):
        image_metadata = coco.loadImgs(image_id)[0]
        file_name = image_metadata["file_name"]
        file_path = os.path.join(folder, file_name)
        assert os.path.exists(file_path), file_path

        annotation_ids = coco.getAnnIds(imgIds=image_metadata["id"], catIds=category_ids)
        if len(annotation_ids) == 0:
            print("No annotations for image", image_id)
            continue
        annotations = coco.loadAnns(annotation_ids)
        if view:
            view_in_napari(coco, file_path, annotations)


if __name__ == "__main__":
    main(view=True)
