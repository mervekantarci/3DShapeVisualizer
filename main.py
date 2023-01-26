import argparse
from os import path
from visualizer import Visualizer


def float_0010(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("%r not a floating-point literal" % x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]" % x)
    return x


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir', required=False, action="store", type=str,
                        help='directory shape files are in (do not set this if you want to visualize single file)')
    parser.add_argument('--file', required=False, action="store", type=str,
                        help='path to input file (set this to visualize single file)')
    parser.add_argument('--out_dir', required=False, action="store", type=str,
                        help="directory to save figure images (default is 'output' in the working directory)")
    parser.add_argument('--save', required=False, action="store_true", default=False,
                        help='if plot should be saved')
    parser.add_argument('--show', required=False, action="store_true", default=False,
                        help='if plot should be displayed')
    parser.add_argument('--verbose', required=False, action="store_true", default=False,
                        help='print output paths')
    parser.add_argument('--skip', required=False, action="store_true", default=False,
                        help='skip file when there is a file with the same name in the destination dir'
                             '(useful when visualizing many files and the process is corrupted)')
    parser.add_argument('--skip_verbose', required=False, action="store_true", default=False,
                        help='print path to skipped file')
    parser.add_argument('--th', required=False, action="store", type=float_0010, default="0.3",
                        help='voxelization threshold for npy files  (float between 0.0 and 1.0)')
    parser.add_argument('--r', required=False, action="store", type=float_0010, default="0.7",
                        help='blue value of shape color (float between 0.0 and 1.0)')
    parser.add_argument('--g', required=False, action="store", type=float_0010, default="0.7",
                        help='blue value of shape color (float between 0.0 and 1.0)')
    parser.add_argument('--b', required=False, action="store", type=float_0010, default="0.7",
                        help='blue value of shape color (float between 0.0 and 1.0)')

    args_ = parser.parse_args()
    return args_


if __name__ == '__main__':
    args = get_args()
    print(args)

    if not args.show and not args.save:
        print("WARNING! You should use --show to display shapes and/or --save to store visualized plots."
              "\nYour current setting will output nothing.")

    if args.file is None and args.in_dir is None:
        raise Exception("You should specify a directory or a file path to visualize!")
    else:
        visualizer = Visualizer(args)
        if args.in_dir is not None:
            if not path.exists(args.in_dir):
                raise Exception("No such directory %s" % args.in_dir)
            print("Working directory: %s" % args.in_dir)
            visualizer.visualize_directory()
        else:
            visualizer.visualize_single_file()




