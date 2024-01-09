from python_template.config.settings import Settings

# Server Socket
bind = f"0.0.0.0:{Settings().PORT}"

# Worker Processes
#
# See below for recommended settings for Cloud Run:
# https://cloud.google.com/run/docs/tips/python#optimize_the_wsgi_server
workers = 1
threads = 8
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 0

# Logging
loglevel = Settings().LOG_LEVEL
