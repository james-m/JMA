#!/bin/bash
#
LOGDIR="${HOME}/codez/logs/djtut"
PIDFILE="${LOGDIR}/spawn.pid"

PID=`cat $PIDFILE`

echo "Killing ${PID}..."
kill $PID
echo "done."