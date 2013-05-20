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
import subprocess
import traceback
import yaml

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

def parse_yaml(data):
    ''' convert yaml string to data structure '''
    return yaml.load(data)

def parse_yaml_from_file(path):
    ''' read yaml string from path and convert to data structure '''
    try:
        data = file(path).read()
        return parse_yaml(data)
    except IOError:
        logging.error('file not found: %s', path)
        return None
    except yaml.YAMLError, e:
        msg = 'Could not parse YAML file %s' % path
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            msg = 'Invalid yaml file %s: line %s, column %s' % (
                    path, mark.line +1, mark.column + 1
            )
        logging.error(msg)
        return None

def run_command(args, cwd=None):
    ''' run a command via subprocess '''
    shell = True
    if isinstance(args, list):
        shell = False
    out = ''
    try:
        cmd = subprocess.Popen(args, shell=shell, cwd=cwd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        out, err = cmd.communicate()
        rc = cmd.returncode
    except (OSError, IOError), e:
        err = str(e)
        rc = e.errno
    except:
        err = traceback.format_exc()
        rc = 257
    return (rc, out, err)
