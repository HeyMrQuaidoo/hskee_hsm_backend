import json
from uuid import UUID
from sqlalchemy import Enum
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.ext.declarative import DeclarativeMeta
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
        detail_mappings: Optional[Dict[str, Any]] = {},
        model_entity_params: Optional[Dict[str, Any]] = {},
        excludes: Optional[List[str]] = [],
        model_registry: Optional[Dict[str, Type[BaseModel]]] = None,
        cache_expiry: Optional[int] = 300,
        *args,
        **kwargs,
    ):
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

    def handle_special_types(self, value):
        """Helper function to handle special non-serializable types."""
        if isinstance(value, UUID):
            return str(value)
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, Decimal):
            return float(value)
        elif isinstance(value, Enum):
            return str(value.name)
        elif isinstance(value, list):
            return [self.handle_special_types(v) for v in value]
        elif isinstance(value.__class__, DeclarativeMeta):
            return self.serialize(value)
        else:
            try:
                json.dumps(value)
                return value
            except TypeError:
                return str(value)

    def serialize(self, obj):
        """Custom function to serialize SQLAlchemy models and handle complex data types."""
        if isinstance(obj.__class__, DeclarativeMeta):
            obj_dict = {}
            for c in inspect(obj).mapper.column_attrs:
                value = getattr(obj, c.key)
                obj_dict[c.key] = self.handle_special_types(value)
            return obj_dict  # Return as dict instead of JSON string
        elif isinstance(obj, list):
            return [self.serialize(item) for item in obj]
        else:
            return self.handle_special_types(obj)

    def unserialize(self, data, model_class=None):
        """Custom function to unserialize data back to SQLAlchemy model instances or Python dictionaries."""
        data_dict = data  # Data is already a dict

        if model_class and isinstance(data_dict, dict):
            for key, value in data_dict.items():
                if isinstance(value, str):
                    try:
                        data_dict[key] = datetime.fromisoformat(value)
                    except ValueError:
                        pass

            return model_class(**data_dict)
        elif model_class and isinstance(data_dict, list):
            return [model_class(**item) for item in data_dict]

        return data_dict

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
                JSONSerializer.deserialize(cached_object) if cached_object else None
            )

        if cached_data:
            return self.unserialize(cached_data, model_class=self.model)

        db_obj = await super().get(db_session, id, skip, limit)

        if self.cache_crud and db_obj:
            serialized_data = self.serialize(db_obj)
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(serialized_data),
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
                # Fetch items from cache
                cached_objs = []
                missing_ids = []
                for id in cached_ids:
                    cache_key = f"{self.model.__name__}:{id}"
                    cached_object = await self.cache_crud.get(cache_key)
                    if cached_object:
                        cached_data = JSONSerializer.deserialize(cached_object)
                        cached_objs.append(
                            self.unserialize(cached_data, model_class=self.model)
                        )
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
                serialized_data = self.serialize(obj)
                await self.cache_crud.set(
                    cache_key,
                    JSONSerializer.serialize(serialized_data),
                    expire=self.cache_expiry,
                )
                await self.cache_crud.sadd(ids_cache_key, obj_id)
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
            serialized_data = self.serialize(db_obj)
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(serialized_data),
                expire=self.cache_expiry,
            )
            ids_cache_key = f"{self.model.__name__}:ids"
            await self.cache_crud.sadd(ids_cache_key, obj_id)
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
            serialized_data = self.serialize(db_obj)
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(serialized_data),
                expire=self.cache_expiry,
            )
            ids_cache_key = f"{self.model.__name__}:ids"
            await self.cache_crud.sadd(ids_cache_key, obj_id)
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
            await self.cache_crud.srem(ids_cache_key, obj_id)
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
            serialized_data = self.serialize(db_obj)
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(serialized_data),
                expire=self.cache_expiry,
            )
            ids_cache_key = f"{self.model.__name__}:ids"
            await self.cache_crud.sadd(ids_cache_key, obj_id)
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
        filters_str = json.dumps(filters, sort_keys=True)
        cache_key = f"{self.model.__name__}:query:{filters_str}:{single}"

        if self.cache_crud:
            cached_object = await self.cache_crud.get(cache_key)
            if cached_object:
                cached_data = JSONSerializer.deserialize(cached_object)
                if single:
                    return self.unserialize(cached_data, model_class=self.model)
                else:
                    return [
                        self.unserialize(obj, model_class=self.model)
                        for obj in cached_data
                    ]

        db_objs = await super().query(db_session, filters, single, options, order_by)

        if self.cache_crud and db_objs:
            if single:
                serialized_data = self.serialize(db_objs)
                await self.cache_crud.set(
                    cache_key,
                    JSONSerializer.serialize(serialized_data),
                    expire=self.cache_expiry,
                )
            else:
                serialized_data = [self.serialize(obj) for obj in db_objs]
                await self.cache_crud.set(
                    cache_key,
                    JSONSerializer.serialize(serialized_data),
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
        filters_str = json.dumps(filters, sort_keys=True)
        cache_key = f"{self.model.__name__}:joins:{filters_str}:{single}:{skip}:{limit}"

        if self.cache_crud:
            cached_object = await self.cache_crud.get(cache_key)
            if cached_object:
                cached_data = JSONSerializer.deserialize(cached_object)
                if single:
                    return self.unserialize(cached_data, model_class=self.model)
                else:
                    return [
                        self.unserialize(obj, model_class=self.model)
                        for obj in cached_data
                    ]

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
            if single:
                serialized_data = self.serialize(db_objs)
                await self.cache_crud.set(
                    cache_key,
                    JSONSerializer.serialize(serialized_data),
                    expire=self.cache_expiry,
                )
            else:
                serialized_data = [self.serialize(obj) for obj in db_objs]
                await self.cache_crud.set(
                    cache_key,
                    JSONSerializer.serialize(serialized_data),
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
        filters_str = json.dumps(filters, sort_keys=True)
        cache_key = (
            f"{self.model.__name__}:query_on_create:{filters_str}:{single}:"
            f"{create_if_not_exist}"
        )

        if self.cache_crud:
            cached_object = await self.cache_crud.get(cache_key)
            if cached_object:
                cached_data = JSONSerializer.deserialize(cached_object)
                return self.unserialize(cached_data, model_class=self.model)

        db_obj = await super().query_on_create(
            db_session,
            filters,
            single,
            options,
            create_if_not_exist,
        )

        if self.cache_crud and db_obj:
            serialized_data = self.serialize(db_obj)
            await self.cache_crud.set(
                cache_key,
                JSONSerializer.serialize(serialized_data),
                expire=self.cache_expiry,
            )

        return db_obj
