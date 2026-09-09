import datetime
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.model.blog_model import Blog
from src.dto.blog_schema import BlogSchema, BlogUpdateSchema


def get_blog(skip: int, limit: int, db: Session, search: Optional[str] = None):
    query = db.query(Blog)

    if search and search.strip():
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Blog.title.ilike(search_filter),
                Blog.body_content.ilike(search_filter),
                Blog.description.ilike(search_filter),
            )
        )

    all_blog = query.order_by(Blog.created_at.desc()).offset(skip).limit(limit).all()
    return all_blog


def create_blog(
    blog_data: BlogSchema,
    db: Session,
):
    existing_blog = db.query(Blog).filter(Blog.slug == blog_data.slug).first()

    if existing_blog:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A blog with this slug already exists",
        )

    # Create blog
    blog = Blog(
        title=blog_data.title.strip(),
        slug=blog_data.slug.strip(),
        description=blog_data.description.strip(),
        body_content=blog_data.body_content,
        status=blog_data.status,
        meta_title=(blog_data.meta_title.strip() if blog_data.meta_title else None),
        meta_description=(
            blog_data.meta_description.strip() if blog_data.meta_description else None
        ),
    )

    # Save to database
    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


def update_blog(blog_id: int, body: BlogUpdateSchema, db: Session):
    # 1. Retrieve the existing blog
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    # 2. Automatically manage published_at based on status changes
    if body.status is not None and body.status != blog.status:
        if body.status == "published":
            blog.published_at = datetime.datetime.now(datetime.timezone.utc)
        elif body.status == "draft":
            blog.published_at = None

    # 3. Extract only the fields the user explicitly sent in the request
    # Note: Use `body.dict(exclude_unset=True)` if you are using Pydantic V1
    update_data = body.model_dump(exclude_unset=True)

    # 4. Dynamically update the SQLAlchemy model attributes
    for key, value in update_data.items():
        setattr(blog, key, value)

    # 5. Save changes
    db.commit()
    db.refresh(blog)

    return blog


def delete_blog(blog_id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    db.delete(blog)

    db.commit()
    return {"details": "Blog Deleted Successfully!", "data": blog}


def get_blog_by_id(blog_id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    return blog
