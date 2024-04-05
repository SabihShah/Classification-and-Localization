import cv2 as cv
import numpy as np
import xml.etree.ElementTree as ET
import os

def resize_images(image_dir, target_size):
    resized_images = []
    image_paths = [img for img in os.listdir(image_dir)]

    for img in image_paths:
        image = cv.imread(os.path.join(image_dir, img))

        height, width = image.shape[:2]
        aspect_ratio = width / height
        if isinstance(target_size, int):
            if width > height:
                new_width = target_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = target_size
                new_width = int(new_height * aspect_ratio)
        else:
            new_width, new_height = target_size
        
        resized_image = cv.resize(image, (new_width, new_height))
        
        resized_images.append(resized_image)

    return resized_images

def parse_annotation(xml_dir):
    annotations = []
    xml_paths = [x for x in os.listdir(xml_dir)]

    for path in xml_paths:
        tree = ET.parse(os.path.join(xml_dir, path))
        root = tree.getroot()
        boxes = []
        labels = []
        for obj in root.findall('object'):
            label = obj.find('name').text
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(label)
            
        annotations.append(list(zip(boxes, labels)))

    return annotations

# Function to resize bounding boxes based on image resizing
def resize_boxes(boxes, original_size, target_size):
    original_height, original_width = original_size
    target_height, target_width = target_size
    width_ratio = target_width / original_width
    height_ratio = target_height / original_height
    resized_boxes = []
    for box in boxes:
        xmin, ymin, xmax, ymax = box
        xmin_resized = int(xmin * width_ratio)
        ymin_resized = int(ymin * height_ratio)
        xmax_resized = int(xmax * width_ratio)
        ymax_resized = int(ymax * height_ratio)
        resized_boxes.append([xmin_resized, ymin_resized, xmax_resized, ymax_resized])
    return resized_boxes


images_dir = r"D:\Deep Learning Models\VOC2012\JPEGImages"
xml_dir = r"D:\Deep Learning Models\VOC2012\Annotations"

resized_images = resize_images(images_dir, (300,300))
annotations = parse_annotation(xml_dir)

print(len(resized_images))
print(len(annotations))
