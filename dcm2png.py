import argparse
import sys
from pathlib import Path
from typing import Tuple

from pydicom import dcmread
from PIL import Image
from rich.progress import track


def get_args() -> Tuple[Path, Path, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dcm-dir', type=str, help='a path to a directory to search for dcm files recursively', required=True)
    parser.add_argument('--png-dir', type=str, help='a path to a directory to output png files', required=True)
    parser.add_argument('--stem-suffix', type=str, help='a suffix of filename added to output png files', default="OUT")
    args = parser.parse_args()

    dcm_dir = Path(args.dcm_dir)
    assert dcm_dir.is_dir()
    png_dir = Path(args.png_dir)
    assert png_dir.is_dir()
    return (dcm_dir, png_dir, args.stem_suffix)


def dcm2png(dcm_path: Path, png_dir: Path, stem_suffix: str) -> Path | None:
    dataset = dcmread(str(dcm_path))
    if not ("PixelData" in dataset):
        return None

    # cf. https://github.com/pydicom/pylibjpeg-libjpeg/issues/29
    dataset.PhotometricInterpretation = "YBR_FULL"
    image = Image.fromarray(dataset.pixel_array)  # type: ignore

    patient_id: str = dataset.PatientID if "PatientID" in dataset else ""
    study_date: str = (
        dataset.StudyDate
        if "StudyDate" in dataset
        else ""
    )
    study_time: str = (
        dataset.StudyTime
        if "StudyTime" in dataset
        else ""
    )
    instance_number: int = int(
        dataset.InstanceNumber
        if "InstanceNumber" in dataset
        else ""
    )
    image_laterality: str = (
        dataset.ImageLaterality
        if "ImageLaterality" in dataset and dataset.ImageLaterality in "LR"
        else ""
    )
    png_path = png_dir / f"{patient_id}_{study_date}_{study_time}_{instance_number}_{image_laterality}_{stem_suffix}.png"
    image.save(png_path, format="png")

    return png_path


def main(dcm_dir: Path, png_dir: Path, stem_suffix: str) -> None:
    dcm_files = list(dcm_dir.glob('**/*.dcm'))
    for idx, dcm_path in track(enumerate(dcm_files), description="Converting dcm to png ..."):
        try:
            png_path = dcm2png(dcm_path, png_dir, stem_suffix)
        except Exception as e:
            print(f"{idx+1:^8d}/{len(dcm_files):^8d}: !!! unexpected error on {str(dcm_path)}: no PixelArray found in DICOM !!!", file=sys.stderr)
        if png_path is None:
            print(f"{idx+1:^8d}/{len(dcm_files):^8d}: !!! failed to convert {str(dcm_path)}: no PixelArray found in DICOM !!!", file=sys.stderr)
            continue
        print(f"{idx+1:^8d}/{len(dcm_files):^8d}: converted {str(dcm_path)} to {str(png_path)} ...", file=sys.stderr)


if __name__ == "__main__":
    main(*get_args())
