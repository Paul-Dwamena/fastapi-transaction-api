

import asyncio

#a message queue system like rabbitmq to process these tasks
async def update_user_stats(user_id, average_transaction_value):
    try:
        # Simulate updating user statistics (e.g., in a database)
        await asyncio.sleep(5)  # Simulate some processing time
        print(f"Updated user statistics for user_id: {user_id}")
    except Exception as e:
        print(f"Error updating user statistics: {str(e)}")
