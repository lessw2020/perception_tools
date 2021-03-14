
# lessw2020 - perception to coco convertor

from pathlib import Path
import json
from copy import deepcopy
import os

#perception_folder = "C:/Users/lessw/AppData/LocalLow/main_synthetic/main_generator/26cd1c73-4631-4b67-bfb1-9726d23d8de6"

from pathlib import Path, PurePath

def require_dir(item, type="Dataset"):
    itemp = Path(item)
    if not itemp.is_dir():
        raise ValueError(f"directory of type {type} not found. aborting...")

def get_sub_folders(upper_path):
    # verify upper path
    fpath = Path(upper_path)

    require_dir(fpath, "Perception root dir")  # will break with raise error if not dir

    # get required subfolders
    # dataset
    # subdirs = [f.path for f in os.scandir(upper_path) if f.is_dir() ]

    dataset_glob = fpath.glob("Dataset*")
    try:
        dataset_dir = next(dataset_glob)
    except StopIteration:
        print(f"** failed to get Dataset dir. aborting..")
        return None, None

    require_dir(dataset_dir, "Dataset")

    print(f"--> using {dataset_dir.name} to generate annotations")

    image_glob = fpath.glob("RGB*")

    try:
        image_dir = next(image_glob)
    except StopIteration:
        print(f"** failed to get an image dir. aborting...")
        return None, None

    print(f"--> using {image_dir.name} for images")

    return image_dir, dataset_dir


def get_anno_file(dataset_dir):
    anno_file = dataset_dir / "annotation_definitions.json"
    return anno_file


def open_json(fpath):
    try:
        with open(str(fpath)) as f:
            jh = json.load(f)
    except:
        raise ValueError(f"failed to open {fpath} for read")
    return jh


def get_perception_categories(anno_file, show_info=True, supercategory="rdt"):

    fh = open_json(anno_file)
    anno_list = fh["annotation_definitions"]
    spec = anno_list[0]
    spec = spec["spec"]
    print(f"\n--> labels in perception definitions:\n")
    for item in spec:
        print(item)

    print(f"\n-->building coco categories:")
    coco_category_block = []
    for item in spec:
        holding = {}
        holding["id"] = item["label_id"]

        holding["name"] = item["label_name"]
        holding["supercategory"] = supercategory
        print(holding)
        coco_category_block.append(holding)
    return coco_category_block


def get_perception_annotations(anno_dir):

    anno_id = 0
    image_id = 0

    capture_files = anno_dir.glob("captures*.json")

    for i, item in enumerate(capture_files):
        pass
    print(f"\n-->{i+1} capture files detected. Processing...")


def convert_perception(base_dir, out_file="coco_labels.json"):

    image_dir, dataset_dir = get_sub_folders(base_dir)

    # get categories
    perception_anno = get_anno_file(dataset_dir)

    coco_cats = get_perception_categories(perception_anno)

    # get annotations
    z = get_perception_annotations(dataset_dir)
