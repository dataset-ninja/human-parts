import os
import shutil
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/Human-Parts/Priv_personpart/Images"
    bboxes_path = "/home/alex/DATASETS/TODO/Human-Parts/Priv_personpart/Annotations"
    batch_size = 30
    im_ext = ".jpg"
    bboxes_ext = ".xml"

    train_names = (
        "/home/alex/DATASETS/TODO/Human-Parts/Priv_personpart/ImageSets/privpersonpart_train.txt"
    )
    val_names = (
        "/home/alex/DATASETS/TODO/Human-Parts/Priv_personpart/ImageSets/privpersonpart_val.txt"
    )

    ds_name_to_anns = {"train": train_names, "val": val_names}

    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        ann_path = image_path.replace("Images", "Annotations").replace(im_ext, bboxes_ext)

        if file_exists(ann_path):
            tree = ET.parse(ann_path)
            root = tree.getroot()

            all_objects = root.findall(".//object")

            for curr_object in all_objects:
                class_name = curr_object.find(".//name").text
                obj_class = meta.get_obj_class(class_name)
                coords_xml = curr_object.findall(".//bndbox")
                for curr_coord in coords_xml:
                    left = float(curr_coord[0].text)
                    top = float(curr_coord[1].text)
                    right = float(curr_coord[2].text)
                    bottom = float(curr_coord[3].text)

                    rect = sly.Rectangle(
                        left=int(left), top=int(top), right=int(right), bottom=int(bottom)
                    )
                    label = sly.Label(rect, obj_class)
                    labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    person = sly.ObjClass("person", sly.Rectangle)
    face = sly.ObjClass("face", sly.Rectangle)
    hand = sly.ObjClass("hand", sly.Rectangle)

    meta = sly.ProjectMeta(
        obj_classes=[person, face, hand],
    )
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, im_names in ds_name_to_anns.items():

        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        with open(im_names) as f:
            images_names = f.read().split("\n")

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [
                os.path.join(dataset_path, im_name + im_ext) for im_name in images_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
