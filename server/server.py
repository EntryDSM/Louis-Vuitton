import os
import optparse

from app import create_app
from config import DevConfig, ProductionConfig


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    if options.debug:
        app = create_app(DevConfig)
    else:
        app = create_app(ProductionConfig)

    if "SECRET_KEY" not in os.environ:
        print("SECRET_KEY isn't set in OS environ")

    app.run(**app.config['RUN_SETTINGS'])
