"""Label management actions."""

from .add_label_to_email import AddLabelToEmail
from .move_email import MoveEmail
from .remove_label_from_email import RemoveLabelFromEmail

__all__ = [
    "AddLabelToEmail",
    "MoveEmail",
    "RemoveLabelFromEmail",
]
