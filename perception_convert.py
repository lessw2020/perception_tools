# lessw2020 - perception to coco convertor

from pathlib import Path, PurePath


def require_dir(item, type="Dataset"):
    itemp = Path(item)
    if not itemp.is_dir():
        raise ValueError(f"directory of type {type} not found. aborting...")


def get_subfolders(upper_path):
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