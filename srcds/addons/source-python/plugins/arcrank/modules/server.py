from cvars import ConVar
from listeners import OnLevelInit

from spam_proof_commands.server import ServerCommand

from ..internal_events import InternalEvent

from ..models.server import Server as DB_Server

from ..resource.config import config

from ..resource.sqlalchemy import Session


cvar_hostname = ConVar("hostname")


class Server:
    def __init__(self):
        self.server_id = config['database']['server_id']
        self.hostname = None
        self.total_positions = 0
        self.last_sorted_at = 0

    def load_from_database(self):
        db_session = Session()

        db_server = db_session.query(DB_Server).filter_by(
            server_id=self.server_id).first()

        if db_server is not None:
            self.hostname = db_server.hostname
            self.total_positions = db_server.total_positions
            self.last_sorted_at = db_server.last_sorted_at

        db_session.close()

    def save_to_database(self):
        db_session = Session()

        db_server = db_session.query(DB_Server).filter_by(
            server_id=self.server_id).first()

        if db_server is None:
            db_server = DB_Server()
            db_server.server_id = self.server_id
            db_server.hostname = cvar_hostname.get_string()
            db_session.add(db_server)

        db_server.total_positions = self.total_positions
        db_server.last_sorted_at = self.last_sorted_at

        db_session.commit()
        db_session.close()

server = Server()


@InternalEvent('load')
def on_load(event_var):
    server.load_from_database()


@InternalEvent('unload')
def on_unload(event_var):
    server.save_to_database()


@OnLevelInit
def listener_on_level_init(map_name):
    server.save_to_database()


@ServerCommand(5, 'arcrank_save_hostname')
def server_arcrank_save_hostname(command):
    server.hostname = cvar_hostname.get_string()
    server.save_to_database()
