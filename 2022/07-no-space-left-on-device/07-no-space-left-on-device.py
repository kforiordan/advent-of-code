#!/usr/bin/env python3

import sys

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

    def __init__(self, name, content=None):
        super().__init__(name)
        if content == None:
            self.content = []
        else:
            self.content = content


if __name__ == "__main__":
    
