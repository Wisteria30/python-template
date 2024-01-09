#!/bin/bash
# entrypoint.sh
echo "=========================================="
# if you want to use wandb
cp /var/tmp/.netrc ${HOME}/
echo "=========================================="
exec "$@"
