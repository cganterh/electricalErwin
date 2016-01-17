#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from sys import argv
from subprocess import call
from re import match
from functools import partial


def parse_massif_file(path):
    """Return execution time and max_mem from massif file.

    :param str path: The path to the massif output file.

    :return: A tuple in the form: (time, max_mem).

    The Massif file should be of the form::
        desc: --stacks=yes --time-unit=i
              --massif-out-file=massif.out
        cmd: ./a.out
        time_unit: i
        #-----------
        snapshot=0
        #-----------
        time=0
        mem_heap_B=0
        mem_heap_extra_B=0
        mem_stacks_B=0
        heap_tree=empty
        #-----------
        snapshot=1
        #-----------
        time=1485
        mem_heap_B=0
        mem_heap_extra_B=0
        mem_stacks_B=472
        heap_tree=empty
        ...
    """
    def get_var(name, table):
        """Yield the selected values of table.

        This generator yields the second value
        of each row of ``table`` for which the
        first value of the row has the value
        ``name``.

        :param str name:
            The name of the values that should
            be yielded.

        :param list table:
            A table of the form::
                [(name, value),
                 (name, value),
                 (name, value),
                 ...]
        :yield:
            The values of the rows for which their
            names are equal to the ``name `` parameter.
        """
        for r in table:
            if r[0] == name:
                yield r[1]

    with open(path) as f:
        table = [
            (m.group(1), int(m.group(2)))
            for m in map(partial(match, '(.+)=(\d+)'), f)
            if m is not None
            if m.group(1) in ('time', 'mem_heap_B',
                              'mem_stacks_B')
        ]

    time = next(
        get_var(
            'time', reversed(table)
        )
    )

    max_mem = max(
        sum(e) for e in zip(
            get_var('mem_heap_B', table),
            get_var('mem_stacks_B', table)
        )
    )

    return time, max_mem

if __name__ == '__main__':
    call(['valgrind', '--tool=massif', '--stacks=yes',
          '--time-unit=i', '--massif-out-file=massif.out',
          argv[1]])

    time, max_mem = parse_massif_file('massif.out')

    print('Memoria máxima utilizada:', max_mem, 'B')
    print('Tiempo de ejecución:', time, 'instr.')
