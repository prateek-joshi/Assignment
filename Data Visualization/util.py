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
            label = item['value']['polygonlabels'][0]
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

        cv2.polylines(img, [item[0]], isClosed=True, thickness=1, color=color)
        # cv2.polylines(img, [approx], isClosed=True, thickness=2, color=color)

    img_file = img_path.split('\\')[-1]
    save_path = img_file.split('.')[0] + '-type-1.' + img_file.split('.')[-1]
    # print(save_path)

    cv2.imwrite(os.path.join('Data Visualization','images',save_path), img)
    # cv2.imshow('defects', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def getBboxCoords(coords):
    # get min and max x, y coords
    xmax, xmin = 0, 10000
    ymax, ymin = 0, 10000

    for point in coords:
        x, y = point[0], point[1]
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y

    return (xmin, ymin), (xmax, ymax)

def drawPolygonsWithClasses(img_path, json_path, opacity):
    # draws the polygons onto a blank canvas and adds it onto the image via a mask.
    # Opacity is controlled by alpha

    items = getClassCoords(json_path)
    img = cv2.imread(img_path)
    blank = np.zeros_like(img, dtype=np.uint8)

    for item in items:
        color = (random.randrange(0, 256),random.randrange(0, 256),random.randrange(0, 256))

        # cv2.polylines(img, [item[0]], isClosed=True, thickness=2, color=color)
        cv2.fillPoly(blank, [item[0]], color=color)
        bbox = getBboxCoords(item[0])
        cv2.rectangle(img, bbox[0], bbox[1], color=color, thickness=1)

    out = img.copy()
    mask = blank.astype(bool)
    alpha = opacity
    out[mask] = cv2.addWeighted(img, alpha, blank, 1 - alpha, 0)[mask]

    # put label in bbox corners
    for item in items:
        # get text size for text background
        # origin at top-left
        bbox = getBboxCoords(item[0])
        text_size, _ = cv2.getTextSize(item[1], cv2.FONT_HERSHEY_PLAIN, 1, 1)
        text_w, text_h = text_size
        rect_start, rect_end = (bbox[0][0], bbox[0][1]), (bbox[0][0]+text_w, bbox[0][1]+text_h)
        cv2.rectangle(out, rect_start, rect_end, (43,43,43), -1)
        cv2.putText(out, item[1], (bbox[0][0]+5, bbox[0][1]+text_h-1), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.5, color=(255,255,255), thickness=1)

    img_file = img_path.split('\\')[-1]
    save_path = img_file.split('.')[0] + '-type-2.' + img_file.split('.')[-1]
    # print(save_path)

    cv2.imwrite(os.path.join('Data Visualization','images',save_path), out)

if __name__=='__main__':
    img_path = 'D:\\Projects\\Assignment\\Data Visualization\\images\\2.jpg'
    json_path = 'D:\\Projects\\Assignment\\Data Visualization\\data\\2.json'
    opacity = 0.5

    drawPolygonsWithClasses(img_path, json_path, opacity)