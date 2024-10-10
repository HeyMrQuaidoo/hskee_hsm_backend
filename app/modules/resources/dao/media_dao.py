from typing import List, Optional

# models
from app.modules.resources.models.media import Media

# dao
from app.modules.common.dao.base_dao import BaseDAO


class MediaDAO(BaseDAO[Media]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = Media

        self.detail_mappings = {}
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="media_id",
        )