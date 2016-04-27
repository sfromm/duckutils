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

import grp
import logging
import os
import pwd
import subprocess
import sys

def daemonize():
    ''' daemonize process '''
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        logging.error("failed to fork (#1): (%d) %s", e.errno, e.strerror)
        sys.exit(1)
    # decouple from parent
    os.chdir('/')
    os.setsid()
    os.umask(0)
    # fork again
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        logging.error("failed to fork (#2): (%d) %s", e.errno, e.strerror)
        sys.exit(1)
    sys.stdout.flush()
    sys.stderr.flush()
    si = file(os.devnull, 'r')
    so = file(os.devnull, 'a+')
    se = file(os.devnull, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def write_pid_file(path):
    ''' write a pid file '''
    pid = str(os.getpid())
    logging.debug("writing pid file: %s", path)
    try:
        f = open(path, 'w')
        f.write(pid)
        f.close()
        return True
    except Exception as e:
        logging.error("failed to write pid file: %s", str(e))
        return False

def drop_privileges(user='nobody', group='nobody'):
    ''' drop privileges if running as root '''
    if os.getuid() != 0:
        return
    new_uid = pwd.getpwname(user).pw_uid
    new_gid = grp.getgrname(group).gr_gid
    try:
        os.setgroups([])
        os.setgid(new_gid)
        os.setuid(new_uid)
    except OSError as e:
        logging.error("failed to drop privileges: %s", str(e))
