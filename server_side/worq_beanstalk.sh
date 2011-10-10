#!/bin/sh

echo 'Listening...'

beanstalkd -l 127.0.0.1 -p 9000
