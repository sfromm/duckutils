# Written by Stephen Fromm <stephenf nero net>
# (C) 2012 University of Oregon
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

import smtplib
import logging

try:
    from email.mime.text import MIMEText
except ImportError:
    from email.MIMEText import MIMEText

def send_email(msg, sender, recipient, subject, server='localhost'):
    ''' send an email

    :param msg: Email message body
    :param sender: Email sender
    :param recipient: Email recipient
    :param subject: Subject of email
    :param server: SMTP server, defaults to localhost
    '''
    msg = MIMEText(msg)
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    try:
        s = smtplib.SMTP(server)
        s.sendmail(sender, [recipient], msg.as_string())
        s.quit()
    except Exception, e:
        logging.warn('failed to send email: %s', str(e))
        return False
    return True
