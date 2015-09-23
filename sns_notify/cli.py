import boto.sns
import argparse

from .message import SNSMessage


def publish_message(topicarn, message):
    """
    Simple wrapper over boto.sns.SNSConnection.publish to translate an
    SNSMessage object into the correct form for the boto call.

    Args:
        @topicarn
        The ARN of the topic to use for notification.

        @message
        The SNSMessage object to send.
    """
    sns_conn = boto.sns.SNSConnection()
    sns_conn.publish(topic=topicarn, message=message.json_body,
                     message_structure='json', subject=message.subject)


def main():
    """
    The main method for sending a notification. Handles all of the arg parsing
    and so forth -- none of that done ahead of time leads to better handling as
    an entry point if this is ever installed with setup.py

    Parses arguments, creates an SNSMessage, and sends that SNSMessage to the
    given Topic.
    """
    # parse le arguments!
    parser = argparse.ArgumentParser(description='Send a notification to SNS')
    parser.add_argument('topicarn',
                        help='The ARN for the SNS Topic to notify.')
    # note, the service is optional
    # when given, assume this is a service notification
    # when absent, assume this is a host notification
    parser.add_argument('--service', '-S', dest='service',
                        help=('The name of the service being checked. When ' +
                              'absent, we assume that this is a host check ' +
                              'notification.'))
    parser.add_argument('--host', '-H', dest='host', required=True,
                        help='The host on which the check was done.')
    parser.add_argument('--type', '--notification-type', '-T', dest='ty',
                        required=True,
                        help='"PROBLEM", "RECOVERY", or "ACKNOWLEDGMENT"')
    parser.add_argument('--state', dest='state',
                        required=True,
                        help='"OK", "WARNING", or "CRITICAL"')
    parser.add_argument('--output', '--check-output', dest='output',
                        required=True,
                        help=("The output of the check command. May be " +
                              "trimmed down in SMS form."))

    args = parser.parse_args()

    check_target = args.host
    if args.service:
        check_target = '{0}:{1}'.format(args.host, args.service)

    # define the email subject line
    subject = '{0} {1} {2}'.format(args.ty, check_target, args.state)
    # the email body
    email_body = '{0}\n{1}\n\n{2}'.format(check_target, args.state,
                                          args.output)
    # and the SMS text
    overrides = {}
    overrides['sms'] = '{0} {1} {2} {3}'.format(args.ty, check_target,
                                                args.state, args.output)
    # wrap it up in a message object
    msg = SNSMessage(subject, email_body,
                     protocol_overrides=overrides)

    # and send it!
    publish_message(args.topicarn, msg)


if __name__ == '__main__':
    main()
