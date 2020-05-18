

import argparse


def parse_args_generate_splits():
    parser = argparse.ArgumentParser(
        description='Simple testing funtion for Monodepthv2 models.')

    parser.add_argument('--dataset_path', type=str,default='/home/roit/datasets/MC',help='path to a test image or folder of images')
    parser.add_argument("--txt_style",default='mc',choices=['mc','visdrone'])
    parser.add_argument('--out_path', type=str,default=None,help='path to a test image or folder of images')
    parser.add_argument("--num",default=100,type=str)
    parser.add_argument("--proportion",default=[0.7,0.2,0.1],help="train, val, test")
    parser.add_argument("--out_name",default=None)

    return parser.parse_args()

def parse_args_main():
    parser = argparse.ArgumentParser(description='main')
    parser.add_argument("--txt_path",default='histc_dirs.txt')
    parser.add_argument("--depth_txt_path",default='depth_map_dirs.txt')


    return parser.parse_args()