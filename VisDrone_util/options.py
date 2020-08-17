
import argparse

class VisDrone_opts:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Simple testing funtion for Monodepthv2 models.')

        self.parser.add_argument('--dataset_path', type=str,
                             default='/home/roit/datasets/VSD2',
                            help='path to a test image or folder of images')


        self.parser.add_argument('--splits', default='visdrone_lite',choices=['visdrone_lite','visdrone_lite'])
        self.parser.add_argument("--wk_root",default='/home/roit/aws/utils/VisDrone_util')

        self.parser.add_argument("--full_height", type=int,
                                 default=1071)
        self.parser.add_argument("--full_width", type=int,
                                 default=1904)
        self.parser.add_argument("--height", type=int, help="input image height", default=192)
        self.parser.add_argument("--width", type=int, help="input image width", default=352)
        self.parser.add_argument("--frame_idxs",default=[-1,0,1])
        self.parser.add_argument("--scales",default=[0,1,2,3])

        self.parser.add_argument("--batch_size",default=1)
        self.parser.add_argument("--num_workers",default=1)

        self.parser.add_argument('--model_name', type=str,
                            help='name of a pretrained model to use',
                            default='mono_640x192',
                                 choices=[
                                "last_model",
                                "mono_640x192",
                                "stereo_640x192",
                                "mono+stereo_640x192",
                                "mono_no_pt_640x192",
                                "stereo_no_pt_640x192",
                                "mono+stereo_no_pt_640x192",
                                "mono_1024x320",
                                "stereo_1024x320",
                                "mono+stereo_1024x320"])
        self.parser.add_argument('--model_path', type=str,
                                 default='/home/roit/models/monodepth2_official',
                                 help='root path of models')

    def parse(self):
        self.options = self.parser.parse_args()
        return self.options

class SplitWithFilter_opts:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Simple testing funtion for Monodepthv2 models.')

        self.parser.add_argument('--dataset_path', type=str, default='/home/roit/datasets/VSD2',
                            help='path to a test image or folder of images')
        self.parser.add_argument("--splits", default='visdrone', help='output_dir')
        self.parser.add_argument('--out_path', type=str, default=None, help='path to a test image or folder of images')
        self.parser.add_argument("--num", default=None, type=str)
        self.parser.add_argument("--proportion", default=[0.9, 0.05, 0.05], help="train, val, test")
        self.parser.add_argument("--num_workers", default=12)
        self.parser.add_argument("--batch_size", default=8)
        self.parser.add_argument("--photometric_threshold", default=[0.12,0.30])
        self.parser.add_argument('--frame_idxs', default=[-3, 0, 3],
                            help="frame interval settings")  # 由于有photometric err 控制了, 所以可以将frame interval 减小
        self.parser.add_argument("--photometric_err_dir", default='./photometric_err_VSD2')
        self.parser.add_argument("--ext", default='.jpg')

        self.parser.add_argument("--out_name", default=None)
    def args(self):
        self.options = self.parser.parse_args()
        return self.options
