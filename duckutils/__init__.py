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

__name__ = 'duckutils'
__author__ = 'Stephen Fromm'
__version__ = '0.1'

import logging
import logging.handlers

import duckutils.constants as C


def setup_logging(verbose, debug, use_syslog=False):
    ''' initalize logging

    :param verbose: boolean value for whether to enable be verbose
    :param debug: boolean value to enable debug mode
    :param use_syslog: boolean for whether to log to syslog
    '''
    loglevel = 'WARN'
    if verbose:
        loglevel = 'INFO'
    if debug:
        loglevel = 'DEBUG'
    numlevel = getattr(logging, loglevel.upper(), None)
    if not isinstance(numlevel, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logargs = {}
    logargs['level'] = numlevel
    logargs['datefmt'] = '%FT%T'
    logargs['format'] = C.DEFAULT_LOGFORMAT
    logging.basicConfig(**logargs)
    if use_syslog:
        # remove default logger and add syslog handler
        logger = logging.getLogger()
        if 'flush' in dir(logger):
            logger.flush()

        h = logger.handlers[0]
        logger.removeHandler(h)
        if isinstance(h, logging.FileHandler):
            h.close()

        handler = logging.handlers.SysLogHandler(address='/dev/log')
        formatter = logging.Formatter('%(filename)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
