import decimal
import pytest
from dynaconf import settings

TESTDB = "test_project.db"
TESTDB_PATH = "/opt/project/data/{}".format(TESTDB)
TEST_DATABASE_URI = "mysql:///" + TESTDB_PATH
settings.TESTING = True
settings.SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI

# Set the precision and rounding policy.
custom_decimal_context = decimal.Context(prec=8, rounding=decimal.ROUND_UP)
decimal.setcontext(custom_decimal_context)


@pytest.fixture(scope="session")
def app(request):
    """Session-wide test `Flask` application."""
    from app.run_app import application

    # Establish an application context before running the tests.
    ctx = application.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return application


@pytest.fixture(scope="function")
def db(app, request):
    """
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    """
    from app.core.config.app_setup import setup_db

    database = setup_db(app)

    yield database

    # Explicitly close DB connection
    database.session.close()
    database.drop_all()


@pytest.fixture(scope="function")
def cache(app, request):
    """
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    """
    from app.core.interfaces.redis import RedisInterface

    cache = RedisInterface().cache

    yield cache

    # Flush database after test
    cache.flushall()
    RedisInterface().cache = None
    RedisInterface().instance = None


@pytest.fixture
def client(app):
    client = app.test_client()

    yield client
