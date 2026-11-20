from typing import Literal, Optional
from pydantic import BaseModel, Field

class WasteRequest(BaseModel):
    house_number: Optional[str] = Field(
        min_length = 3, max_length = 50, default = None
    )
    estate_or_area: Optional[str] = Field(default = None, min_length = 5, max_length = 50)
    issue_type: Literal['missed_pickup', 'damaged_bin', 'delayed_pickup', 'other']
    issue_description: str = Field(min_length = 5, max_length = 300)
    is_urgent: Optional[bool] = Field(default = None)
    bin_type: Optional[str] = Field (
        default = None, min_length = 3, max_length = 30
    )

# request = WasteRequest(
#     # house_number = "House 14, Block C",
#     # is_urgent = True,
#     # bin_type = "general_waste",
#     estate_or_area = "Lekki Phase 1",
#     issue_type = "missed_pickup",
#     issue_description = "My waste bin was not collected yesterday.", 
# )

# print(request)