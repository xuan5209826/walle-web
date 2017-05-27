# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from walle import commands, user
from walle.extensions import bcrypt, csrf_protect, db, login_manager, migrate
from walle.settings import ProdConfig
from walle.common import api as resource
from flask_restful import Api

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
    api.add_resource(resource.Base, '/', endpoint='root')
    api.add_resource(resource.RoleAPI, '/api/role/', '/api/role/<int:role_id>', endpoint='role')
    api.add_resource(resource.GroupAPI, '/api/group/', '/api/group/<int:group_id>', endpoint='group')
    api.add_resource(resource.PassportAPI, '/api/passport/', '/api/passport/', endpoint='passport')
    api.add_resource(resource.UserAPI, '/api/user/', '/api/user/<int:user_id>', endpoint='user')
    api.add_resource(resource.EnvironmentAPI, '/api/environment/', '/api/environment/<int:env_id>', endpoint='environment')
    api.add_resource(resource.ServerAPI, '/api/server/', '/api/server/<int:id>', endpoint='server')
    api.add_resource(resource.ProjectAPI, '/api/project/', '/api/project/<int:project_id>', endpoint='project')
    api.add_resource(resource.TaskAPI, '/api/task/', '/api/task/<int:task_id>', endpoint='task')


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
            'User': user.models.User,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
