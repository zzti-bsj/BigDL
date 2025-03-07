#!/usr/bin/env python

#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

import sys
from shutil import copyfile, copytree, rmtree
import fnmatch
from setuptools import setup

TEMP_PATH = "bigdl/share/orca"
bigdl_home = os.path.abspath(__file__ + "/../../../..")
exclude_patterns = ["*__pycache__*", "*ipynb_checkpoints*"]

VERSION = open(os.path.join(bigdl_home, 'python/version.txt'), 'r').read().strip()

RAY_DEP = ['ray[default]==1.9.2', 'aiohttp==3.8.1', 'async-timeout==4.0.1', 'aioredis==1.3.1',
           'hiredis==2.0.0', 'setproctitle', 'psutil', 'prometheus-client==0.11.0']
AUTOML_DEP = RAY_DEP + ['ray[tune]==1.9.2', 'scikit-learn', 'tensorboard']

building_error_msg = """
If you are packing python API from BigDL source, you must build BigDL first
and run sdist.
    To build BigDL with maven you can run:
      cd $BigDL_HOME
      ./make-dist.sh
    Building the source dist is done in the Python directory:
      cd python
      python setup.py sdist
      pip install dist/*.tar.gz"""


def build_from_source():
    code_path = bigdl_home + "/python/orca/src/bigdl/orca/common.py"
    print("Checking: %s to see if build from source" % code_path)
    if os.path.exists(code_path):
        return True
    return False


def init_env():
    if build_from_source():
        print("Start to build distributed package")
        print("HOME OF BIGDL: " + bigdl_home)
        dist_source = bigdl_home + "/dist"
        if not os.path.exists(dist_source):
            print(building_error_msg)
            sys.exit(-1)
        if os.path.exists(TEMP_PATH):
            rmtree(TEMP_PATH)
        copytree(dist_source, TEMP_PATH)
        copyfile(bigdl_home + "/python/orca/src/bigdl/orca/automl/__init__.py",
                 TEMP_PATH + "/__init__.py")
    else:
        print("Do nothing for release installation")


def get_bigdl_packages():
    bigdl_python_home = os.path.abspath(__file__ + "/..")
    bigdl_packages = ['bigdl.share.orca']
    source_dir = os.path.join(bigdl_python_home, "bigdl")
    for dirpath, dirs, files in os.walk(source_dir):
        package = dirpath.split(bigdl_python_home)[1].replace('/', '.')
        if any(fnmatch.fnmatchcase(package, pat=pattern)
                for pattern in exclude_patterns):
            print("excluding", package)
        else:
            bigdl_packages.append(package)
            print("including", package)
    return bigdl_packages


def setup_package():
    metadata = dict(
        name='bigdl-orca',
        version=VERSION,
        description='Seamlessly scale out TensorFlow and PyTorch for Big Data (using Spark & Ray)',
        author='BigDL Authors',
        author_email='bigdl-user-group@googlegroups.com',
        license='Apache License, Version 2.0',
        url='https://github.com/intel-analytics/analytics-zoo',
        packages=get_bigdl_packages(),
        install_requires=['packaging', 'filelock',
                          'bigdl-tf==0.14.0.dev1', 'bigdl-math==0.14.0.dev1',
                          'bigdl-dllib=='+VERSION, 'pyzmq'],
        extras_require={'ray': RAY_DEP,
                        'automl': AUTOML_DEP,
                        },
        dependency_links=['https://d3kbcqa49mib13.cloudfront.net/spark-2.0.0-bin-hadoop2.7.tgz'],
        include_package_data=True,
        package_data={"bigdl.share.orca": ['lib/bigdl-orca*.jar']},
        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython'],
        platforms=['mac', 'linux']
    )

    setup(**metadata)


if __name__ == '__main__':
    try:
        init_env()
        setup_package()
    except Exception as e:
        raise e
    finally:
        if build_from_source() and os.path.exists(TEMP_PATH):
            rmtree(TEMP_PATH)
