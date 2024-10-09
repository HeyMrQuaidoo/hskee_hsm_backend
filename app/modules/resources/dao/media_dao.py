from typing import List, Optional

from app.modules.common.dao.base_dao import BaseDAO
from app.modules.resources.models.media import Media

class MediaDAO(BaseDAO[Media]):
    def __init__(self, excludes: Optional[List[str]] = None):
        super().__init__(model=Media, excludes=excludes)
