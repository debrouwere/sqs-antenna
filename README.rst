Antenna.

Usage: antenna listen antenna configure

The most stupidly simple way to scale an application is through a
message queue, at least where latency is not an issue. If you're using
the AWS ecosystem, the most stupidly simple way to run tasks based on
messages from a message queue is through Antenna.

Grab a message from a queue, run a command and if it worked, remove the
message:

::

    antenna listen <profile> <queue> "<command>" \
        1> antenna.log \
        2> antenna.err.log

Antenna will look for credentials in either ``~/.aws/config`` (this is
where your `AWS CLI <http://aws.amazon.com/documentation/cli/>`__
credentials live) or ``~/.boto`` if you're using
`Boto <http://boto.readthedocs.org/>`__ in Python.

::

    [profile my-profile-name]
    aws_access_key_id=<id>
    aws_secret_access_key=<secret>
    region=<region>

An easy way to see if everything is working would be to manually add a
couple of messages with the `SQS Management
Console <https://console.aws.amazon.com/sqs/home>`__, and use
``"cat >> log.txt"`` as a command.

You can also add messages to the queue from the command line with the
`AWS CLI <http://aws.amazon.com/documentation/cli/>`__

::

    # get your queue's endpoint if you only know its name
    aws sqs get-queue-url --profile my-profile-name --queue-name my-queue | jq '.QueueUrl'
    aws sqs send-message --queue-url my-queue-url --message-body my-message-body

For more information, look at the `AWS CLI documentation for
SQS <http://docs.aws.amazon.com/cli/latest/reference/sqs/index.html>`__

Install Antenna with ``pip``, the Python package installer.

::

    pip install sqs-antenna

While Antenna will run indefinitely, executing your command for each
message it receives, it's probably still safe to run Antenna as a
daemon.

If you're on Ubuntu, you can run Antenna as a daemon by adding it to
Upstart:

::

    antenna configure <profile> <queue> "<command>" > /etc/init/<task>.conf
    initctl reload-configuration
    start <task>

