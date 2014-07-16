#!/usr/bin/env python
# encoding: utf-8

""" Antenna.

Usage:
    antennna listen <profile> <queue> <command>
    antenna configure <profile> <queue> <command>

The most stupidly simple way to scale an application is through a message queue,
at least where latency is not an issue. If you're using the AWS ecosystem, the
most stupidly simple way to run tasks based on messages from a message queue is
through Antenna.

Grab a message from a queue, run a command and if it worked, remove the message:

    antenna listen <profile> <queue> "<command>" \\
        1> antenna.log \\
        2> antenna.err.log

Antenna will look for credentials in either `~/.aws/config` (this is where your
AWS CLI credentials live) or `~/.boto`.

    [profile my-profile-name]
    aws_access_key_id=<id>
    aws_secret_access_key=<secret>
    region=<region>

Install Antenna with `pip`, the Python package installer.

    pip install sqs-antenna

While Antenna will run indefinitely, executing your command for each message it
receives, it's probably still safe to run Antenna as a daemon.

If you're on Ubuntu, you can run Antenna as a daemon by adding it to Upstart:

    antenna configure <profile> <queue> "<command>" > /etc/init/<task>.conf
    initctl reload-configuration
    start <task>

"""

from docopt import docopt


def listen(profile, queue_name, command):
    import sys
    import os
    import subprocess
    from StringIO import StringIO
    import ConfigParser
    import json
    import boto.sqs

    # while Boto can read its own configuration just fine, we want Antenna 
    # to also work with AWS CLI configuration file
    config = ConfigParser.ConfigParser()
    config.read(map(os.path.expanduser, ['~/.aws/config', '~/.boto']))
    region = config.get(profile, 'region')
    access_key = config.get(profile, 'aws_access_key_id')
    secret_key = config.get(profile, 'aws_secret_access_key')

    sqs = boto.sqs.connect_to_region(region, 
        aws_access_key_id=access_key, 
        aws_secret_access_key=secret_key)

    queue = sqs.get_queue(queue_name)

    while True:
        messages = queue.get_messages(1, wait_time_seconds=20)

        if len(messages):
            message = messages[0]
            body = message.get_body()
            process = subprocess.Popen([command], stdin=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate(body)

            if stdout:
                sys.stdout.writeline(stdout)

            if stderr:
                sys.stderr.writeline(stderr)
            else:
                queue.delete_message(message)



def main():
    arguments = docopt(__doc__, version='Antenna 0.1')

    # TODO: Upstart configuration template
    listen(**kwargs)

if __name__ == '__main__':
    main()