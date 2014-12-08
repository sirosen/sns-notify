#!/usr/bin/env python

import boto.sns
import json


class SNSMessage(object):
    def __init__(self, subject, body, protocol_overrides=None):
        """
        This is used to represent a notification that will be sent, potentially
        to multiple topics. It is used to wrap a message and its various
        attributes in a simple object.

        Typical usage might look like this:

        >>> overrides = {}
        >>> overrides['email'] = 'Email Message -- especially verbose'
        >>> overrides['sms'] = 'SMS msg, very terse'
        >>> msg = SNSMessage('SNS Notification!', 'Default Message',
        >>>                  protocol_overrides=overrides)
        >>> # send message

        or

        >>> uniform_msg = SNSMessage('SNS Notification!', 'Only Message!')
        >>> # send message

        Args:
            @subject
            The subject for email notification forms of this message.

            @body
            The default message body, if not otherwise modified.

        KWArgs:
            @protocol_overrides=None
            A dict of attributes that should be used to override forms of the
            message based on the protocol, as per the SNS JSON format spec.
        """
        self.subject = subject
        self.body = body

        protocol_dict = {'default': body}
        if protocol_overrides is not None:
            protocol_dict.update(protocol_overrides)

        self.json_body = json.dumps(self.protocol_dict)


def publish_message(sns_conn, topicarn, message):
    """
    Simple wrapper over boto.sns.SNSConnection.publish to translate an
    SNSMessage object into the correct form for the boto call.

    Args:
        @sns_conn
        An SNSConnection object used to publish messages.

        @topicarn
        The ARN of the topic to use for notification.

        @message
        The SNSMessage object to send.
    """
    sns_conn.publish(topic=topicarn, message=message.json_body,
            message_structure='json', subject=message.subject)


def main():
    """
    The main method for sending a notification. Handles all of the arg parsing
    and so forth -- none of that done ahead of time leads to better handling as
    an entry point if this is ever installed with setup.py
    """
    # TODO


if __name__ == '__main__':
    main()
