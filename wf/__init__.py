"""
Predict antimicrobial reistance
"""

from dataclasses import dataclass
import subprocess
from pathlib import Path
import os
from latch import small_task, workflow, large_gpu_task
from latch.types import LatchFile, LatchDir, LatchAppearanceType, LatchAuthor, LatchMetadata, LatchParameter, LatchRule
from typing import Optional
from enum import Enum
from dataclasses_json import dataclass_json
from glob import glob
from flytekit import conditional

metadata = LatchMetadata(
    display_name="Predict AMR resistance",
    documentation="https://github.com/Mykrobe-tools/mykrobe/wiki/AMR-Prediction",
    author=LatchAuthor(
        name="Geodette",
        email="steveodettegeorge@gmail.com",
        github="https://github.com/GeOdette",
    ),
    repository="https://github.com/GeOdette/mikrobe.git",
    license="MIT",
)
metadata.parameters = {
    "sample_name": LatchParameter(
        display_name="Sample name",
        description="The name of your samples",
    ),
    "species": LatchParameter(
        display_name="Species",
        description="The species from which the samples were obtained. e.g tb"
    ),
    "read1": LatchParameter(
        display_name="Read 1",
        description="Paired read 1 to be analyzed",
    ),
    "read2": LatchParameter(
        display_name="Read 2",
        description="Paired read 2 to be analyzed",
    ),
    "output_dir": LatchParameter(
        display_name="Output directory",
        description="The name of your output directory. *Create a directory at the console"
    ),
    "output_format": LatchParameter(
        display_name="Output format",
        description="Output format for your files. Default is a .csv",
    ),
}


class mykrobeOutput(Enum):
    json = "json"
    csv = "csv"
    JSONAndCSV = "json_and_csv"


class readStatus(Enum):
    singleEnd = "SE"
    pairedEnd = "PE"


# I dont think I'll use this.


@dataclass_json
@dataclass
class mykrobeoutFILes:
    csv: LatchFile
    JSON: LatchFile
    JSONandCSV: LatchFile


class outputFormatError(Exception):
    pass


@dataclass_json
@dataclass
class SingleEndReads:
    read1: LatchFile


@dataclass_json
@dataclass
class PaireEndReads:
    read1: LatchFile
    read2: LatchFile


@large_gpu_task
def mykrobe_task(species: str,
                 sample_name: str,
                 read1: LatchFile,
                 read2: Optional[LatchFile],
                 output_dir: LatchDir,
                 output_format: mykrobeOutput = mykrobeOutput.csv) -> LatchFile:
    # defining the output
    # for out_choice in mykrobeOutput:
    # if output_format.value == mykrobeOutput.csv:
    # mykrobe_output = Path("latch_mykrobe.csv")
    # elif output_format.value == mykrobeOutput.json:
    #  mykrobe_output = Path("latch_mykrobe.json")
    # elif output_format.value == mykrobeOutput.JSONAndCSV:
    # mykrobe_output = Path("latch_mikrobe")

    # else:
    #  raise outputFormatError(
    # "The output file chosen must be a CSV, JSON, or both JSON and CSV")
    # for file in input_dir.local_path:

    # read1 = glob.glob("*_r1")
    # read2 = glob.glob("*r2")
    # if isinstance(end_read_status, singleEnd):
    # reads = [str(read1.local_path), str(read2.local_path)]
    mykrobe_output = Path("latch_mykrobe.csv")

    _mykrobe_cmd = [
        "mykrobe",
        "predict",
        "-s",
        str(sample_name),
        "-S",
        str(species),
        "-1",
        read1.local_path,
        read2.local_path,
        "--output",
        str(mykrobe_output),
        "--format",
        output_format.value,

    ]
    with open(mykrobe_output, "w") as mk:
        subprocess.run(_mykrobe_cmd, stdout=mk, check=True)
    return LatchFile(str(mykrobe_output), f"{output_dir.remote_path}/latch_mykrobe.csv")
    # return conditional(("myrobe_files")
    # .if_(output_format.value == mykrobeOutput.csv)
    # .then(LatchFile(str(mykrobe_output), f"{output_dir.remote_path}/latch_mykrobe.csv"))
    # .elif_(output_format.value == mykrobeOutput.json)
    # .then(LatchFile(str(mykrobe_output), f"{output_dir.remote_path}/latch_mykrobe.json"))
    # .elif_(output_format.value == mykrobeOutput.JSONAndCSV)
    # .then(LatchFile(str(mykrobe_output), f"{output_dir.remote_path}/latch_mykrobe")))


@ workflow(metadata)
def mikrobe(species: str,
            sample_name: str,
            read1: LatchFile,
            read2: Optional[LatchFile],
            output_dir: LatchDir,
            output_format: mykrobeOutput = mykrobeOutput.csv) -> LatchFile:
    """Predict AMR

    # Mikrobe

    > This is the latch implementation of the Mykrobe AMR predictor

    # Basic Usage

    > Input fastq files and click __launch workflow__ at the latch console

    """
    return mykrobe_task(species=species, sample_name=sample_name, read1=read1, read2=read2, output_dir=output_dir, output_format=output_format)
