from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, validator

from .user import User
from .project import Project

'''
@validator是pydantic的验证器修饰符，validator需作用于类函数（传入cls，而不是self）。
@validator传入参数包括：
    1. 需要验证的字段名，可以多个
    2. 验证的方法以及被调用的时间点，比如pre=True，表示这个验证器需要在标准验证器调用前调用；
对应的类函数用于实现判断逻辑。除了做判断校验，validator也可以用于字段初始化。
'''
class ItemBase(BaseModel):
    subject: str
    target_completion: Optional[datetime] = None
    effort_unit: Optional[str] = None
    effort_count: Optional[int] = None
    detail: Optional[str] = None
    owner_id: int
    creator_id: int
    # last_updater_id: int
    parent_id: Optional[int] = None
    project_id: Optional[int] = None
    status: str


class ItemCreate(ItemBase):
    last_updater_id: Optional[int] = None
    '''
    @validator('last_updater_id', pre=True)
    def default_last_updater_id(cls, v: Optional[int], values: Dict[str, Any]) -> Any:
        #Validate if last_updater_id is provided, if not, then format it as creator_id 
        if v is not None:
            print('last_updater_id is provided')
            return v
        elif 'creator_id' in values and isinstance(values['creator_id'], int):
            print('creator_id is %d' % creator_id)
            return values['creator_id']
        else:
            raise ValueError('last_updator_id must be provided')
    '''

class ItemUpdate(ItemBase):
    id: int 
    last_updater_id: int

    #TODO - Need to add validator to ensure last_updater_id is provided for update. 

    
class ItemDeleted(ItemUpdate):
    '''
    Added this deleted schema because the deleted item will be detached from the session, so could no more use
    the relationship to get the owner/creator/project/parent/children information into response. 

    This is a tactical solution, and this could already help to re-create objects.

    TO-DO: Find the solution to use the session. 
    '''
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class Item(ItemUpdate):
    # id: int
    # last_updater_id: int
    created_at: datetime
    last_updated_by: datetime
    owner: User
    creator: User
    last_updater: User
    # Self-referring Type annotation, use the string for replacement first.
    # children: List['Item'] = []
    # parent: 'Item' = None
    # Do not specify children and parent with `Item` schema, otherwise, it will cause recursive loop trying to extract the parent's children' parent...
    children: List[Any] = []
    parent: Optional[Any] = None 
    project: Optional[Project] = None
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

# And after defining the "Item" schema, use the below function to "replace" the 
# string value `Item` with the real Class
# Item.update_forward_refs()