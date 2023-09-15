from concurrent.futures import Future, ProcessPoolExecutor
from pathlib import Path

from pydicom import dcmread
from PIL import Image
from rich.console import Console
from rich.progress import track
import typer

app = typer.Typer(help="Convert DICOM files to PNG files.")
console = Console(stderr=True)


def dcm2png(dcm_path: Path, png_dir: Path, stem_suffix: str) -> Path:
    dataset = dcmread(dcm_path.as_posix())
    if "PixelData" not in dataset:
        raise RuntimeError(f"{dcm_path} has no PixelData")

    # cf. https://github.com/pydicom/pylibjpeg-libjpeg/issues/29
    dataset.PhotometricInterpretation = "YBR_FULL"
    image = Image.fromarray(dataset.pixel_array)  # type: ignore

    patient_id = str(getattr(dataset, "PatientID", ""))
    study_date = str(getattr(dataset, "StudyDate", ""))
    study_time = str(getattr(dataset, "StudyTime", ""))

    instance_number = int(getattr(dataset, "InstanceNumber", -1))
    image_laterality = str(getattr(dataset, "ImageLaterality", ""))
    if image_laterality not in "LR":
        image_laterality = "?"

    png_path = (
        png_dir
        / f"{patient_id}_{study_date}_{study_time}_{instance_number}_{image_laterality}_{stem_suffix}.png"
    )
    image.save(png_path)
    return png_path


def ensure_dir(path: Path, /, *, create_ok: bool = False) -> None:
    if not path.exists():
        if create_ok:
            path.mkdir(parents=True)
            return

        raise RuntimeError(f"{path} is not a directory")

    if not path.is_dir():
        raise RuntimeError(f"{path} is not a directory")


@app.command()
def main(
    dcm_dir: Path = typer.Argument(
        help="a path to a directory to search for dcm files recursively",
    ),
    png_dir: Path = typer.Argument(
        help="a path to a directory to output png files",
    ),
    verbose: bool = typer.Option(
        default=False,
        help="whether to show verbose messages",
    ),
    stem_suffix: str = typer.Option(
        default="out",
        help="a suffix of filename added to output png files",
    ),
    max_workers: int = typer.Option(
        default=64,
        help="the maximum number of workers to convert dcm files to png files",
    ),
) -> None:
    ensure_dir(dcm_dir)
    ensure_dir(png_dir, create_ok=True)

    executor = ProcessPoolExecutor(max_workers=max_workers)
    futures: list[Future[Path]] = []

    dcm_paths = list(dcm_dir.glob("**/*.dcm"))
    for dcm_path in dcm_paths:
        future = executor.submit(dcm2png, dcm_path, png_dir, stem_suffix)
        futures.append(future)

    if not verbose:
        # if verbose is False, suppress all exceptions
        console.print_exception = lambda *args, **kwargs: None

    total = len(dcm_paths)
    for count, (dcm_path, future) in enumerate(zip(dcm_paths, futures), 1):
        try:
            png_path = future.result()
            console.print(f"{count:8d}/{total:8d}: {dcm_path.name} -> {png_path.name}")
        except:
            console.print(f"{count:8d}/{total:8d}: {dcm_path.name} -> failed")
            console.print_exception(show_locals=True)


if __name__ == "__main__":
    app()
