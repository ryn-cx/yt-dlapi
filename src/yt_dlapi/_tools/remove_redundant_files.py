# TODO: Validate
"""Removes redundant YtDlapi files."""

import logging

from good_ass_pydantic_integrator.utils import remove_redundant_files

import yt_dlapi

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    remove_redundant_files(yt_dlapi)
