__author__ = 'vfdev'

# Python
import argparse
import os, sys
import shutil
import subprocess
import json
from path import Path
from tqdm import tqdm
# Opencv
import cv2

parser = argparse.ArgumentParser(description="Video2Frames converter")
parser.add_argument('--input', default='/home/roit/datasets/c302', help="Input video file")
#parser.add_argument('--input', default='../data', help="Input video file")

parser.add_argument('--output', default="out_frames", help="Output folder. If exists it will be removed")
parser.add_argument('--maxframes', type=int, default=None, help="Output max number of frames")
parser.add_argument('--verbose', default=True, action='store_true', help="Enable verbose")
parser.add_argument('--skipDelta',default=5)
parser.add_argument('--videos2frames_log',default='./videos2frames_log.txt')


args = parser.parse_args()

def main():
    global args


    in_path = Path(args.input)



    if not in_path.exists():
        parser.error("Input video file is not found")
        return 1
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path('scences_frame')

    out_path.makedirs_p()

    seqs = open(args.videos2frames_log)
    seq_names = []
    for line in seqs:
        if line[0] != '#':
            seq_names.append(line.strip('\n'))
    seq_names.sort()
    print('处理场景{}个\n'.format(len(seq_names)))

    cap = cv2.VideoCapture()
    print('get {} sences'.format(len(in_path.files())))
    in_path.files('*.mp4').sort()
    files = in_path.files('*.mp4')
    for file in tqdm(files):
        if file.stem not in seq_names:
            continue
        cap.open(file)
        if not cap.isOpened():
            parser.error("Failed to open input video {}".format(file))
            continue
        (out_path/file.stem).makedirs_p()

        frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)#视频最大能切分几张


        skipDelta = 0
        frameId = 0

        if args.skipDelta:
            skipDelta = args.skipDelta
        else:
            maxframes = args.maxframes
            skipDelta = int(frameCount / maxframes)  # 乡下取证





    #main cycle
    #while frameId < frameCount:
        f_cnt = 1#output num of frames

        con_list = []


        while len(con_list) <maxframes:
            frameId+=skipDelta
            con_list.append(frameId)



        #while frameId < frameCount:
        for frameId in tqdm(con_list):
            ret, frame = cap.read()
            # print frameId, ret, frame.shape
            if not ret:
                print("Failed to get the frame {f}".format(f=frameId))
                continue

            # Rotate if needed:

            ofname = out_path / file.stem / '{:0>7}.png'.format(f_cnt)  # 补零操作

            if file.stem[-2:]=='_d':#如果为深度图文件， 保存为单通道灰度图
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            ret = cv2.imwrite(ofname, frame)
            if not ret:
                print("Failed to write the frame {f}".format(f=frameId))
                continue

            cap.set(cv2.CAP_PROP_POS_FRAMES, frameId)
            f_cnt += 1

        f_cnt = 1
        frameId = 0


    #post precess
    print('\n Over')
    return 0




if __name__ == "__main__":
    print("Start Video2Frames script ...")
    ret = main()
    exit(ret)

