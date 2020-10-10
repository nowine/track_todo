from .base import CRUDBase
from app.models import Item
from app.schemas import ItemCreate, ItemUpdate

class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass

item = CRUDItem(Item)