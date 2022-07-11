import os


def zipdir(path, zf):
    for dirname, subdirs, files in os.walk(path):
        for filename in files:
            zf.write(
                os.path.join(dirname, filename),
                os.path.relpath(os.path.join(dirname, filename),
                                os.path.join(path, '..')),
            )
