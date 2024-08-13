###############################################################################
#
#        ███████████ ████████    ████████████
#        ██     ██      ██       ██   ██   ██ █
#        ███████████ ██      ██  ██████████
#        ██          ██ ██     ██████ ██     ██
#        ███████████ █████    ██     ███████
#                   █        █████████████████   ████████
#                    █    █ ██   ██   ██  ██     ██   ██   ██
#                     ████  ██████   ██  ██  █████████   ██
#                      ████   ██  █   ██  ██   ████   ██   ██
#                             ██   ████████████   ██   ██
# -----------------------------------------------------------------------------
#
#      Author: Lorenzo D. Moon (Lodomo.Dev)
#        Date:
#     Purpose: Test the "Role" Class without being derived.
# Description: This serves as the base class for all the roles. It helps to
#              ensure that all roles have the same structure and can be
#              easily integrated into the experience.
#              This is a test file to ensure that the Role class is working
#              as an semi-abstract base class
#
###############################################################################


import pytest

from escapewright import Role
from escapewright.enums import Status


# PURE TESTS
def test_role():
    role = Role()
    assert role.status is Status.INIT
    assert role.running is False


def test_join_thread():
    role = Role()
    assert role._Role__force_join_thread() is False  # Nothing Running
    role._Role__running = True
    assert role._Role__force_join_thread() is True  # No Thread, but Running


def test_relay_status():
    role = Role()
    assert role._Role__relay_status(Status.READY) == 0

    def listener(status):
        return

    role.sub_to_status(listener)
    assert role._Role__relay_status(Status.READY) == 1


def test_load():
    role = Role()

    with pytest.raises(NotImplementedError):
        role.process_message("load")
        role._Role__load()
        role._load()


def test_logic():
    role = Role()

    with pytest.raises(NotImplementedError):
        role.process_message("logic")
        role._Role__logic()
        role._logic()


def test_start():
    role = Role()

    with pytest.raises(NotImplementedError):
        role.process_message("start")
        role._Role__start()
        role._start()


def test_reset():
    role = Role()

    with pytest.raises(NotImplementedError):
        role.process_message("reset")
        role._Role__reset()
        role._reset()


def test_stop():
    role = Role()

    with pytest.raises(NotImplementedError):
        role.process_message("stop")
        role._Role__stop()
        role._stop()


def test_bypass():
    role = Role()

    with pytest.raises(NotImplementedError):
        role.process_message("bypass")
        role._Role__bypass()
        role._bypass()


def test_default_triggers():
    role = Role()
    assert role._Role__default_triggers() == {
        "load": role._Role__load,
        "start": role._Role__start,
        "reset": role._Role__reset,
        "stop": role._Role__stop,
        "bypass": role._Role__bypass,
    }


def test_process_message():
    role = Role()
    assert role.process_message("junk") is False


def test_add_triggers():
    role = Role()

    def junk():
        return

    some_triggers = {"junk": junk}

    role._add_triggers(some_triggers)
    assert role._Role__triggers == {
        "load": role._Role__load,
        "start": role._Role__start,
        "reset": role._Role__reset,
        "stop": role._Role__stop,
        "bypass": role._Role__bypass,
        "junk": junk,
    }


def test_update_status():
    role = Role()

    assert role._update_status(Status.READY) == Status.READY
    assert role.status == Status.READY


if __name__ == "__main__":
    pytest.main(["-v", __file__])
