# json/coco utils for Unity
# lessw2020
# https://github.com/lessw2020/perception_tools

from pathlib import Path, PurePath
import json
from copy import deepcopy
import os
from datetime import datetime as dt


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
    anno_file = dataset_dir / 'annotation_definitions.json'
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
    anno_list = fh['annotation_definitions']
    spec = anno_list[0]
    spec = spec['spec']
    print(f"\n--> labels in perception definitions:\n")
    for item in spec:
        print(item)

    print(f"\n-->building coco categories:")
    coco_category_block = []
    for item in spec:
        holding = {}
        holding['id'] = item['label_id']

        holding['name'] = item['label_name']
        holding['supercategory'] = supercategory
        print(holding)
        coco_category_block.append(holding)
    return coco_category_block


def get_perception_annotations(anno_dir, image_width=1024, image_height=768):
    anno_id = 0  # can also start with 1 if desired
    image_id = 0

    images_block = []
    annos_block = []

    capture_files = anno_dir.glob('captures*.json')

    for j, _ in enumerate(capture_files):
        pass

    print(f"\n--> {j + 1} capture files detected. Processing...")

    # processing
    capture_files = anno_dir.glob('captures*.json')

    for item in capture_files:

        fh = open_json(item)

        captures = fh['captures']

        for image_entry in captures:
            image_dict = {}

            image_dict['id'] = image_id

            fp = Path(image_entry['filename'])

            # it's likely you are exporting all images as same size.
            # could open each image and check height/width, but will use passed in args for now
            image_dict['width'] = image_width
            image_dict['height'] = image_height
            image_dict['file_name'] = fp.name

            # dummy values
            image_dict['license'] = None
            image_dict['flickr_url'] = ""
            image_dict['coco_url'] = ""
            image_dict['date_captured'] = "0:00"

            images_block.append(deepcopy(image_dict))

            annos = image_entry['annotations']

            ad = {}

            for a in annos:
                ad.update(a)

            values = ad['values']

            coco_anno = []

            for item in values:
                temp_anno = {}
                x = item['x']
                y = item['y']
                w = item['width']
                h = item['height']

                bbox = [x, y, w, h]

                temp_anno["id"] = anno_id
                temp_anno["image_id"] = image_id
                temp_anno["category_id"] = item["label_id"]

                # bbox details
                temp_anno["bbox"] = bbox
                temp_anno["area"] = int(w * h)

                # segmentation - todo if needed
                temp_anno["segmentation"] = None
                temp_anno["iscrowd"] = 0

                annos_block.append(deepcopy(temp_anno))

                anno_id += 1

            image_id += 1

    print(f"--> annotation processing completed.")
    return images_block, annos_block


def convert_perception(base_dir, out_file="coco_labels.json", image_width=1024, image_height=768):
    """
    main entry for converting perception output into ready to train coco file

    note - currently image height and width are passed in /hardcoded.  Workaround is can open every image file
    and check, or update perception to export image info...for now just using passed in vars

    """

    image_dir, dataset_dir = get_sub_folders(base_dir)

    mainfile = {}

    # build info section
    infod = {}

    today = dt.today()
    infod['year'] = str(today.year)
    infod['date_created'] = str(today)

    infod['version'] = "1.0"
    infod['contributor'] = "lessw2020"
    infod['url'] = 'https://github.com/lessw2020/perception_tools'

    mainfile['info'] = infod

    mainfile['licenses'] = []

    # get categories
    perception_anno = get_anno_file(dataset_dir)

    coco_cats = get_perception_categories(perception_anno)

    mainfile['categories'] = coco_cats

    # print(f"--> mainfile = {mainfile}")

    # get annotations
    images_block, annos_block = get_perception_annotations(dataset_dir,
                                                           image_width, image_height)

    mainfile['images'] = images_block
    mainfile['annotations'] = annos_block

    if out_file:
        save_file = dataset_dir / out_file
        with open(save_file, 'w') as fh:
            json.dump(mainfile, fh)

    # all done
    print(f"\n--> Processing complete.  Total images = {len(mainfile['images'])}\n")

    return mainfile
