from json import dumps, loads
from time import time

from messages import SayText2
from players.helpers import index_from_userid

from .models.ranked_player import RankedPlayer as DB_RankedPlayer

from .resource.sqlalchemy import Session

from .resource.strings import COLOR_SCHEME, strings_common


class RankedPlayer:
    def __init__(self, player):
        self.player = player

        # We're saving to database asynchronously, and some properties will
        # be unavailable
        self._steamid = player.steamid
        self._last_used_name = player.name

        self.score = 0
        self.position = 0
        self.online_time = 0
        self.detected_at = 0
        self.last_seen_at = 0
        self.data = {}

        self._loaded = False

    @property
    def loaded(self):
        return self._loaded

    def load_from_database(self):
        if self._steamid == "BOT":
            return

        db_session = Session()

        db_ranked_player = db_session.query(DB_RankedPlayer).filter_by(
            steamid=self._steamid).first()

        if db_ranked_player is not None:
            self.score = db_ranked_player.account
            self.position = db_ranked_player.position
            self.online_time = db_ranked_player.online_time
            self.detected_at = db_ranked_player.detected_at
            self.last_seen_at = db_ranked_player.last_seen_at
            self.data = loads(db_ranked_player.data)

        self._loaded = True

        db_session.close()

    def save_to_database(self):
        if self._steamid == "BOT":
            return

        if not self._loaded:
            raise RuntimeError("User couldn't be synced with database")

        db_session = Session()

        db_ranked_player = db_session.query(DB_RankedPlayer).filter_by(
            steamid=self._steamid).first()

        if db_ranked_player is None:
            db_ranked_player = DB_RankedPlayer()
            db_ranked_player.steamid = self._steamid
            db_ranked_player.position = 0
            db_ranked_player.detected_at = time()
            db_session.add(db_ranked_player)

        db_ranked_player.last_used_name = self._last_used_name
        db_ranked_player.score = self.score

        # We don't update 'position' field - it's rather read-only
        # in terms of database and is managed by a separate thread
        # from time to time

        db_ranked_player.online_time = self.online_time
        db_ranked_player.last_seen_at = time()
        db_ranked_player.data = dumps(self.data)

        db_session.commit()
        db_session.close()


class RankedPlayerManager(dict):
    def get_by_userid(self, userid):
        return self.get(index_from_userid(userid))

ranked_player_manager = RankedPlayerManager()


def tell(ranked_players, message, **tokens):
    """Send a SayText2 message to a list of RankedPlayer instances."""
    if isinstance(ranked_players, RankedPlayer):
        ranked_players = (ranked_players, )

    player_indexes = [
        ranked_player.player.index for ranked_player in ranked_players]

    tokens.update(COLOR_SCHEME)

    message = message.tokenize(**tokens)
    message = strings_common['chat_base'].tokenize(
        message=message, **COLOR_SCHEME)

    SayText2(message=message).send(*player_indexes)


def broadcast(message, **tokens):
    """Send a SayText2 message to all registered users."""
    tell(list(ranked_player_manager.values()), message, **tokens)
