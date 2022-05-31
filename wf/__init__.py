"""
Predict antimicrobial reistance
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile


@small_task
def mykrobe_task(species: str, sample_name: str, reads: LatchFile, output_name: str) -> LatchFile:
    # defining the output
    csv_file = Path("out.csv").resolve()
    _mykrobe_cmd = [
        "mykrobe",
        "predict",
        "--species",
        species,
        "--sample",
        str(sample_name),
        "--seq",
        reads.local_path,
        "--output",
        output_name

    ]
    subprocess.run(_mykrobe_cmd, check=True)
    return LatchFile(str(Path("csv_file")), "latch:///out.csv")


@workflow
def mikrobe(species: str, sample_name: str, reads: LatchFile, output_name: str) -> LatchFile:
    """Predict AMR



    __metadata__:
        display_name: Predict AMR resistance
        author:
            name:
            email:
            github:
        repository:
        license:
            id: MIT

    Args:
        species:
          pathogen species e.g tb

          __metadata__:
            display_name: Species

        sample_name:
          Sample name

          __metadata__:
            display_name: Sample Name

        reads:
          File containing DNA sequences

          __metadata__:
            display_name: Reads

        output_name:
          Name for your output file e.g out.csv

          __metadata__:
            display_name: Output
    """

    return mykrobe_task(species=species, sample_name=sample_name, reads=reads, output_name=output_name)
