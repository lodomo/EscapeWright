###############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Control the Screamboat Simulated Reality Experience
#     Version: 0.0.1 - Derived from Code Samurai Version 2.X
# Description: Control the entire Screamboat Simulated Reality Experience
#              This should be ran from a gunicorn server.
#              Entry Points are as follows:
#              TBD
#
###############################################################################

from flask import Flask


PORT = 12413
HOST = "0.0.0.0"

pi_list_file = "pi_list.ew"

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True, threaded=True)
