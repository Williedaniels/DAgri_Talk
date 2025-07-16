import multiprocessing

# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/settings.html

# The number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1

# The socket to bind to
bind = "0.0.0.0:5000"

# The maximum number of seconds to wait for a request
timeout = 120