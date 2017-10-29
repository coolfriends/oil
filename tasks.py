## https://github.com/pyinvoke/invoke

from invoke import task

@task
def test(ctx):
    command = 'python -m unittest'
    ctx.run(command)
