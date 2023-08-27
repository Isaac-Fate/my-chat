from typing import Optional
import os
from pathlib import Path
import tomllib
from xpyutils import lazy_property, singleton

@singleton
class Config:
    
    _data: Optional[dict] = None
    
    @lazy_property
    def PROJECT_ROOT_DIR(self) -> Path:
        
        return Path(self._data.pop("PROJECT_ROOT_DIR")).absolute()
    
    @lazy_property
    def OPENAI_API_KEY(self) -> Path:
        
        # Get the API key
        openai_api_key = self._data.pop("OPENAI_API_KEY")
        
        # Set the environment variable
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        return openai_api_key
    
    @lazy_property
    def ASSETS_DIR(self) -> Path:
        
        return self.PROJECT_ROOT_DIR.joinpath("assets")
    
    @lazy_property
    def MONGO_HOST(self) -> str:
        
        return self._data.get("mongo").pop("host")
    
    @lazy_property
    def MONGO_PORT(self) -> int:
        
        return self._data.get("mongo").pop("port")
    
    @lazy_property
    def MONGO_DATABASE_NAME(self) -> int:
        
        return self._data.get("mongo").pop("database_name")
    
    @lazy_property
    def MONGO_CONNECTION_STRING(self) -> str:
        
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DATABASE_NAME}"
    
    @lazy_property
    def QDRANT_HOST(self) -> str:
        
        return self._data.get("qdrant").pop("host")
    
    @lazy_property
    def QDRANT_PORT(self) -> int:
        
        return self._data.get("qdrant").pop("port")
    
    @lazy_property
    def QDRANT_CONNECTION_STRING(self) -> str:
        
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

CONFIG = Config()

def load_config(filepath: os.PathLike) -> Config:
    
    # Create the one and only configuration instance
    config = Config()
    
    # Read the config file
    with open(filepath, "rb") as f:
        data = tomllib.load(f)
        
    # Set the data attr of config
    setattr(Config, "_data", data)
    
    # Set the environment variable
    config.OPENAI_API_KEY
    
    return config
