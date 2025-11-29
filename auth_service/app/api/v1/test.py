"""
Test API endpoints for verifying database and FastAPI functionality.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.test_item import TestItem
from app.schemas.test_item import TestItemCreate, TestItemResponse

router = APIRouter(prefix="/test", tags=["test"])


@router.post("/items", response_model=TestItemResponse, status_code=status.HTTP_201_CREATED)
def create_test_item(
    item: TestItemCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new test item.

    This endpoint tests:
    - Database write operations
    - Request validation via Pydantic
    - Response serialization
    """
    db_item = TestItem(
        title=item.title,
        description=item.description,
        is_active=item.is_active
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items", response_model=List[TestItemResponse])
def get_all_test_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all test items with pagination.

    This endpoint tests:
    - Database read operations
    - Query pagination
    - Multiple record serialization
    """
    items = db.query(TestItem).offset(skip).limit(limit).all()
    return items


@router.get("/items/{item_id}", response_model=TestItemResponse)
def get_test_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific test item by ID.

    This endpoint tests:
    - Database read by ID
    - 404 error handling
    - Single record serialization
    """
    item = db.query(TestItem).filter(TestItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test item with id {item_id} not found"
        )
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a test item by ID.

    This endpoint tests:
    - Database delete operations
    - 404 error handling
    """
    item = db.query(TestItem).filter(TestItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test item with id {item_id} not found"
        )
    db.delete(item)
    db.commit()
    return None


@router.get("/db-check")
def database_check(db: Session = Depends(get_db)):
    """
    Quick database connectivity check.

    Returns the count of test items in the database.
    """
    try:
        count = db.query(TestItem).count()
        return {
            "status": "success",
            "message": "Database connection successful",
            "test_items_count": count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
