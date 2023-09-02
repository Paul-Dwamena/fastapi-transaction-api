FastAPI Transaction API

Table of Contents
Overview
Setup Instructions
Running the Application
Design and Architectural Decisions
Unit Test Instructions
Scaling Strategies



Overview
This is a FastAPI-based API for managing user transactions. It allows users to retrieve transaction records, update transactions, and perform other transaction-related operations.

Setup Instructions
Follow these steps to set up and run the FastAPI Transaction API:


1. git clone https://github.com/Paul-Dwamena/fastapi-transaction-api.git
2. cd fastapi-transaction-api
3. pip install -r requirements.txt
4. Database setup
  - I am using postgresql database setup for this test
5. Environmental variables setup
    DATABASE_URL=your_database_url but with this example, the database url has already been provided.
  
6. Running the application 
    docker-compose build
    docker-compose up


Design and Architectural Decisions
Technology Stack
FastAPI: A modern, fast (high-performance), web framework for building APIs with Python.
SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
Pydantic: Data validation and serialization using Python type hints.
psycopg2-binary: It allows you to establish connections to PostgreSQL databases from your Python code. You can connect to remote databases, authenticate, and establish a session for executing SQL queries

Error Handling
The application handles errors gracefully and returns appropriate HTTP status codes and error messages.


Unit Test Instructions
1. Make sure the server container is running and double check the server container name by running "docker ps"
2. Enter the container by running "docker exec -it 'container_name' bash
3. Now run pytest -v -s
NB. For a successful unit test run, make sure you are passing the right parameters(user ids, transaction ids) to the test functions and run your docker containers again


Scaling Strategies
The following scaling strategies can be considered when the transaction api grows so that it can serve a substantial user base:

1. Load Balancing: Use a load balancer to distribute incoming traffic across multiple application instances. This helps distribute the load and improves availability.

2. Horizontal Scaling: Add more server instances to handle increased traffic. Container orchestration platforms like Kubernetes can automate this process.

3. Caching: Implement caching mechanisms to store frequently accessed data and reduce database load. Use caching solutions like Redis or Memcached.

4. Asynchronous Processing: Offload non-urgent tasks (e.g., background processing, email notifications) to message queues and process them asynchronously. Use tools like RabbitMQ or Apache Kafka for this purpose.

5. Content Delivery Networks (CDNs): Use CDNs to cache and serve static assets (e.g., images, CSS, JavaScript) to reduce server load and improve content delivery speed.

6. Database Optimization: Continuously optimize database queries, indexes, and schema design to improve query performance.


