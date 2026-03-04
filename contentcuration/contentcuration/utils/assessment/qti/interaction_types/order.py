from typing import Annotated
from typing import List
from typing import Optional

from annotated_types import Len
from pydantic import Field

from contentcuration.utils.assessment.qti.constants import Orientation
from contentcuration.utils.assessment.qti.interaction_types.base import BlockInteraction
from contentcuration.utils.assessment.qti.interaction_types.simple import SimpleChoice
from contentcuration.utils.assessment.qti.prompt import Prompt


class OrderInteraction(BlockInteraction):
    """For ordering questions"""

    shuffle: bool = True
    min_choices: Optional[int] = None
    max_choices: Optional[int] = None
    orientation: Orientation = Orientation.VERTICAL
    prompt: Optional[Prompt] = None
    children: Annotated[List[SimpleChoice], Len(min_length=1)]
