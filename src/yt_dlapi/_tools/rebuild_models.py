import logging

from good_ass_pydantic_integrator.utils import rebuild_models

import yt_dlapi

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    rebuild_models(yt_dlapi)
