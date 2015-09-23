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

        self.json_body = json.dumps(protocol_dict)
