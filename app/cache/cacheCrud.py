import json
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from typing import Any, Dict, Optional, Union, Type, List

# db
from app.db.dbCrud import DBOperations, DBModelType

# core
from app.core.lifespan import cache_manager
from app.core.serializer import JSONSerializer


class DBOperationsWithCache(DBOperations):
    def __init__(
        self,
        model: Type[DBModelType],
        detail_mappings: Optional[Dict[str, Any]] = None,
        model_entity_params: Optional[Dict[str, Any]] = None,
        excludes: Optional[List[str]] = None,
        model_registry: Optional[Dict[str, Type[BaseModel]]] = None,
        cache_expiry: Optional[int] = 300,
        *args,
        **kwargs,
    ):
        if detail_mappings is None:
            detail_mappings = {}
        if model_entity_params is None:
            model_entity_params = {}
        if excludes is None:
            excludes = []

        super().__init__(
            model=model,
            detail_mappings=detail_mappings,
            model_entity_params=model_entity_params,
            excludes=excludes,
            *args,
            **kwargs,
        )
        self.cache_crud = None  # Initialize as None
        self.model_registry = model_registry or {}
        self.cache_expiry = cache_expiry

    async def _initialize_cache(self):
        """Ensure cache_crud is properly initialized asynchronously."""
        if not self.cache_crud:
            cache_module = await cache_manager.cache_module
            self.cache_crud = cache_module

    async def get(
        self,
        db_session: AsyncSession,
        id: Union[UUID, int, str],
        skip: int = 0,
        limit: int = 100,
    ) -> Optional[DBModelType]:
        await self._initialize_cache()
        cache_key = f"{self.model.__name__}:{id}"
        cached_data = None

        if self.cache_crud:
            cached_object = await self.cache_crud.get(cache_key)
            cached_data = (
                JSONSerializer.deserialize(cached_object, model_class=self.model)
                if cached_object
                else None
            )

        if cached_data:
            return cached_data

        db_obj = await super().get(db_session, id, skip, limit)

        if self.cache_crud and db_obj:
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(db_obj),
                expire=self.cache_expiry,
            )

        return db_obj

    async def get_all(
        self, db_session: AsyncSession, offset: int = 0, limit: int = 100
    ) -> List[DBModelType]:
        await self._initialize_cache()
        ids_cache_key = f"{self.model.__name__}:ids"

        if self.cache_crud:
            cached_ids = await self.cache_crud.smembers(ids_cache_key)
            if cached_ids:
                # Convert cached_ids to a set of strings
                cached_ids = {
                    id.decode("utf-8") if isinstance(id, bytes) else str(id)
                    for id in cached_ids
                }
                # Fetch items from cache
                cached_objs = []
                missing_ids = []
                for id in cached_ids:
                    cache_key = f"{self.model.__name__}:{id}"
                    cached_object = await self.cache_crud.get(cache_key)
                    if cached_object:
                        cached_data = JSONSerializer.deserialize(
                            cached_object, model_class=self.model
                        )
                        cached_objs.append(cached_data)
                    else:
                        missing_ids.append(id)

                if not missing_ids:
                    # All items found in cache
                    return cached_objs[offset : offset + limit]

        # Cache miss or partial miss
        db_objs = await super().get_all(db_session, offset, limit)

        if self.cache_crud and db_objs:
            # Update cache
            for obj in db_objs:
                obj_id = getattr(obj, self.primary_key)
                cache_key = f"{self.model.__name__}:{obj_id}"
                await self.cache_crud.set(
                    cache_key,
                    JSONSerializer.serialize(obj),
                    expire=self.cache_expiry,
                )
                await self.cache_crud.sadd(ids_cache_key, str(obj_id))
            await self.cache_crud.expire(ids_cache_key, self.cache_expiry)

        return db_objs

    async def create(
        self,
        db_session: AsyncSession,
        obj_in: Union[Dict[str, Any], BaseModel, Any],
    ) -> DBModelType:
        await self._initialize_cache()
        db_obj = await super().create(db_session, obj_in)
        if self.cache_crud and db_obj:
            obj_id = getattr(db_obj, self.primary_key)
            cache_key = f"{self.model.__name__}:{obj_id}"
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(db_obj),
                expire=self.cache_expiry,
            )
            ids_cache_key = f"{self.model.__name__}:ids"
            await self.cache_crud.sadd(ids_cache_key, str(obj_id))
            await self.cache_crud.expire(ids_cache_key, self.cache_expiry)
        return db_obj

    async def update(
        self, db_session: AsyncSession, db_obj: DBModelType, obj_in: Dict[str, Any]
    ) -> DBModelType:
        await self._initialize_cache()
        db_obj = await super().update(db_session, db_obj, obj_in)

        if self.cache_crud and db_obj:
            obj_id = getattr(db_obj, self.primary_key)
            cache_key = f"{self.model.__name__}:{obj_id}"
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(db_obj),
                expire=self.cache_expiry,
            )
            ids_cache_key = f"{self.model.__name__}:ids"
            await self.cache_crud.sadd(ids_cache_key, str(obj_id))
            await self.cache_crud.expire(ids_cache_key, self.cache_expiry)

        return db_obj

    async def delete(
        self, db_session: AsyncSession, db_obj: DBModelType
    ) -> DBModelType:
        await self._initialize_cache()
        if self.cache_crud and db_obj:
            obj_id = getattr(db_obj, self.primary_key)
            cache_key = f"{self.model.__name__}:{obj_id}"
            await self.cache_crud.delete(cache_key)
            ids_cache_key = f"{self.model.__name__}:ids"
            await self.cache_crud.srem(ids_cache_key, str(obj_id))
        return await super().delete(db_session, db_obj)

    async def create_or_update(
        self,
        db_session: AsyncSession,
        obj_in: Union[Dict[str, Any], DBModelType],
        filters: Optional[Dict[str, Any]] = None,
        update_existing: bool = True,
    ) -> DBModelType:
        await self._initialize_cache()
        db_obj = await super().create_or_update(
            db_session, obj_in, filters, update_existing
        )

        if self.cache_crud and db_obj:
            obj_id = getattr(db_obj, self.primary_key)
            cache_key = f"{self.model.__name__}:{obj_id}"
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(db_obj),
                expire=self.cache_expiry,
            )
            ids_cache_key = f"{self.model.__name__}:ids"
            await self.cache_crud.sadd(ids_cache_key, str(obj_id))
            await self.cache_crud.expire(ids_cache_key, self.cache_expiry)
        return db_obj

    async def query(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single: bool = False,
        options: Optional[List[InstrumentedAttribute]] = None,
        order_by: Optional[List[InstrumentedAttribute]] = None,
    ) -> Union[List[DBModelType], Optional[DBModelType]]:
        await self._initialize_cache()
        # Generate a cache key based on filters
        filters_str = json.dumps(filters, sort_keys=True, default=str)
        cache_key = f"{self.model.__name__}:query:{filters_str}:{single}"

        if self.cache_crud:
            cached_object = await self.cache_crud.get(cache_key)
            if cached_object:
                cached_data = JSONSerializer.deserialize(cached_object)
                if single:
                    return self.model(**cached_data)
                else:
                    return [self.model(**item) for item in cached_data]

        db_objs = await super().query(db_session, filters, single, options, order_by)

        if self.cache_crud and db_objs:
            if single:
                await self.cache_crud.set(
                    cache_key,
                    JSONSerializer.serialize(db_objs),
                    expire=self.cache_expiry,
                )
            else:
                await self.cache_crud.set(
                    cache_key,
                    JSONSerializer.serialize(db_objs),
                    expire=self.cache_expiry,
                )
        return db_objs

    async def query_on_joins(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single: bool = False,
        options: Optional[List[InstrumentedAttribute]] = None,
        order_by: Optional[List[InstrumentedAttribute]] = None,
        join_conditions: Optional[List] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Union[List[DBModelType], Optional[DBModelType]]:
        await self._initialize_cache()
        # Generate a cache key based on filters
        filters_str = json.dumps(filters, sort_keys=True, default=str)
        cache_key = f"{self.model.__name__}:joins:{filters_str}:{single}:{skip}:{limit}"

        if self.cache_crud:
            cached_object = await self.cache_crud.get(cache_key)
            if cached_object:
                cached_data = JSONSerializer.deserialize(cached_object)
                if single:
                    return self.model(**cached_data)
                else:
                    return [self.model(**item) for item in cached_data]

        db_objs = await super().query_on_joins(
            db_session,
            filters,
            single,
            options,
            order_by,
            join_conditions,
            skip,
            limit,
        )

        if self.cache_crud and db_objs:
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(db_objs),
                expire=self.cache_expiry,
            )

        return db_objs

    async def query_on_create(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single: bool = False,
        options: Optional[List[InstrumentedAttribute]] = None,
        create_if_not_exist: bool = False,
    ) -> Optional[DBModelType]:
        await self._initialize_cache()
        # Generate a cache key based on filters
        filters_str = json.dumps(filters, sort_keys=True, default=str)
        cache_key = (
            f"{self.model.__name__}:query_on_create:{filters_str}:{single}:"
            f"{create_if_not_exist}"
        )

        if self.cache_crud:
            cached_object = await self.cache_crud.get(cache_key)
            if cached_object:
                cached_data = JSONSerializer.deserialize(cached_object)
                return self.model(**cached_data)

        db_obj = await super().query_on_create(
            db_session,
            filters,
            single,
            options,
            create_if_not_exist,
        )

        if self.cache_crud and db_obj:
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(db_obj),
                expire=self.cache_expiry,
            )

        return db_obj
