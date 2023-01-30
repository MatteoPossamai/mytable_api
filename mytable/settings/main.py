# IMPORTING STANDARD PACKAGES
import os

from dotenv import load_dotenv

# LOADING CUSTOM ENV VARS
ENV_TYPE = os.getenv("ENV_TYPE", default="master")

if ENV_TYPE == "local":
    paths = [
        "./envs/django/.local-configs.env",
        "./envs/db/.local-configs.env",
    ]
elif ENV_TYPE == "venv":
    paths = [
        "./envs/django/.venv-configs.env",
        "./envs/db/.venv-configs.env",
    ]
elif ENV_TYPE == "master":
    paths = [
        "./envs/django/.configs.env",
        "./envs/db/.configs.env",
    ]

for path in paths:
    load_dotenv(path)
