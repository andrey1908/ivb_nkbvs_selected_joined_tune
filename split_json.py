import json
import numpy as np


def get_annotations(images, annotations):
    new_annotations = list()
    images_ids = set()
    for image in images:
        images_ids.add(image['id'])
    ann_id = 1
    for annotation in annotations:
        if annotation['image_id'] in images_ids:
            annotation['id'] = ann_id
            new_annotations.append(annotation)
            ann_id += 1
    return new_annotations


def split_json(json_file, train_rate):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)
    images_num = len(json_dict['images'])
    train_images_num = int(images_num * train_rate)
    np.random.shuffle(json_dict['images'])
    train_images = json_dict['images'][:train_images_num]
    val_images = json_dict['images'][train_images_num:]
    train_annotations = get_annotations(train_images, json_dict['annotations'])
    val_annotations = get_annotations(val_images, json_dict['annotations'])
    train_json = {'images': train_images, 'annotations': train_annotations, 'categories': json_dict['categories']}
    val_json = {'images': val_images, 'annotations': val_annotations, 'categories': json_dict['categories']}
    with open('_train.json', 'w') as f:
        json.dump(train_json, f)
    with open('_val.json', 'w') as f:
        json.dump(val_json, f)


if __name__ == '__main__':
    split_json('ann.json', 0.535)

