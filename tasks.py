## https://github.com/pyinvoke/invoke

import unittest
from invoke import task

@task
def test(ctx, no_functional=True):
    if no_functional:
        ctx.run('export OIL_FUNCTIONAL_TESTS=False')
    else:
        ctx.run('export OIL_FUNCTIONAL_TESTS=True')

    command = 'python -m unittest'
    ctx.run(command)
