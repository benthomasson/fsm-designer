
import tempfile
import shutil


def before_scenario(context, scenario):
    context.tempdir = tempfile.mkdtemp()


def after_scenario(context, scenario):
    shutil.rmtree(context.tempdir)
