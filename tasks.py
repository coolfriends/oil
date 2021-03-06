## https://github.com/pyinvoke/invoke

import unittest
import os
from invoke import task

@task
def test(ctx, no_functional=False):
    if no_functional:
        os.environ['OIL_FUNCTIONAL_TESTS'] = str(False)
    else:
        os.environ['OIL_FUNCTIONAL_TESTS'] = str(True)

    ctx.run('python -m unittest')

@task
def coverage(ctx):
    ctx.run('coverage run --source=oil -m unittest discover -s tests')
    ctx.run('coverage report')
