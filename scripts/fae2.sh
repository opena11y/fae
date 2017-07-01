#!/bin/bash
#
# chkconfig: 35 90 12
# description: FAE 2.0 Self Registration Production evaluation processor
#
# Get function from functions library
. /etc/init.d/functions
# Start the service FOO
start() {
        echo "Starting FAE Self Registration evaluation processor: "
    /var/www/fae2/virtual-environments/fae-self-reg-production/bin/python /var/www/fae2/fae-self-reg-production/f
ae2/fae-util/process_evaluation_requests.py  &
        ### Create the lock file ###
        touch /var/lock/subsys/fae-self-reg-production
        success $"FAE Self Registration Production evaluation processor startup"
        echo
}
# Restart the service FOO
stop() {
        echo "Stopping FAE Self Production evaluation processor: "
#        killproc /var/www/fae2/virtual-envronments/fae2-self-reg-production/bin/python
        ### Now, delete the lock file ###
        rm -f /var/lock/subsys/fae-self-reg-production
        echo
}
### main logic ###
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        status FOO
        ;;
  restart|reload|condrestart)
        stop
        start
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac
exit 0