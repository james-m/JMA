#!/bin/bash
#
LOGDIR="${HOME}/codez/logs/djtut"
PIDFILE="${LOGDIR}/spawn.pid"



spawn --factory=spawning.django_factory.config_factory mysite.settings \
  --port 8000 -s 4 -t 0 \
  --daemonize \
  --pidfile=$PIDFILE \
  --stdout="${LOGDIR}/stdout.log" \
  --stderr="${LOGDIR}/stderr.log" \
  --access-log-file="${LOGDIR}/access.log"