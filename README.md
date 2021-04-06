# YOLOv4 to AutoML
Convert the YOLOv4 Darknet format txt files to AutoML csv format for Cloud AutoML Vision Object Detection.

Python version 3.7 or higher

Note: only work with one label

Usage:
` python3 convert.py [yolo_txts_path] [gs_path] [label] -o output.csv`

```
YOLOv4 to AutoML: Convert the YOLOv4 Darknet format txt files to AutoML csv format for Cloud AutoML Vision
Object Detection.

positional arguments:
  yolo_txts_path        Path to your YOLO folder with the all the .txt (e.g. ./labels/)
  gs_path               Base path to location of the images in the gs. (e.g. gs://dataset/cars/images/)
  label                 Label name. (e.g. car)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name. (default: output.csv)
```

TODO:
- [ ] Make it work with multiple labels