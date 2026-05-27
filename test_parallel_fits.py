from astropy import units as u, constants as c
from astropy.time import Time
import numpy as np
from loguru import logger as log
import multiprocessing
from pathlib import Path
import pint
from pint.models import get_model_and_toas
import pint.logging
import json
import parallel_fit

testdata = Path(pint.__file__).resolve().parent.parent.parent / "tests/datafile"

tests = {
    "no binary": {
        "parfile": Path(pint.config.examplefile("NGC6440E.par")),
        "timfile": Path(pint.config.examplefile("NGC6440E.tim")),
    },
    "ELL1 PB": {
        "parfile": testdata / "J0613-0200_NANOGrav_9yv1.gls.par",
        "timfile": testdata / "J0613-0200_NANOGrav_9yv1.tim",
    },
    "ELL1 FB": {
        "parfile": testdata / "J0023+0923_NANOGrav_11yv0.gls.par",
        "timfile": testdata / "J0023+0923_NANOGrav_11yv0.tim",
    },
    "ELL1H": {
        "parfile": testdata / "J1853+1303_NANOGrav_11yv0.gls.par",
        "timfile": testdata / "J1853+1303_NANOGrav_11yv0.tim",
    },
    "DD": {
        "parfile": testdata / "B1855+09_NANOGrav_9yv1.gls.par",
        "timfile": testdata / "B1855+09_NANOGrav_9yv1.tim",
    },
}

if __name__ == "__main__":
    __spec__ = None
    multiprocessing.freeze_support()

    pint.logging.setup("INFO")

    for testtype in tests:
        log.debug(f"RUNNING test {testtype}: {tests[testtype]['parfile'].parts[-1]}")
        print(
            f"Starting test {testtype}: {tests[testtype]['parfile'].parts[-1]} at {Time.now().iso}"
        )
        parfile = tests[testtype]["parfile"]
        timfile = tests[testtype]["timfile"]
        m, t = get_model_and_toas(parfile, timfile)

        tf = parallel_fit.TestFitter(parfile, timfile)
        # can also specify existing model/toas objects
        # tf = parallel_fit.TestFitter(model=m, toas=t)
        results = tf.run(maxiter=20)

        print(f"Finished test '{testtype}' at {Time.now().iso}\n\n")
        with open(f"{testtype}_results.json", "w") as fo:
            json.dump(
                results,
                fo,
                indent=4,
                default=parallel_fit.astropy_numpy_json_serializer,
            )
