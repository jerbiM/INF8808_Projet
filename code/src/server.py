'''
    Contains the server to run our application.
'''
from flask_failsafe import failsafe


@failsafe
def create_app():
    '''
        Gets the underlying Flask server from our Dash app.
        Returns:
            The server to be run
    '''
    # the import is intentionally inside to work with the server failsafe
    from src.app import app  # pylint: disable=import-outside-toplevel
    return app.server

app=create_app()

if __name__ == "__main__":
    app.run()
