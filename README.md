# parallel_fitter
To allow multiple parallel fits during parameter F-testing

## Requirements
`pint-pulsar`

## Usage
```python
from astropy import units as u, constants as c
from astropy.time import Time
import numpy as np
from loguru import logger as log
import multiprocessing
from pathlib import Path
import pint
from pint.models import get_model_and_toas
import pint.logging
import parallel_fit

if __name__ == "__main__":
    __spec__ = None
    multiprocessing.freeze_support()

    pint.logging.setup("INFO")

    for testtype in tests:
        parfile = ...
        timfile = ...
        m, t = get_model_and_toas(parfile, timfile)

        # tf = parallel_fit.TestFitter(parfile, timfile)
        tf = parallel_fit.TestFitter(model=m, toas=t)
        results = tf.run(maxiter=20)
```
Note that when running as a script, the `multiprocessing.freeze_support()` line may be needed.

```python
    >>> tf = TestFitter(parfile, timfile)
    >>> results = tf.run(maxiter=20)
    # the results contain meta info about the start and stop time
    # as well as info about each specific parameter examined
    >>> parameters = list(results.keys())
    # the meta info is separate
    >>> parameters.remove('meta')
    # for example
    >>> print(results['PX'])
    # will contain info like:
    # {'number': 0, 'string': 'Combination 0: add PX', '
    # initvalues': [None, 0, 0, 0, 0, 0, 0], 'chi2': np.float64(59.064087888302154), 'dof': np.int16(55),
    # 'results': {'PX': <Quantity 5.20704212 mas>, 'F2': <Quantity 0. Hz / s2>, 'FD1': <Quantity 0. s>,
    # 'FD2': <Quantity 0. s>, 'FD3': <Quantity 0. s>, 'FD4': <Quantity 0. s>, 'FD5': <Quantity 0. s>}}
    # where it lists all of the parameters that have been considered for all of the tests, but all except
    # the parameter of interest should be at their default/null value

    # If you need to adjust the parameter sets, you can do that:
    >>> tf.defaults['extraparnames'].remove('F2')
    >>> tf.setup(maxFD=4)
    # and then re-run the fit
```

