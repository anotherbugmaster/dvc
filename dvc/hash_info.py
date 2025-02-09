from collections import OrderedDict
from dataclasses import dataclass, field

HASH_DIR_SUFFIX = ".dir"


@dataclass
class HashInfo:
    PARAM_SIZE = "size"
    PARAM_NFILES = "nfiles"

    name: str
    value: str
    dir_info: dict = field(default=None, compare=False)
    size: int = field(default=None, compare=False)
    nfiles: int = field(default=None, compare=False)

    def __bool__(self):
        return bool(self.value)

    @classmethod
    def from_dict(cls, d):
        _d = d.copy() if d else {}
        size = _d.pop(cls.PARAM_SIZE, None)
        nfiles = _d.pop(cls.PARAM_NFILES, None)

        if not _d:
            return cls(None, None)

        ((name, value),) = _d.items()
        return cls(name, value, size=size, nfiles=nfiles)

    def to_dict(self):
        ret = OrderedDict()
        if not self:
            return ret

        ret[self.name] = self.value
        if self.size is not None:
            ret[self.PARAM_SIZE] = self.size
        if self.nfiles is not None:
            ret[self.PARAM_NFILES] = self.nfiles
        return ret

    @property
    def isdir(self):
        if not self:
            return False
        return self.value.endswith(HASH_DIR_SUFFIX)
