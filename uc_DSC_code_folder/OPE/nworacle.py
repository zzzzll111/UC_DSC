#!/usr/bin/env python3

##################################################################
# This file is part of the POPE implementation.                  #
# Paper at https://eprint.iacr.org/2015/1106                     #
# U.S. Government work product, in the public domain.            #
# Written in 2015 by Daniel S. Roche, roche@usna.edu             #
##################################################################

"""
This file contains client and server classes for the backend POPE
server to connect to a comparison oracle.
"""

import socket
import socketserver
import pickle
import argparse

import ciphers
import oracle

"""Single byte op-codes"""
PARTITION = b'p'
PARTITION_SORT = b's'
FIND = b'f'
MAX_SIZE = b'm'

DEBUG = True
BUFSIZE = 1024


# convenience method
def identity(x):
    return x


class OracleClient:
    """Accessed by an OPE back-end server in order to determine the order
    of elements.
    """

    def __init__(self, hostname, port):
        """There should be an oracle server running on the specified hostname
        and port."""
        self._addr = (hostname, port)
        self._conn = None

    def open(self):
        """opens the connection and allows operations"""
        if self._conn:
            raise RuntimeError("already open")
        self._conn = socket.create_connection(self._addr)
        self._sockfile = self._conn.makefile('rwb')

        # go get the max size
        # send opcode
        self._sockfile.write(MAX_SIZE)
        self._sockfile.flush()
        self._max_size = pickle.load(self._sockfile)

    def __enter__(self):
        self.open()
        return self

    def close(self):
        """closes the connection"""
        if not self._conn:
            raise RuntimeError("not open; can't close it")
        try:
            self._sockfile.flush()
            self._sockfile.close()
            self._conn.close()
        except:
            pass
        del self._sockfile
        del self._conn
        self._conn = None

    def __exit__(self, t, v, r):
        self.close()

    @property
    def max_size(self):
        return self._max_size

    def partition(self, needles, haystack, nkey=identity, haykey=identity):
        """Just like partition() in oracle.Oracle."""
        # send opcode
        self._sockfile.write(PARTITION)

        # send haystack and haykey
        pickle.dump(haystack, self._sockfile)
        pickle.dump(haykey, self._sockfile)

        # send nkey
        pickle.dump(nkey, self._sockfile)

        # do partition
        res = self._send_rec_stream(needles)

        return res

    def partition_sort(self, needles, haystack, nkey=identity, haykey=identity):
        """Just like partition_sort() in oracle.Oracle."""
        # send opcode
        self._sockfile.write(PARTITION_SORT)

        # send haystack and haykey
        pickle.dump(haystack, self._sockfile)
        pickle.dump(haykey, self._sockfile)
        self._sockfile.flush()

        # receive sorted haystack
        shay = pickle.load(self._sockfile)

        # send nkey
        pickle.dump(nkey, self._sockfile)

        # do the partition
        res = self._send_rec_stream(needles)

        return shay, res

    def _send_rec_stream(self, outvals):
        """Convenience method to send and receive a stream of the same length,
        buffered according to global variable BUFSIZE."""
        res = []

        count = 0
        for x in outvals:
            pickle.dump(x, self._sockfile)
            count += 1

            # stop sending and receive some results
            if count == BUFSIZE:
                self._sockfile.flush()
                res.extend(pickle.load(self._sockfile) for _ in range(BUFSIZE))
                count = 0

        # indicate end
        pickle.dump(None, self._sockfile)
        self._sockfile.flush()

        # receive any remaining results
        res.extend(pickle.load(self._sockfile) for _ in range(count))

        return res

    def find(self, needles, haystack, nkey=identity, haykey=identity):
        """Just like find() in oracle.Oracle."""
        # send opcode
        self._sockfile.write(FIND)

        # send haystack and haykey
        pickle.dump(haystack, self._sockfile)
        pickle.dump(haykey, self._sockfile)

        # send nkey
        pickle.dump(nkey, self._sockfile)

        # find everything
        res = self._send_rec_stream(needles)

        return res


class OracleHandler(socketserver.BaseRequestHandler):
    # Note: must have field "orc" added to point to the underlying Oracle instance

    def handle(self):
        with self.request.makefile('rwb') as sockfile:
            if DEBUG: print("Connection open")
            while True:
                # receive opcode
                opcode = sockfile.read(1)
                if not opcode:
                    if DEBUG: print("Connection closed")
                    return
                elif opcode == PARTITION:
                    if DEBUG: print("Received PARTITION request")
                    self.partition(sockfile)
                elif opcode == PARTITION_SORT:
                    if DEBUG: print("Received PARTITION_SORT request")
                    self.partition_sort(sockfile)
                elif opcode == FIND:
                    if DEBUG: print("Received FIND request")
                    self.find(sockfile)
                elif opcode == MAX_SIZE:
                    if DEBUG: print("Received MAX_SIZE request")
                    pickle.dump(self.orc.max_size, sockfile)
                    sockfile.flush()
                else:
                    raise RuntimeError("ORACLE ERROR: invalid opcode", opcode)
                if DEBUG:
                    print("(finished request)")
                    print()

    def stream_until_none(self, sockfile):
        while True:
            obj = pickle.load(sockfile)
            if obj is None:
                break
            yield obj

    def _stream_back(self, sockfile, L):
        """sends back the list or generator, stopping occationally to flush"""
        count = 0
        for x in L:
            pickle.dump(x, sockfile)
            count += 1
            if count == BUFSIZE:
                sockfile.flush()
                count = 0

    def partition(self, sockfile):
        # read haystack and haykey
        haystack = pickle.load(sockfile)
        haykey = pickle.load(sockfile)

        # read nkey
        nkey = pickle.load(sockfile)

        # read needles
        needles = self.stream_until_none(sockfile)

        # stream back results
        self._stream_back(sockfile, self.orc.partition(needles, haystack, nkey, haykey))

        sockfile.flush()

    def partition_sort(self, sockfile):
        # read haystack and haykey
        haystack = pickle.load(sockfile)
        haykey = pickle.load(sockfile)

        # sort haystack and send it back
        shay = self.orc.sort(haystack, haykey)
        pickle.dump(shay, sockfile)
        sockfile.flush()

        # read nkey
        nkey = pickle.load(sockfile)

        # read needles
        needles = self.stream_until_none(sockfile)

        # stream back results
        self._stream_back(sockfile, self.orc.partition(needles, shay, nkey, haykey))

        sockfile.flush()

    def find(self, sockfile):
        # read haystack and haykey
        haystack = pickle.load(sockfile)
        haykey = pickle.load(sockfile)

        # read nkey
        nkey = pickle.load(sockfile)

        # read needles
        needles = self.stream_until_none(sockfile)

        # stream back results
        self._stream_back(sockfile, self.orc.find(needles, haystack, nkey, haykey))

        sockfile.flush()


def get_oracle_server(the_oracle, hostname, port):
    """Creates a socketserver to relay requests to given oracle."""

    class Handler(OracleHandler):
        orc = the_oracle

    return socketserver.TCPServer((hostname, port), Handler)
