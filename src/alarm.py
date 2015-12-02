#!/usr/bin/env python
#
#
#
'''
Module to perform the scheduling functions
'''

#---------------------------------------------------------------------------#
import os
import sys
import datetime
import signal
import time
import threading

from argparse import ArgumentParser
import logging
from ConfigParser import SafeConfigParser, NoOptionError
from logging.config import fileConfig

from configParse import configParse

__version__ = '0.1.0'

#---------------------------------------------------------------------------#
def signal_handler(signal, frame):
    print ('You pressed Ctrl+C')
    logger.info('Script Stopped on: %s' % time.asctime(
        time.localtime(time.time())))
    sys.exit(0)

#---------------------------------------------------------------------------#
class alarm(threading.Thread):
    """performs the function of the alarm
        duration  and snooze_interval are defined in seconds
    """
    def __init__(self, duration=300, snooze=420, time_format=24):
        super(alarm, self).__init__()
        self.threadID = 2
        self.name = '%(prog)s'
        self.stoprequest = threading.Event()

        self.duration = duration
        self.snooze = snooze
        self.time_format = time_format

        self.start = None
        self.end = None

        self.alarm_repeat = False
        self.alarm_repeat_schedule = {
        'sunday': False,
        'monday': False,
        'tuesday': False,
        'wednesday': False,
        'thursday': False,
        'friday': False,
        'saturday': False
        }

        self.active = False
        self.enabled = False

    def run(self):
        while not self.stoprequest.isSet():
            if self.enabled:
                if time.time() >= self.start and time.time() < self.end:
                    self.active = True
                elif time.time() >= self.end:
                    self.active = False

            time.sleep(1)


    def join(self, timeout=None):
        self.stoprequest.set()
        super(dataValidation, self).join(timeout)

    def setStartTime(self, start_time):
        if self.time_format = 24:
            self.start = time.strptime(start_time, '%H:%M')
        elif self.time_format = 12:
            self.start = time.strptime(start_time, '%I:%M %p')

        self.end = self.start + duration

    def changeDuration(self, duration):
        self.duration = duration
        self.end = self.start + duration

    def silence(self):
        self.active = False

    def snooze(self):
        self.start = time.time() + self.snooze
        self.active = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def check(self):
        return self.active

#---------------------------------------------------------------------------#
if __name__ == '__main__':

    #register Ctrl-C signal handler
    signal.signal(signal.SIGINT, signal_handler)

    fileConfig('sunrise.ini')
    logger = logging.getLogger('scheduler')


    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '--sw_file', help='file path and name of Sierra Wireless file',
    #     default='C:\\Users\\jeastman\\Desktop\\Draker SN List_Truncated.csv'
    #     )
    parser.add_argument(
        '-v', '--version', action='version',version='%(prog)s ' + __version__
        )
    args = parser.parse_args()

    logger.info(
        'Script started on: %s' % time.asctime(time.localtime(time.time()))
        )

    alarm1 = alarm()

    # starts the thread
    alarm1.start()

    alarm1.setStartTime('22:55')
    alarm1.enable()

    # wait for user input
    while True:
        cmd = sys.stdin.readline()

        if cmd.find('quit') == 0:
            # stops the thread
            alarm1.join()
            break
        elif cmd.find('c') == 0:
            print 'Alarm State: {}'.format(alarm1.check())

