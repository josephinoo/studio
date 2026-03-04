from typing import Annotated
from typing import List
from typing import Optional

from annotated_types import Len
from pydantic import Field

from contentcuration.utils.assessment.qti.base import BaseSequence
from contentcuration.utils.assessment.qti.base import QTIBase
from contentcuration.utils.assessment.qti.fields import QTIIdentifier
from contentcuration.utils.assessment.qti.html import FlowContentList
from contentcuration.utils.assessment.qti.interaction_types.base import BlockInteraction
from contentcuration.utils.assessment.qti.prompt import Prompt


class SimpleAssociableChoice(QTIBase, BaseSequence):
    """
    Represents a choice in a QTI match interaction.
    """

    identifier: QTIIdentifier
    match_max: int = 1
    match_min: int = 0
    children: FlowContentList = Field(default_factory=list)


class SimpleMatchSet(QTIBase, BaseSequence):
    """
    A set of associable choices in a match interaction.
    """

    children: List[SimpleAssociableChoice] = Field(default_factory=list)


class MatchInteraction(BlockInteraction):
    """For matching questions"""

    shuffle: bool = True
    max_associations: int = 0
    min_associations: int = 0
    prompt: Optional[Prompt] = None
    children: Annotated[List[SimpleMatchSet], Len(min_length=2, max_length=2)]
