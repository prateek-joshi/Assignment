import argparse
from util import drawPolygons, drawPolygonsWithClasses

parser = argparse.ArgumentParser(description='Application to visualize damaged areas on vehicle images')
parser.add_argument('-f', '--imgpath', help='Path to the image file', required=True)
parser.add_argument('-j', '--jsonpath', help='Path to JSON metadata file', required=True)
parser.add_argument('-o', '--opacity', help='Opacity of plotted visuals', required=False, default=0.6)

args = parser.parse_args()
img_path = args.imgpath
json_path = args.jsonpath
opacity = float(args.opacity)

if __name__=='__main__':
    drawPolygons(img_path, json_path)
    drawPolygonsWithClasses(img_path, json_path, opacity)