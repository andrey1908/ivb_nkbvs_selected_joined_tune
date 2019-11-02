import json


coco_classes = ('person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', # 6
               'train', 'truck', 'boat', 'traffic_light', 'fire_hydrant', # 11
               'stop_sign', 'parking_meter', 'bench', 'bird', 'cat', 'dog',
               'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
               'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
               'skis', 'snowboard', 'sports_ball', 'kite', 'baseball_bat',
               'baseball_glove', 'skateboard', 'surfboard', 'tennis_racket',
               'bottle', 'wine_glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
               'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
               'hot_dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
               'potted_plant', 'bed', 'dining_table', 'toilet', 'tv', 'laptop',
               'mouse', 'remote', 'keyboard', 'cell_phone', 'microwave',
               'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
               'vase', 'scissors', 'teddy_bear', 'hair_drier', 'toothbrush')


# stop_sign -> traffic_sign
new_classes = ('person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', # 6
               'train', 'truck', 'boat', 'traffic_light', 'fire_hydrant', # 11
               'traffic_sign', 'parking_meter', 'bench', 'bird', 'cat', 'dog',
               'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
               'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
               'skis', 'snowboard', 'sports_ball', 'kite', 'baseball_bat',
               'baseball_glove', 'skateboard', 'surfboard', 'tennis_racket',
               'bottle', 'wine_glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
               'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
               'hot_dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
               'potted_plant', 'bed', 'dining_table', 'toilet', 'tv', 'laptop',
               'mouse', 'remote', 'keyboard', 'cell_phone', 'microwave',
               'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
               'vase', 'scissors', 'teddy_bear', 'hair_drier', 'toothbrush')


def classes_list_to_categories(classes):
    categories = list()
    cat_id = 1
    for cl in classes:
        category = {'name': cl, 'id': cat_id}
        categories.append(category)
        cat_id += 1
    return categories


def get_new_categories(old_categories):
    new_categories = classes_list_to_categories(new_classes)
    old_category_name_to_new_id = {'traffic_sign': 12, 'car': 3, 'truck': 8, 'person': 1, 'traffic_light': 10}
    old_category_id_to_new = dict()
    for old_category in old_categories:
        if old_category['name'] in old_category_name_to_new_id.keys():
            old_category_id_to_new[old_category['id']] = old_category_name_to_new_id[old_category['name']]
    return new_categories, old_category_id_to_new


def get_new_annotations(annotations, old_category_id_to_new, start_id=1):
    new_annotations = list()
    used_images_id = set()
    idx = start_id
    for annotation in annotations:
        if annotation['category_id'] not in old_category_id_to_new.keys():
            continue
        annotation['category_id'] = old_category_id_to_new[annotation['category_id']]
        annotation['id'] = idx
        new_annotations.append(annotation)
        used_images_id.add(annotation['image_id'])
        idx += 1
    return new_annotations, used_images_id


def get_new_images(images, used_images_id, start_id=0):
    new_images = list()
    old_image_id_to_new = dict()
    idx = start_id
    for image in images:
        if image['id'] not in used_images_id:
            # continue
            pass
        old_image_id_to_new[image['id']] = idx
        image['id'] = idx
        new_images.append(image)
        idx += 1
    return new_images, old_image_id_to_new


def correct_for_training(coco_file, out_file):
    with open(coco_file, 'r') as f:
        json_dict = json.load(f)
    images = json_dict['images']
    annotations = json_dict['annotations']
    categories = json_dict['categories']

    categories, old_category_id_to_new = get_new_categories(categories)
    annotations, used_images_id = get_new_annotations(annotations, old_category_id_to_new)
    images, old_image_id_to_new = get_new_images(images, used_images_id)
    for annotation in annotations:
        annotation['image_id'] = old_image_id_to_new[annotation['image_id']]

    json_dict = {'images': images, 'annotations': annotations, 'categories': categories}
    with open(out_file, 'w') as f:
        json.dump(json_dict, f)


if __name__ == '__main__':
    correct_for_training('_train.json', 'train.json')
    correct_for_training('_val.json', 'val.json')

