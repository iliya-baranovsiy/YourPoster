from enum import Enum


class AddChannelStatus(Enum):
    OK = "ok"
    NOT_CHANNEL = "not_a_channel"
    ALREADY_EXISTS = "already_exists"
    NO_ACCESS = "no_access"
