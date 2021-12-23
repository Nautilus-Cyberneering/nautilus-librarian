# pylint: disable=no-member
# Dinamically added members of GIT API Repo object are not detected by pyLint

import os.path
import tempfile
from os import path

from git import Repo

import nautilus_librarian.nautilus_dvc_api.nautilus_dvc_api as dvcapi

# temp_dir will store the File object pointing to the temporary directory that will store
# all the objects generated by each tests.


temp_dir = None


# If the following variable has some path value (e.g. "/tmp/testObjects"), test contest will be
# stored there, instead on a random temporary folder. Useful for debugging tests.


test_dir = None


def create_test_contents():
    with open(path.join(get_test_dir(), "test.data"), "w") as file:
        file.write("lorem ipsum")


def remove_contents():
    os.remove("test.data")


def push_test_contents():
    repo = Repo(get_test_dir())
    repo.add("test.data.dvc")
    repo.push(repo.push(refspec="master:master"))


def get_test_dir():
    if test_dir is None:
        return temp_dir.name
    else:
        return test_dir


# TO-DO: Currently, this functions creates the temporary directory using tempfile.TemporaryDirectory.
#        This can produce an exception in DVC execution when adding a remote storage to a repo, for unknown causes.
#        To prevent this, tempfile.mkdtemp can be used, but additional logic for deletin the temp dir should be
#        added. A better option could be using pytest fixtures.
def create_test_scenario(init_GIT=False, init_DVC=False, create_contents=False):
    global temp_dir
    temp_dir = tempfile.TemporaryDirectory()
    os.chdir(get_test_dir())
    print(get_test_dir())
    if init_GIT:
        Repo.init(get_test_dir())
    if init_DVC:
        dvcapi.init(get_test_dir(), no_scm=(not init_GIT))
    if create_contents:
        create_test_contents()
    return


def add_remote_to_scenario():
    remote_temp_dir = tempfile.TemporaryDirectory().name
    os.system("dvc remote add -d localremote " + remote_temp_dir)


def test_dvc_init():
    create_test_scenario(init_GIT=True, init_DVC=True)
    assert path.exists(".dvc")


def test_dvc_standalone_init():
    create_test_scenario(init_DVC=True)
    assert path.exists(".dvc")


def test_add():
    create_test_scenario(init_GIT=True, init_DVC=True, create_contents=True)
    dvcapi.add(get_test_dir(), "test.data")
    assert path.exists("test.data.dvc")
    assert path.exists(".gitignore")


def test_status():
    create_test_scenario(init_GIT=True, init_DVC=True, create_contents=True)
    dvcapi.add(get_test_dir(), "test.data")
    add_remote_to_scenario()
    assert dvcapi.status(get_test_dir(), remote="localremote") == {"test.data": "new"}


def test_push():
    create_test_scenario(init_GIT=True, init_DVC=True, create_contents=True)
    dvcapi.add(get_test_dir(), "test.data")
    add_remote_to_scenario()
    dvcapi.push(get_test_dir())
    assert dvcapi.status(get_test_dir(), remote="localremote") == {}


def test_pull():
    create_test_scenario(init_GIT=True, init_DVC=True, create_contents=True)
    dvcapi.add(get_test_dir(), "test.data")
    add_remote_to_scenario()
    dvcapi.push(get_test_dir())
    assert path.exists("test.data")
    remove_contents()
    assert not path.exists("test.data")
    dvcapi.pull(get_test_dir())
    assert path.exists("test.data")


def test_list():
    create_test_scenario(init_GIT=True, init_DVC=True, create_contents=True)
    dvcapi.add(get_test_dir(), "test.data")
    add_remote_to_scenario()
    dvcapi.push(get_test_dir())
    expected_list_output = [
        {"isout": False, "isdir": False, "isexec": False, "path": ".dvcignore"},
        {"isout": False, "isdir": False, "isexec": False, "path": ".gitignore"},
        {"isout": True, "isdir": False, "isexec": False, "path": "test.data"},
        {"isout": False, "isdir": False, "isexec": False, "path": "test.data.dvc"},
    ]
    assert dvcapi.list(get_test_dir()) == expected_list_output
