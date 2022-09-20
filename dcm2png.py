import argparse
import sys
from pathlib import Path
from typing import Tuple

from pydicom import dcmread
from PIL import Image
from rich.progress import track


def get_args() -> Tuple[Path, Path]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dcm-dir', type=str, help='a path to a directory to search for dcm files recursively', required=True)
    parser.add_argument('--png-dir', type=str, help='a path to a directory to output png files', required=True)
    args = parser.parse_args()

    dcm_dir = Path(args.dcm_dir)
    assert dcm_dir.is_dir()
    png_dir = Path(args.png_dir)
    assert png_dir.is_dir()
    return (dcm_dir, png_dir)


def dcm2png(dcm_path: Path, png_path: Path) -> None:
    # dicom を読み取り、画像部を PIL.Image に変換
    dataset = dcmread(str(dcm_path))
    # cf. https://github.com/pydicom/pylibjpeg-libjpeg/issues/29
    dataset.PhotometricInterpretation = "YBR_FULL"
    image = Image.fromarray(dataset.pixel_array)  # type: ignore
    image.save(png_path, format="png")



def main(dcm_dir: Path, png_dir: Path) -> None:
    dcm_files = list(dcm_dir.glob('**/*.dcm'))
    for idx, dcm_path in track(enumerate(dcm_files)):
        filename = dcm_path.name
        png_path = (png_dir / filename).with_suffix('.png')
        print(f"{idx+1:^8d}/{len(dcm_files):^8d}: converting {str(dcm_path)} to {str(png_path)} ...", file=sys.stderr)
        dcm2png(dcm_path, png_path)


if __name__ == "__main__":
    main(*get_args())
