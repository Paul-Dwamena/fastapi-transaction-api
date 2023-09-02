from .schema import Transaction  # Import your Transaction model here


def gen_response(msg:str, data: dict = None, success:bool = False) -> dict:
    print('Message', msg)
    return {'message': msg, 'data': data, 'success': success}


class Api0Exception(Exception):
    def __init__(self, status_code: str,message:str):
        self.status_code = status_code
        self.message = message





def transaction_to_dict(transaction: Transaction):
    return {
        "id": transaction.id,
        "user_id": transaction.user_id,
        "full_name": transaction.full_name,
        "transaction_date": transaction.transaction_date,
        "transaction_amount": transaction.transaction_amount,
        "transaction_type": transaction.transaction_type.value  # Convert Enum to string
    }

