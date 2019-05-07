from sqlalchemy import create_engine
import json
import yaml

def get_engine_postgres():
    with open("config.yaml") as stream:
        config=yaml.load(stream)
    return config
    eng = create_engine(config['postgres']['dbname'])
    return eng


