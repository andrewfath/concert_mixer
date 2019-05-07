from sqlalchemy import create_engine
import json
import yaml

def get_engine_postgres():
    with open("config.yaml") as stream:
        config=yaml.load(stream)
    user=config['postgres']['user']
    pw=config['postgres']['pw']
    host='localhost'
    db=config['postgres']['dbname']
    eng = create_engine("postgresql+psycopg2://{}:{}@{}/{}".format(user,pw,host,db))
    return eng


