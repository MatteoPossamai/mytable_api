# IMPORTING STANDARD PACKAGES
import os

from dotenv import load_dotenv

# LOADING CUSTOM ENV VARS
ENV_TYPE = os.environ.get("ENV_TYPE", default="master")
if ENV_TYPE == "local":
    paths = [
        "./envs/django/.local-configs.env",
        "./envs/postgres/.local-configs.env",
    ]
elif ENV_TYPE == "master":
    paths = [
        "./envs/django/.configs.env",
        "./envs/postgres/.configs.env",
    ]

for path in paths:
    load_dotenv(path)