#!/usr/bin/env python3

import sys
import re

class ElfFile:
    name: str

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return(f'ElfFile(name={self.name})')


class ElfRegularFile(ElfFile):
    size: int

    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

    def __repr__(self):
        return(f'ElfRegularFile(name={self.name}, size={self.size})')


class ElfDir(ElfFile):
    content: list[ElfFile]
    parent: ElfFile	# Can't specify ElfDir, argh.

    def __init__(self, name, content=None):
        super().__init__(name)
        if content == None:
            self.content = []
        else:
            self.content = content

    def __repr__(self):
        annotate_name = lambda ef: is_elf_dir(ef) and f'{ef.name}/' or ef.name
        names_str = ", ".join([annotate_name(f) for f in self.content])
        return(f'ElfDir(name={self.name}, content=[{names_str}])')

    def find_by_name(self, elf_file_name:str):
        for ef in self.content:
            if elf_file_name == ef.name:
                return ef
        return None

    def add(self, elf_file:ElfFile):
        if not self.find_by_name(elf_file.name):
            if is_elf_dir(elf_file):
                elf_file.parent = self
            self.content.append(elf_file)


def is_elf_dir(f):
    return isinstance(f, ElfDir)


def build_fs(fh):
    fs = None
    cwd = None

    command_re = re.compile('^\$ (cd|ls) ?([-\./0-9a-zA-Z]+)?')
    file_re = re.compile('^(/|[-\.0-9a-zA-Z]+) ([-\.0-9a-zA-Z]+)')

    for line in fh:
        line = line.rstrip('\n')
        if line == '$ cd /':
            # root is special, so I don't feel bad treating it as a special case.
            if fs == None:
                fs = ElfDir('/')
            cwd = fs
        else:
            m = command_re.match(line)
            if m:
                cmd = m.group(1)
                if cmd == 'cd':
                    elf_dir_name = m.group(2)
                    print(repr(cwd))
                    if cwd.find_by_name(elf_dir_name):
                        print("find {} worked".format(elf_dir_name))
                elif cmd == 'ls':
                    # ls doesn't require us to do anything, tbh.
                    continue
            else:
                m = file_re.match(line)
                name = m.group(2)
                if m.group(1) == 'dir':
                    new_file = ElfDir(name)
                else:
                    size = m.group(1)
                    new_file = ElfRegularFile(name, size)
                cwd.add(new_file)


    return fs


if __name__ == "__main__":
    fs = build_fs(sys.stdin)
