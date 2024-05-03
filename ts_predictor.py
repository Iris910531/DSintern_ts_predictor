import argparse
import time
from pathlib import Path

from postprocess import Postprocess
from predict import Predict
from preprocess import Preprocess


def main(arg):
    
    # preprocess
    SG , nan_SG, timeString = Preprocess(args.timestamp)

    # predict
    forecast, gt = Predict(timeString, SG, nan_SG)

    # postprocess
    Postprocess(args.output_file, forecast, gt)

    # check
    assert Path(arg.output_file).is_file()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Time Series Predictor')
    parser.add_argument('--output_file', type=str, help='Output CSV file')
    parser.add_argument('--timestamp', type=int, help='timestamp for prediction')
    args = parser.parse_args()
    main(args)