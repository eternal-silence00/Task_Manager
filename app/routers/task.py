from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.task import TaskRepo
from app.schemas.task import TaskCreate, TaskResponse, TaskPatch
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/task")
async def get_all_users_tasks(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = TaskRepo(session)
    result = await repo.get_all_users_tasks(user.id)
    return result 

@router.get("/task/{task_id}")
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = TaskRepo(session)
    result = await repo.get_by_id(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    if result.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return result

@router.post('/task')
async def create_task(
    data: TaskCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    repo = TaskRepo(session)
    task = await repo.create_task(
        data=data,
        user_id=user.id
    )
    return task

@router.patch("/task/{task_id}")
async def patch_task(
    task_id: int,
    data: TaskPatch,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = TaskRepo(session)
    result = await repo.patch_tasks(
        task_id=task_id,
        data=data
        )
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    if result.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return result 

@router.delete("/task/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = TaskRepo(session)
    task = await repo.get_by_id(
        task_id=task_id
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await repo.delete_task(task_id)
    return 
    