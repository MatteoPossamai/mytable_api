# IMPORTING STANDARD PACKAGES
import os

from dotenv import load_dotenv

# LOADING CUSTOM ENV VARS
ENV_TYPE = os.getenv("ENV_TYPE", default="venv")
if ENV_TYPE == "local":
    paths = [
        "./envs/django/.local-configs.env",
        "./envs/postgres/.local-configs.env",
    ]
elif ENV_TYPE == "venv":
    paths = [
        "./envs/django/.venv-configs.env",
        "./envs/postgres/.venv-configs.env",
    ]
elif ENV_TYPE == "master":
    paths = [
        "./envs/django/.configs.env",
        "./envs/postgres/.configs.env",
    ]

for path in paths:
    load_dotenv(path)
