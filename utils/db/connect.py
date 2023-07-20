from mongoengine import connect
from sqlalchemy import create_engine
import configparser
import pathlib

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")

config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get("MONGO_DB", "user")
mongodb_pass = config.get("MONGO_DB", "pass")
mongo_db_name = config.get("MONGO_DB", "db_name")
mongo_domain = config.get("MONGO_DB", "domain")

# connect to cluster on AtlasDB with connection string

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{mongo_domain}/{mongo_db_name}?retryWrites=true&w=majority""",
    ssl=True,
)

postgr_username = config.get('POSTGR_DB', 'user')
postgr_password = config.get('POSTGR_DB', 'password')
postgr_db_name = config.get('POSTGR_DB', 'db_name')
postgr_domain = config.get('POSTGR_DB', 'domain')
postgr_port = config.get('POSTGR_DB', 'port')

URL = f'postgresql://{postgr_username}:{postgr_password}@{postgr_domain}:{postgr_port}/{postgr_db_name}'

engine = create_engine(URL, echo=False, pool_size=5, max_overflow=0)

