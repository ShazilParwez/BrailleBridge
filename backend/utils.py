import json
import numpy as np

# Load the mapping dictionary globally
with open("full_alphabet_map.json", "r", encoding="utf-8") as f:
    BRAILLE_MAP = json.load(f)

NUMBER_MAP = {
    'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5',
    'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '0'
}

import torch

def parse_xywh_and_class(boxes: torch.Tensor) -> list:
    if len(boxes) == 0:
        return []
    # copy values from troublesome "boxes" object to numpy array
    new_boxes = np.zeros(boxes.shape)
    new_boxes[:, :4] = boxes.xywh.cpu().numpy()  # first 4 channels are xywh
    new_boxes[:, 4] = boxes.conf.cpu().numpy()  # 5th channel is confidence
    new_boxes[:, 5] = boxes.cls.cpu().numpy()  # 6th channel is class which is last channel

    # sort according to y coordinate
    new_boxes = new_boxes[new_boxes[:, 1].argsort()]

    # find threshold index to break the line
    y_threshold = np.mean(new_boxes[:, 3]) // 2
    boxes_diff = np.diff(new_boxes[:, 1])
    threshold_index = np.where(boxes_diff > y_threshold)[0]

    # cluster according to threshold_index
    boxes_clustered = np.split(new_boxes, threshold_index + 1)
    boxes_return = []
    for cluster in boxes_clustered:
        # sort according to x coordinate
        cluster = cluster[cluster[:, 0].argsort()]
        boxes_return.append(cluster)

    return boxes_return

def convert_to_english(class_names: list) -> str:
    """
    State-aware braille decoder that takes a list of 6-bit binary strings.
    Supports numbers, capitalization, and punctuation.
    """
    result = ""
    is_num_mode = False
    is_caps_mode = False
    
    for bin_code in class_names:
        char = BRAILLE_MAP.get(bin_code, "?")
        
        # State modifiers
        if char == "NUM":
            is_num_mode = True
            continue
        elif char == "CAPS":
            is_caps_mode = True
            continue
            
        # Processing characters based on state
        if is_num_mode:
            if char in NUMBER_MAP:
                result += NUMBER_MAP[char]
            else:
                # In standard Braille, hitting a punctuation or non a-j letter often exits num mode
                # unless it's a period/comma inside a number. We'll exit num mode for safety on non a-j.
                is_num_mode = False
                if is_caps_mode and char.isalpha():
                    result += char.upper()
                    is_caps_mode = False
                else:
                    result += char
        else:
            if is_caps_mode and char.isalpha():
                result += char.upper()
                is_caps_mode = False
            else:
                result += char
                
    return result
