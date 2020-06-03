

from datasets.visdrone_dataset import VSDataset
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt
from path import Path
from options import  VisDrone_opts



def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return lines




def main(opts):
    fpath = Path(os.path.dirname(__file__))/opts.splits/ "{}_files.txt"
    train_filenames = readlines(fpath.format("train"))
    val_filenames = readlines(fpath.format("val"))

    train_dataset = VSDataset(
        data_path=opts.dataset_path,
        filenames=train_filenames,
        height=opts.height,
        width=opts.width,
        frame_idxs=opts.frame_idxs,
        num_scales=len(opts.scales)
    )

    dataloader = DataLoader(
        dataset=train_dataset,
        batch_size=opts.batch_size,
        shuffle=False,
        num_workers=opts.num_workers,
        pin_memory=True,
        drop_last=True
    )


    for batch_idx,inputs in enumerate(dataloader):
        print('ok')


if __name__=="__main__":
    options = VisDrone_opts()
    opts = options.parse()
    main(opts)