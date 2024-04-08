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

from escapewright import RoleTemplate
from escapewright.enums import Status


def test_derived_functions():
    role = RoleTemplate()

    role.process_message("load")
    role._Role__load()
    assert role._load() is None

    role.process_message("logic")
    role._Role__logic()
    assert role._logic() is None

    role.process_message("start")
    role._Role__start()
    assert role._start() is None

    role.process_message("reset")
    role._Role__reset()
    assert role._reset() is None

    role.process_message("stop")
    role._Role__stop()
    assert role._stop() is None

    role.process_message("bypass")
    role._Role__bypass()
    assert role._bypass() is None


def test_added_triggers():
    role = RoleTemplate()
    assert role._Role__triggers == {
        "trigger_name": role._load,
        "load": role._Role__load,
        "start": role._Role__start,
        "reset": role._Role__reset,
        "stop": role._Role__stop,
        "bypass": role._Role__bypass,
    }

if __name__ == "__main__":
    pytest.main(["-v", __file__])
