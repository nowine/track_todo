from typing import TypeVar, Type, Generic, List, Any, Dict, Optional, Union

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.database import Base

# Define a generic type of Models, which must be bound under db `Base` class (sub-class of `Base`)
ModelType = TypeVar("ModelType", bound=Base)
# Define a generic type of Create Schema, which must be bound under pydantic BaseModel
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# Define a generic type of Update Schema, which must be bound under pydantic BaseModel
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# Create a Generics CRUDBase Class, which will use the ModelType, CreateSchemaType and UpdateSchemaType
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    # The initator of this class receives a model class (Type[ModelType] means the `model` must be a class under ModelType)
    def __init__(self, model: Type[ModelType]):
        self.model = model # The CRUD class will use this model to create instance to operate with DB

    # Get single record by "id"
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    # Get multiple records (default no other filtering criteria)
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    # Generic creation of records, receive CreateSchemaType
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in) # convert the Pydantic BaseModel data structure to an json compatible structure, which could be a dict
        #obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data) # Use the dict to create new instance of model, remember, model is a class. So here it is calling model`s initiator
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Generic update of record, assume the db object is already retrieved, and it should support using UpdateSchemaType or dict to pass the updated data
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj) # Convert the db_obj (instance of model) into a dict-like structure
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Generic removal of record
    def remove(self, db: Session, *, id: int) -> Dict[Any, Any]:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return jsonable_encoder(obj)