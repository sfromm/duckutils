# Written by Stephen Fromm <stephenf nero net>
# (C) 2016 University of Oregon
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import logging
import email.utils
import json
import socket
import smtplib
import time

try:
    from email.mime.text import MIMEText
except ImportError:
    from email.MIMEText import MIMEText

import duckutils.constants as C

try:
    import fedmsg
    import fedmsg.confi
    HAVE_FEDMSG = True
except ImportError:
    HAVE_FEDMSG = False

def send_email(msg, sender, recipient, subject, **kwargs):
    ''' send an email

    :param msg: Email message body
    :param sender: Email sender
    :param recipient: Email recipient
    :param subject: Subject of email
    :param server: SMTP server, defaults to localhost
    '''
    server = kwargs.get('server', DEFAULT_SMTP_SERVER)
    cc = kwargs.get('cc', None)
    recipients = list()
    recipients.append(recipient)
    msg = MIMEText(msg)
    msg['From'] = sender
    msg['To'] = recipient
    if cc:
        msg['Cc'] = cc
        recipients.append(cc)
    msg['Date'] = email.utils.formatdate(time.time(), True)
    msg['Subject'] = subject
    try:
        s = smtplib.SMTP(server)
        s.sendmail(sender, recipients, msg.as_string())
        s.quit()
    except Exception, e:
        logging.warn('failed to send email: %s', str(e))
        return False
    return True

def fedmsg_publish(msg, modname=C.DEFAULT_FEDMSG_MODNAME, topic=C.DEFAULT_FEDMSG_TOPIC):
    ''' publish message to fedmsg bus

    :param msg: JSON message
    :param modname: Message topic name
    :param topic: Message topic
    '''
    if not HAVE_FEDMSG:
        return
    hostname = socket.gethostname().split('.', 1)[0]
    fedmsg.init(name="modname.{0}".format(hostname))
    fedmsg.publish(
        modname=modname,
        topic=topic,
        msg=msg,
    )
