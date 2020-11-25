"""
Example of capturing the HDR image width VideoCaptureEX class
"""
import argparse
import os

import cv2
import numpy as np

import EasyPySpin


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--index", type=int, default=0, help="Camera index (Default: 0)")
    parser.add_argument("-g", "--gain", type=float, default=16.0, help="Gain [dB] (Default: 0)")
    parser.add_argument("--min", type=float, default=50.0, help="Minimum exposure time [us]")
    parser.add_argument("--max", type=float, default=500000.0, help="Maximum exposure time [us]")
    parser.add_argument("-n", "--num", type=int, default=10, help="Number of images to capture")
    parser.add_argument("-o", "--output", type=str, default="capture_hdr.png", help="Output file name (*.exr)")
    parser.add_argument("-a", "--n_ave", type=int, default=1, help="Number of frames per exposure time to average")
    parser.add_argument("-t", "--t_ref", type=float, default=50000.0)
    parser.add_argument("-w", "--weighting", type=str, default="gaussian",
                        help="HDR weighting function (uniform, tent, gaussian, photon, hist_eq)")
    args = parser.parse_args()

    cap = EasyPySpin.VideoCaptureEX(args.index)

    cap.set(cv2.CAP_PROP_GAMMA, 1.0)
    cap.set(cv2.CAP_PROP_GAIN, args.gain)
    cap.average_num = args.n_ave

    print(f"Capturing HDR image from camera {args.index}")
    ret, img_hdr, img_list, t_int = cap.readHDR(args.min, args.max, args.num, t_ref=args.t_ref,
                                                weighting=args.weighting)

    print("Write {}".format(args.output))
    img_hdr = ((2 ** 16 - 1) * ((img_hdr - img_hdr.min()) / img_hdr.ptp())).astype(np.uint16)
    cv2.imwrite(args.output, img_hdr)


if __name__ == "__main__":
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    main()
