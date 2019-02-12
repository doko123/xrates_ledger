from app.core.config.app_setup import create_app, setup_db
from app.core.config.logging import dictConfig as _  #noqa

application = create_app()
db = setup_db(application)
