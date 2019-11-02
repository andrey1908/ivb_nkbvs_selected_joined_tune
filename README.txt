PURPOSE:
Fine-tune pre-trained on coco dataset model on our dataset (cvat ivb_nkbvs_selected_joined).

FILES:
ann.json - our annotations converted into coco (cvat2coco.py).
split_json.py - split ann.json into _train.json and _val.json.
correct_for_training.py - correct categories in _train.json and _val.json, and save it in train.json and val.json.

USEAGE:
1. Dump annotations from cvat ivb_nkbvs_selected_joined. Call it ann.xml.
2. Convert ann.xml to ann.json with cvat2coco.py.
3. Use split_json.py to split ann.json into _train.json and _val.json.
4. Use correct_for_training.py to extend categories to 80 (as in coco) in _train.json and _val.json, and save it in train.json and val.json.
5. Fune-tune model, using train.json and val.json as annotations.

