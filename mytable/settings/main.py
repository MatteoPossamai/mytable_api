# IMPORTING STANDARD PACKAGES
import os

from dotenv import load_dotenv

# LOADING CUSTOM ENV VARS
ENV_TYPE = os.getenv("ENV_TYPE", default="master")
if ENV_TYPE == "local":
    paths = [
        "./.env",
        "./envs/django/.local-configs.env",
        "./envs/postgres/.local-configs.env",
    ]
elif ENV_TYPE == "venv":
    paths = [
        "./.env",
        "./envs/django/.venv-configs.env",
        "./envs/postgres/.venv-configs.env",
    ]
elif ENV_TYPE == "master":
    paths = [
        "./.env",
        "./envs/django/.configs.env",
        "./envs/postgres/.configs.env",
    ]
print(paths)
for path in paths:
    load_dotenv(path)
