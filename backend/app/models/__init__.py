from .user import User
from .account import Account
from .card import Card
from .transactions import Transactions

# >>> from app import create_app
# >>> from app.extensions import db
# >>> app = create_app()
# >>> app.app_context().push()
# >>> db.create_all()
# >>> exit()

# update account set euro_balance = 50000.00 where id = 1;