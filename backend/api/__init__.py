from flask import Blueprint
api = Blueprint('api', 'api', url_prefix='', static_folder='../../instance/dist/static')
api.config = {}


@api.record
def record_params(setup_state):
    app = setup_state.app
    api.config = dict([(key, value) for (key, value) in app.config.items()])


from .dataset_api import *
from .document_api import *
from .project_api import *
from .user_api import *
from .summary_api import *









