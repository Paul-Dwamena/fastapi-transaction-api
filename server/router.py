from fastapi import APIRouter, Response, Depends,HTTPException
from fastapi import status, Request
from .utils import *
from .schema import *
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from .background_tasks import *
import asyncio
from fastapi.responses import JSONResponse





router = APIRouter(
            prefix='/api/v1',
            tags=['Transactions Api'],
            responses={422: {"message": "Request failed"}}
         )
  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#create a transaction record
@router.post("/createtransaction", description='Generate user transaction',status_code=status.HTTP_202_ACCEPTED)
async def create_transaction(transaction: TransactionCreateModel, db: Session = Depends(get_db)):
    try:
        db_transaction = Transaction(
            user_id=transaction.user_id,
            full_name=transaction.full_name,
            transaction_date=transaction.transaction_date,
            transaction_amount=transaction.transaction_amount,
            transaction_type=transaction.transaction_type
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return {"message": "Transaction created successfully", "transaction": db_transaction}
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an exception
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    




#get all transaction records of a user
#I added a limit and a pagination feature so that there is query optimization for larger dataset
@router.get("/user/transactions/{user_id}",status_code=status.HTTP_200_OK)
async def get_user_transactions(user_id: int, db: Session = Depends(get_db),limit: int = 10, page: int = 1):
    try:
        skip = (page - 1) * limit
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.id).limit(limit).offset(skip).all()
        
        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found for this user")
        
        results = [
            TransactionModel(
                transaction_id=transaction.id,
                user_id=transaction.user_id,
                full_name=transaction.full_name,
                transaction_date=transaction.transaction_date,
                transaction_amount=transaction.transaction_amount,
                transaction_type=transaction.transaction_type,
            )
            for transaction in transactions
        ]

        return {"Status":"Success","Results":len(results),"Transactions":results}
    except HTTPException as http_exception:
        return http_exception  # Return the HTTPException as is

    except Exception as e:
       raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

    

# Update a transaction record
#Ideally we should be passing a more secured access tokens to the endpoint and not user ids.
@router.put("/update_transaction/{transaction_id}",status_code=status.HTTP_200_OK)
async def update_transaction(transaction_id: int,user_id:int,updated_transaction: UpdateModel,db: Session = Depends(get_db)):
    try:
        # Query the database to find the existing transaction record
        existing_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        

        # If the transaction record does not exist, raise a 404 error
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # check if transaction belongs to the specified user
        if existing_transaction.user_id != user_id:
            raise HTTPException(status_code=403,detail="Access forbidden: This transaction does not belong to the specified user")

        # Update the transaction record with the new data
        for key, value in updated_transaction.dict().items():
            setattr(existing_transaction, key, value)

        db.commit()
        db.refresh(existing_transaction)


        updated_transaction_dict = transaction_to_dict(existing_transaction)
        
        return {"message":"Transaction updated successfully","Updated_transaction":updated_transaction_dict}

    except HTTPException as http_exception:
        raise http_exception 
    

    except Exception as e:

        db.rollback()  # Rollback the transaction in case of an exception
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    




# Delete a transaction record
#Ideally we should be passing a more secured access tokens to the endpoint and not user ids.
@router.delete("/delete_transaction/{transaction_id}",status_code=status.HTTP_200_OK)
async def delete_transaction(transaction_id: int,user_id: int,db: Session = Depends(get_db)):
    try:
        # Query the database to find the existing transaction record
        existing_transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()

        # If the transaction record does not exist, raise a 404 error
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        # Delete the transaction record
        db.delete(existing_transaction)
        db.commit()

        return {"message": "Transaction deleted successfully"}

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/user_stats/{user_id}",description='Get user transaction statistics')
async def get_user_stats(user_id:int, db:Session=Depends(get_db)):
    try:

        avg_transaction_query = db.query(func.avg(Transaction.transaction_amount).label("average_transaction_value")).filter(
            Transaction.user_id == user_id
        )
        avg_transaction_result = avg_transaction_query.first()
        avg_transaction = avg_transaction_result.average_transaction_value or 0.0  # Set default to 0.0 if no transactions

        # Determine the day with the highest number of transactions
        max_transaction_day_query = db.query(
            func.date(Transaction.transaction_date).label("transaction_day"),
            func.count(Transaction.id).label("transaction_count")
        ).filter(
            Transaction.user_id == user_id
        ).group_by("transaction_day").order_by(func.count(Transaction.id).desc()).first()

        if max_transaction_day_query:
            max_transaction_day = max_transaction_day_query.transaction_day
        else:
            max_transaction_day = None


        # Enqueue background tasks for updating user statistics. By using this approach, non-urgent tasks are offloaded to the background, improving the responsiveness of your get_user_stats endpoint
        asyncio.create_task(update_user_stats(user_id, avg_transaction))

        return {
            "user_id": user_id,
            "average_transaction_value": avg_transaction,
            "day_with_highest_transactions": max_transaction_day
        }

 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=f"Internal server error: {str(e)}")















