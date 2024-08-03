from enum import Enum


class SharedNarrationsStatus(Enum):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    CHECKING = 'checking'
    TRANSFERRED = 'transferred'
    PENDING = 'pending'
