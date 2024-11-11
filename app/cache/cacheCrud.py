from typing import Any, Dict, Optional, Union, Type, List, TypeVar
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.cache.cacheModule import CacheModule
from app.db.dbCrud import DBOperations, DBModelType
from app.core.serializer import JSONSerializer


DBModelType = TypeVar("DBModelType")

class DBOperationsWithCache(DBOperations):
    def __init__(
        self,
        model: Type[DBModelType],
        detail_mappings: Optional[Dict[str, Any]] = {},
        model_entity_params: Optional[Dict[str, Any]] = {},
        excludes: Optional[List[str]] = [],
        cache_crud: Optional[CacheModule] = None,
        model_registry: Optional[Dict[str, Type[BaseModel]]] = None,
        cache_expiry: Optional[int] = 300,
        *args,
        **kwargs,
    ):
        # Call the parent constructor
        super().__init__(
            model=model,
            detail_mappings=detail_mappings,
            model_entity_params=model_entity_params,
            excludes=excludes,
            *args,
            **kwargs,
        )
        self.cache_crud = cache_crud  # CacheModule instance for caching
        self.model_registry = model_registry or {}  # Registry for model deserialization
        self.cache_expiry = cache_expiry  # Cache expiry time

    async def get(
        self,
        db_session: AsyncSession,
        id: Union[UUID, int, str],
        skip: int = 0,
        limit: int = 100,
    ) -> Optional[DBModelType]:
        cache_key = f"{self.model.__name__}:{id}"
        cached_data = None

        if self.cache_crud:
            cached_data = await self.cache_crud.get(cache_key)

        if cached_data:
            print(f"Cache hit for {cache_key}")
            return JSONSerializer.deserialize(cached_data, self.model_registry)

        print(f"Cache miss for {cache_key}")
        db_obj = await super().get(db_session, id, skip, limit)

        if self.cache_crud and db_obj:
            serialized_data = JSONSerializer.serialize(db_obj)
            await self.cache_crud.set(cache_key, serialized_data, expire=self.cache_expiry)

        return db_obj

    async def get_all(
        self, db_session: AsyncSession, offset: int = 0, limit: int = 100
    ) -> List[DBModelType]:
        cache_key = f"{self.model.__name__}:all:{offset}:{limit}"
        cached_data = None

        if self.cache_crud:
            cached_data = await self.cache_crud.get(cache_key)

        if cached_data:
            print(f"Cache hit for {cache_key}")
            return [JSONSerializer.deserialize(item, self.model_registry) for item in cached_data]

        print(f"Cache miss for {cache_key}")
        db_objs = await super().get_all(db_session, offset, limit)

        if self.cache_crud and db_objs:
            serialized_data = [JSONSerializer.serialize(obj) for obj in db_objs]
            await self.cache_crud.set(cache_key, serialized_data, expire=self.cache_expiry)

        return db_objs

    async def create(
        self,
        db_session: AsyncSession,
        obj_in: Union[Dict[str, Any], BaseModel, Any],
    ) -> DBModelType:
        print("About to create")
        db_obj = await super().create(db_session, obj_in)
        print("Created")
        if self.cache_crud:
            cache_key = f"{self.model.__name__}:{getattr(db_obj, self.primary_key)}"
            print("About to serialize", cache_key)
            serialized_data = JSONSerializer.serialize(db_obj)
            print("About to cache")
            await self.cache_crud.set(cache_key, serialized_data, expire=self.cache_expiry)

        return db_obj

    async def create_or_update(
        self,
        db_session: AsyncSession,
        obj_in: Union[Dict[str, Any], DBModelType],
        filters: Optional[Dict[str, Any]] = None,
        update_existing: bool = True,
    ) -> DBModelType:
        db_obj = await super().create_or_update(db_session, obj_in, filters, update_existing)

        if self.cache_crud:
            cache_key = f"{self.model.__name__}:{getattr(db_obj, self.primary_key)}"
            serialized_data = JSONSerializer.serialize(db_obj)
            await self.cache_crud.set(cache_key, serialized_data, expire=self.cache_expiry)

        return db_obj

    async def update(
        self, db_session: AsyncSession, db_obj: DBModelType, obj_in: Dict[str, Any]
    ) -> DBModelType:
        db_obj = await super().update(db_session, db_obj, obj_in)

        if self.cache_crud:
            cache_key = f"{self.model.__name__}:{getattr(db_obj, self.primary_key)}"
            serialized_data = JSONSerializer.serialize(db_obj)
            await self.cache_crud.set(cache_key, serialized_data, expire=self.cache_expiry)

        return db_obj

    async def delete(
        self, db_session: AsyncSession, db_obj: DBModelType
    ) -> DBModelType:
        if self.cache_crud:
            cache_key = f"{self.model.__name__}:{getattr(db_obj, self.primary_key)}"
            await self.cache_crud.delete(cache_key)

        return await super().delete(db_session, db_obj)

    async def query(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single: bool = False,
        options: Optional[List[InstrumentedAttribute]] = None,
        order_by: Optional[List[InstrumentedAttribute]] = None,
    ) -> Union[List[DBModelType], Optional[DBModelType]]:
        cache_key = f"{self.model.__name__}:query:{str(filters)}:{single}:{str(options)}:{str(order_by)}"
        cached_data = None

        if self.cache_crud:
            cached_data = await self.cache_crud.get(cache_key)

        if cached_data:
            print(f"Cache hit for {cache_key}")
            deserialized_data = [JSONSerializer.deserialize(item, self.model_registry) for item in cached_data]
            return deserialized_data if not single else deserialized_data[0]

        print(f"Cache miss for {cache_key}")
        db_objs = await super().query(db_session, filters, single, options, order_by)

        if self.cache_crud and db_objs:
            if isinstance(db_objs, list):
                serialized_data = [JSONSerializer.serialize(obj) for obj in db_objs]
            else:
                serialized_data = [JSONSerializer.serialize(db_objs)]
            await self.cache_crud.set(cache_key, serialized_data, expire=self.cache_expiry)

        return db_objs
    

     # Add the query_on_joins method
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
        """
        Executes a query with join conditions using the cache-aware CRUD operations.
        """
        cache_key = f"{self.model.__name__}:joins:{filters}:{skip}:{limit}"
        if self.cache_crud:
            cached_data = await self.cache_crud.get(cache_key)
            if cached_data:
                print(f"Cache hit for {cache_key}")
                return JSONSerializer.deserialize(cached_data, self.model_registry)

        # Perform the query if no cache hit
        result = await super().query_on_joins(
            db_session, filters, single, options, order_by, join_conditions, skip, limit
        )

        # Cache the result
        if self.cache_crud and result:
            serialized_data = JSONSerializer.serialize(result)
            await self.cache_crud.set(cache_key, serialized_data, expire=self.cache_expiry)

        return result

    # Add the query_on_create method
    async def query_on_create(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single: bool = False,
        options: Optional[List[InstrumentedAttribute]] = None,
        create_if_not_exist: bool = False,
    ) -> Optional[DBModelType]:
        """
        Executes a query, and optionally creates an entry if it does not exist, using the cache-aware CRUD operations.
        """
        cache_key = f"{self.model.__name__}:query_on_create:{filters}"
        if self.cache_crud:
            cached_data = await self.cache_crud.get(cache_key)
            if cached_data:
                print(f"Cache hit for {cache_key}")
                return JSONSerializer.deserialize(cached_data, self.model_registry)

        # Perform the query if no cache hit
        result = await super().query_on_create(
            db_session, filters, single, options, create_if_not_exist
        )
