from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.task import TaskRepo
from app.schemas.task import TaskCreate, TaskResponse, TaskPatch
from app.models.user import User
from app.services.auth import get_current_user
from app.redis_client import redis_client
import json

router = APIRouter()

@router.get("/task")
async def get_all_users_tasks(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    cache_key = f"tasks:{user.id}:{limit}:{offset}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = TaskRepo(session)
    result = await repo.get_all_users_tasks(user.id, limit, offset)
    await redis_client.set(cache_key, json.dumps([
        {"id": t.id, "title": t.title, "status": t.status, "is_active": t.is_active}
         for t in result]), ex=300)

    return result 

@router.get("/task/{task_id}")
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    cache_key = f"task:{task_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = TaskRepo(session)
    result = await repo.get_by_id(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    if result.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await redis_client.set(cache_key, json.dumps({"id": result.id, "title": result.title, "status": result.status, "is_active": result.is_active}), ex=300)

    return result

@router.post('/task', status_code=201)
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
    keys = await redis_client.keys(f"tasks:{user.id}:*")
    if keys:
        await redis_client.delete(*keys)
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
    keys = await redis_client.keys(f"tasks:{user.id}:*")
    if keys:
        await redis_client.delete(*keys)
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
    keys = await redis_client.keys(f"tasks:{user.id}:*")
    if keys:
        await redis_client.delete(*keys)
    return 
    