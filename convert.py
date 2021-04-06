import argparse
import csv
import glob
import os
import time
from os.path import join


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

def main():
    global total
    parser = argparse.ArgumentParser(description='YOLOv4 to AutoML: Convert the YOLOv4 Darknet format txt files to AutoML csv format for Cloud AutoML Vision Object Detection.')
    parser.add_argument('yolo_txts_path', help='Path to your YOLO folder with the all the .txt (e.g. ./labels/)', type=dir_path)
    parser.add_argument('gs_path', help='Base path to location of the images in the gs. (e.g. gs://dataset/cars/images/)')
    parser.add_argument('label', help='Label name. (e.g. car)')
    parser.add_argument('-o', '--output', default='output.csv', help='Output file name. (default: output.csv)')

    args = parser.parse_args()

    # only to make sure gs path ends with /
    gs_path = args.gs_path if args.gs_path.endswith('/') else f'{args.gs_path}/'

    final = []
    yolo_lines = []
    automl_lines = []
    output_lines = []
    for file in glob.glob(os.path.join(args.yolo_txts_path, '*.txt')):
        with open(file, 'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                yolo_lines.append(convert(line))
                # final should be "UNASSIGNED,gs://dataset/cars/images/0001.jpg,,,,,,,,,""
                final.append(f'UNASSIGNED,{gs_path}{os.path.basename(file.removesuffix(".txt"))}.jpg,,,,,,,,,')

    # This could be simplified with the loop above, but...
    for i, line in enumerate(yolo_lines):
        spl = final[i].split(',')
        output_line = [spl[0], spl[1], args.label]
        for value in line.split(','):
            output_line.append(value)
        output_lines.append(output_line)

    try:
        export2csv(output_lines, args.output)
    except BaseException as e:
        print('Failed to export to csv:', e)
        exit(1)

    total = len(output_lines)

def convert(line: str) -> str:
    # YOLOv4 format: 1 0.365234 0.541016 0.386719 0.847656
    # AutoML format: TRAIN,gs://cloud-ml-data/img/openimage/2851/11476419305_7b73a0128c_o.jpg,Baked goods,0.56,0.25,0.97,0.25,0.97,0.50,0.56,0.50

    _, x, y, w, h = line.split(' ')
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    return f'{round(float(x - w / 2), 2)},{round(float(y - h / 2), 2)}, {round(float(x + w / 2), 2)}, {round(float(y - h / 2), 2)}, {round(float(x + w / 2), 2)}, {round(float(y + h / 2), 2)}, {round(float(x - w / 2), 2)}, {round(float(y + h / 2), 2)}'


def export2csv(output_lines: list, filename: str):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output_lines)


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Done in {(end - start) * 1000.0} ms. {total} files processed.")
    

