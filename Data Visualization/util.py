import json
import cv2
import numpy as np
import random
import os

def load_json(json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception:
        print(f'Could not load json file - {json_path}')

def denormalizeCoords(coords, width, height):
    for coord in coords:
        coord[0] = (coord[0]*width)/100
        coord[1] = (coord[1]*height)/100

    return coords

def getClassCoords(json_path):
    data = load_json(json_path)
    img_height, img_width = None, None
    items = []
    for item in data:
        if item['type'] == 'polygonlabels':
            img_width = item['original_width']
            img_height = item['original_height']

            coords = denormalizeCoords(np.array(item['value']['points'], dtype=np.int32), img_width, img_height)
            label = item['value']['polygonlabels']
            items.append((coords, label))

    return items

def drawPolygons(img_path, json_path):
    items = getClassCoords(json_path)
    img = cv2.imread(img_path)

    for item in items:
        color = (random.randrange(0, 256),random.randrange(0, 256),random.randrange(0, 256))
        
        # perimeter = cv2.arcLength(item[0], closed=True)
        # epsilon = 0.0001*perimeter
        # approx = cv2.approxPolyDP(item[0], epsilon, closed=True)

        cv2.polylines(img, [item[0]], isClosed=True, thickness=2, color=color)
        # cv2.polylines(img, [approx], isClosed=True, thickness=2, color=color)

    img_file = img_path.split('\\')[-1]
    save_path = img_file.split('.')[0] + '-type-1.' + img_file.split('.')[-1]
    # print(save_path)

    cv2.imwrite(os.path.join('Data Visualization','images',save_path), img)
    # cv2.imshow('defects', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__=='__main__':
    img_path = 'D:\\Projects\\Assignment\\Data Visualization\\images\\1.jpg'
    json_path = 'D:\\Projects\\Assignment\\Data Visualization\\data\\1.json'

    drawPolygons(img_path, json_path)