from src.core import init_db, create_session
from src.core.config import settings

init_db()

print(settings.SQLALCHEMY_DATABASE_URI)
session = create_session()
print(session)