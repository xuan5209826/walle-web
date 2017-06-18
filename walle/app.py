# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import sys

from flask import Flask, render_template
from flask_restful import Api

from walle import commands
from walle.api import access as AccessAPI
from walle.api import api as BaseAPI
from walle.api import environment as EnvironmentAPI
from walle.api import group as GroupAPI
from walle.api import passport as PassportAPI
from walle.api import project as ProjectAPI
from walle.api import public as PublicAPI
from walle.api import role as RoleAPI
from walle.api import server as ServerAPI
from walle.api import task as TaskAPI
from walle.api import user as UserAPI
from walle.config.settings import ProdConfig
from walle.service.extensions import bcrypt, csrf_protect, db, migrate
from walle.service.extensions import login_manager
from walle.model.user import UserModel


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    reload(sys)
    sys.setdefaultencoding('utf-8')
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    api = Api(app)
    api.add_resource(BaseAPI.Base, '/', endpoint='root')
    api.add_resource(PublicAPI.PublicAPI, '/api/public/<string:method>', endpoint='public')
    api.add_resource(AccessAPI.AccessAPI, '/api/access/', '/api/access/<int:access_id>', endpoint='access')
    api.add_resource(RoleAPI.RoleAPI, '/api/role/', '/api/role/<int:role_id>', endpoint='role')
    api.add_resource(GroupAPI.GroupAPI, '/api/group/', '/api/group/<int:group_id>', endpoint='group')
    api.add_resource(PassportAPI.PassportAPI, '/api/passport/', '/api/passport/<string:method>', endpoint='passport')
    api.add_resource(UserAPI.UserAPI, '/api/user/', '/api/user/<int:user_id>', endpoint='user')
    api.add_resource(ServerAPI.ServerAPI, '/api/server/', '/api/server/<int:id>', endpoint='server')
    api.add_resource(ProjectAPI.ProjectAPI, '/api/project/', '/api/project/<int:project_id>', endpoint='project')
    api.add_resource(TaskAPI.TaskAPI, '/api/task/', '/api/task/<int:task_id>', endpoint='task')
    api.add_resource(EnvironmentAPI.EnvironmentAPI, '/api/environment/', '/api/environment/<int:env_id>',
                     endpoint='environment')

    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': UserModel,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
