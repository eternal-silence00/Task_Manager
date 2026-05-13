from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskPatch, TaskCreate

class TaskRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_id(self, task_id: int):
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()
    
    async def get_all_users_tasks(self, user_id: int, limit: int = 10, offset: int = 0):
        result = await self.session.execute(select(Task).where(Task.user_id == user_id).limit(limit).offset(offset))
        return result.scalars().all()
    
    async def patch_tasks(self, task: Task, data: TaskPatch):
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(task, key, value)
        return task 
    
    async def create_task(self, data: TaskCreate, user_id: int):
        task = Task(user_id = user_id,
                    title = data.title, 
                    description = data.description)
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task
    
    async def delete_task(self, task_id: int):
        task_to_del = await self.session.execute(select(Task).where(Task.id == task_id))
        task = task_to_del.scalar_one_or_none()
        await self.session.delete(task)
        await self.session.flush()
        return 