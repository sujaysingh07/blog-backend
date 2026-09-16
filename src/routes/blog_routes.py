from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from src.dto.blog_schema import BlogSchema, BlogResponseSchema, BlogUpdateSchema
from src.controller import blog_controller, auth_controller
from src.utils.db import get_db
from typing import List, Optional

blog_router = APIRouter(prefix="/blogs", tags=["Blogs"])


@blog_router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[BlogResponseSchema]
)
def get_all_blog(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    search: Optional[str] = Query(None, max_length=50, description="Search term for blog title or content"),
    db: Session = Depends(get_db),
    current_user=Depends(auth_controller.get_current_user),
):
    return blog_controller.get_blog(skip, limit, db,search)


@blog_router.get(
    "/public", status_code=status.HTTP_200_OK, response_model=List[BlogResponseSchema]
)
def get_published_blogs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    search: Optional[str] = Query(None, max_length=50, description="Search term for blog title or content"),
    db: Session = Depends(get_db),
):
    return blog_controller.get_published_blogs(skip, limit, db, search)


@blog_router.get(
    "/public/{id}", status_code=status.HTTP_200_OK, response_model=BlogResponseSchema
)
def get_published_blog(
    id: int,
    db: Session = Depends(get_db),
):
    return blog_controller.get_published_blog_by_id(id, db)


@blog_router.post(
    "", response_model=BlogResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_blog(
    blog_data: BlogSchema,
    db: Session = Depends(get_db),
    current_user=Depends(auth_controller.get_current_user),
):
    return blog_controller.create_blog(blog_data, db)


@blog_router.put(
    "/{id}", status_code=status.HTTP_200_OK, response_model=BlogResponseSchema
)
def update_blog(
    id: int,
    body: BlogUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(auth_controller.get_current_user),
):
    return blog_controller.update_blog(id, body, db)


@blog_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_blog(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth_controller.get_current_user),
):
    return blog_controller.delete_blog(id, db)


@blog_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_blog(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth_controller.get_current_user),
):
    return blog_controller.get_blog_by_id(id, db)
