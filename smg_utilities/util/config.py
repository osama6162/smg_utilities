# -*- coding: utf-8 -*-

"""Generate a default configuration-file section for smg_utilities"""

from __future__ import print_function


def config_section_data():
    """Produce the default configuration section for app.config,
       when called by `resilient-circuits config [-c|-u]`
    """
    return u"""
[smg_utilities]
smg_url=
smg_username=
smg_password=
smg_log=
"""
