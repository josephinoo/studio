from typing import List
from typing import Optional

from pydantic import Field

from contentcuration.utils.assessment.qti.base import BaseSequence
from contentcuration.utils.assessment.qti.base import QTIBase
from contentcuration.utils.assessment.qti.fields import QTIIdentifier
from contentcuration.utils.assessment.qti.html import FlowContentList
from contentcuration.utils.assessment.qti.interaction_types.base import BlockInteraction
from contentcuration.utils.assessment.qti.prompt import Prompt


class GapText(QTIBase, BaseSequence):
    identifier: QTIIdentifier
    match_max: int = 1
    match_min: int = 0
    children: FlowContentList = Field(default_factory=list)


class Gap(QTIBase):
    identifier: QTIIdentifier
    required: Optional[bool] = None


class GapMatchInteraction(BlockInteraction):
    """For fill in the blank and drag and drop questions"""

    shuffle: bool = True
    prompt: Optional[Prompt] = None
    gap_texts: List[GapText] = Field(default_factory=list)
    children: FlowContentList = Field(default_factory=list)
