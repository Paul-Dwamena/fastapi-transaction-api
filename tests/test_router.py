from fastapi.testclient import TestClient
from main import app
from fastapi import status
from unittest.mock import patch
from server.router import get_db
client=TestClient(app)



def test_create_transaction():
    sample_payload = {
        "user_id": 1,
        "full_name": "Paul Dwamena",
        "transaction_date": "2023-09-02T11:32:11.614Z",
        "transaction_amount": 2000,
        "transaction_type": "credit"
    }

    response = client.post("/api/v1/createtransaction", json=sample_payload)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert "id" in response.json()["transaction"]  # Ensure that "id" is present in the response
    assert response.json()["transaction"]["user_id"] == 1
    assert response.json()["transaction"]["full_name"] == "Paul Dwamena"
    assert response.json()["transaction"]["transaction_date"] == "2023-09-02T11:32:11.614000"
    assert response.json()["transaction"]["transaction_amount"] == 2000.0
    assert response.json()["transaction"]["transaction_type"] == "credit"


def test_get_user_transactions():
    # Assuming you have a user with ID 1 and some transactions in the database
    user_id = 1
    page = 1
    limit = 10

    response = client.get(f"/api/v1/user/transactions/{user_id}?page={page}&limit={limit}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["Status"] == "Success"
    
    # Check the structure of the response JSON
    assert "Transactions" in response.json()
    assert "Results" in response.json()  # Check if "Results" field is present
    assert isinstance(response.json()["Transactions"], list)
    assert isinstance(response.json()["Results"], int)  # Check if "Results" is an integer
    
    transactions = response.json()["Transactions"]
    results = response.json()["Results"]  # Get the value of "Results" field

    # Check each transaction object in the list
    for transaction in transactions:
        assert "transaction_id" in transaction
        assert "user_id" in transaction
        assert "full_name" in transaction
        assert "transaction_date" in transaction
        assert "transaction_amount" in transaction
        assert "transaction_type" in transaction

        # Check specific data content for each field
        assert isinstance(transaction["transaction_id"], int)
        assert isinstance(transaction["user_id"], int)
        assert isinstance(transaction["full_name"], str)
        assert isinstance(transaction["transaction_date"], str)  # Depending on your data format
        assert isinstance(transaction["transaction_amount"], float)  # Depending on your data format
        assert isinstance(transaction["transaction_type"], str)  # Depending on your data format

    # Check if the total number of transactions matches the "Results" value
    assert len(transactions) == results



def test_get_user_transactions_with_no_transactions():
    # Assuming you have a user with ID 999 (an ID that has no transactions in the database)
    user_id = 999
    page = 1
    limit = 10

    response = client.get(f"/api/v1/user/transactions/{user_id}?page={page}&limit={limit}")

    assert response.json()['status_code']== 404
    assert response.json()["detail"] == "No transactions found for this user"



def test_delete_transaction_transactionid_notfound():
    # Assuming you have a user ID and a transaction ID
    user_id = 1
    transaction_id = 123
    response = client.delete(f"/api/v1/delete_transaction/{transaction_id}?user_id={user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"

   


def test_delete_transaction():
    # Assuming you have a transaction ID and user ID
    transaction_id = 15
    user_id = 1

    # Test case 1: Successful deletion
    response = client.delete(f"/api/v1/delete_transaction/{transaction_id}?user_id={user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Transaction deleted successfully"}




def test_update_transaction():
    # Assuming you have a transaction ID, user ID, and an updated_transaction dictionary
    transaction_id = 13
    user_id = 1
    updated_transaction_data = {
        "transaction_date": "2023-09-02T17:26:19.914000",
        "transaction_amount": 9000.0,
        "transaction_type":"debit"
        # Add more fields as needed to match your UpdateModel
    }
    
    # Test case 1: Successful update
    response = client.put(
        f"/api/v1/update_transaction/{transaction_id}?user_id={user_id}",
        json=updated_transaction_data
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Transaction updated successfully"

    # You can also add assertions to verify the updated data
    updated_transaction = response.json()["Updated_transaction"]
    for key, value in updated_transaction_data.items():
        assert updated_transaction[key] == value

    # Test case 2: Transaction not found (404 error)
    # simulate this by having a transaction_id that doesn't exist
    response = client.put(
        f"/api/v1/update_transaction/999?user_id={user_id}",
        json=updated_transaction_data
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Transaction not found"}

    # Test case 3: Access forbidden (403 error)
    # Simulate this by providing a user_id that doesn't match the transaction's user_id
    response = client.put(
        f"/api/v1/update_transaction/{transaction_id}?user_id=2",
        json=updated_transaction_data
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access forbidden: This transaction does not belong to the specified user"}




def test_get_user_stats_with_real_database():
    # Assuming you have a user ID and test data in your database
    user_id = 1
    
 

    # Test the get_user_stats endpoint
    response = client.get(f"/api/v1/user_stats/{user_id}")
    
    # Assert the response status code and structure
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert "user_id" in response_json
    assert "average_transaction_value" in response_json
    assert "day_with_highest_transactions" in response_json
