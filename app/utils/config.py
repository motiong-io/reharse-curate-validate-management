import os
from typing import Optional

from motiong.knowledgereference.v1.enums.status_pb2 import KnowledgeStatusEnum
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):

    DATABASE_URI: PostgresDsn



    INTERACTION_MANAGEMENT_ENDPOINT: str
    SPACE_MANAGEMENT_ENDPOINT: str



class LocalDevSettings(EnvSettings):

    model_config = SettingsConfigDict(env_file="config", extra="ignore")


class DeployedSettings(EnvSettings):
    # takes in env vars from the pod
    ...


def find_config() -> EnvSettings:
    if os.getenv("ENV"):
        return DeployedSettings()
    else:
        return LocalDevSettings()


env = find_config()

if __name__ == "__main__":
    print(env)
