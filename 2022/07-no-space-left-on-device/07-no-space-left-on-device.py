#!/usr/bin/env python3

import sys
import re

class ElfFile:
    name: str

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return(f'ElfFile(name={self.name})')

    def is_dir(self):
        return None


class ElfRegularFile(ElfFile):
    size: int

    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

    def __repr__(self):
        return(f'ElfRegularFile(name={self.name}, size={self.size})')

    def is_dir(self):
        return False


class ElfDir(ElfFile):
    content: list[ElfFile]
    parent: ElfFile	# Can't specify ElfDir, argh.

    def __init__(self, name, content=None):
        super().__init__(name)
        if name == '/':
            self.parent = self
        if content == None:
            self.content = []
        else:
            self.content = content

    def __repr__(self):
        annotate_name = lambda ef: ef.is_dir() and f'{ef.name}/' or ef.name
        names_str = ", ".join([annotate_name(f) for f in self.content])
        return(f'ElfDir(name={self.name}, content=[{names_str}])')

    def is_dir(self):
        return True

    def find_by_name(self, elf_file_name:str):
        if elf_file_name == '.':
            return self
        elif elf_file_name == '..':
            return self.parent
        else:
            for ef in self.content:
                if elf_file_name == ef.name:
                    return ef
        return None

    def add(self, elf_file:ElfFile):
        if not self.find_by_name(elf_file.name):
            if elf_file.is_dir():
                elf_file.parent = self
            self.content.append(elf_file)


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
                    # Not handling error cases
                    cwd = cwd.find_by_name(elf_dir_name)
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
                    new_file = ElfRegularFile(name, int(size))
                cwd.add(new_file)

    return fs


# depth first, not exactly pre-order
def fs_walk(fs, fn, depth=0):
    if fs.name == '/':
        fn(fs, depth)

    for ef in fs.content:
        fn(ef, depth+1)
        if ef.is_dir():
            fs_walk(ef, fn, depth+1)


def fs_walk_postorder(fs, fn, depth=0):
    result = []

    for ef in fs.content:
        if ef.is_dir():
            result.extend(fs_walk_postorder(ef, fn, depth+1))
        result.append(fn(ef, depth))

    # if fs.name == '/':
    #     result.extend(fs_walk_postorder(ef,fn, depth+1))

    return result


def lol(fs):
    dir_size = 0

    if fs.is_dir():
        for ef in fs.content:
            dir_size += lol(ef)

        dh["{}/{}".format(fs.parent.name, fs.name)] = dir_size
        return dir_size
    else:
        return fs.size


def custom_print(ef, depth, indent="  "):
    bullet = "- "
    indent_str = "".join([indent for _ in range(0, depth)])
    print("{}{}{}".format(indent_str, bullet, repr(fs)))


def aoc_print(ef, depth, indent="  "):
    bullet = "- "
    indent_str = "".join([indent for _ in range(0, depth)])
    if ef.is_dir():
        ef_info = "{} (dir)".format(ef.name)
    else:
        ef_info = "{} (file, size={})".format(ef.name, ef.size)
    print("{}{}{}".format(indent_str, bullet, ef_info))


if __name__ == "__main__":
    fs = build_fs(sys.stdin)
    #fs_walk(fs, aoc_print)

    # THIS IS HORRIBLE HAHAHAHAHAHAHAH I SUCK AT PROGRAMMING
    dh = {}	# SORRY
    lol(fs)
    print(sum([x for x in dh.values() if x < 100000]))

