
# FastAPI Assignment

This project is a FastAPI application that provides a set of RESTful APIs for managing clock-in records and items. The application utilizes MongoDB as its database and includes functionalities to create, read, update, and delete clock-in records and items.

## Features

- **Clock-In Records Management**: Create, retrieve, update, and delete clock-in records.
- **Items Management**: Create, retrieve, update, and delete items.
- **Filtering**: Filter clock-in records based on email, location, and insert date.
- **Input Validation**: Validates ObjectId format for MongoDB operations.

## Technologies Used

- FastAPI
- MongoDB
- Pydantic
- Uvicorn (ASGI server)
- Python 3.x

## Environment Variables

Create a `.env` file in the root directory of your project to store your MongoDB connection URL. 

1. **Create the `.env` file**:
   ```bash
   touch .env

2. **.Add the MongoDB connection URL**:
    Open the .env file and add the following line, replacing <your_mongo_url> with your actual MongoDB connection string:

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/Garima14Gupta/fastapi_assignment>
   cd fastapi_assignment
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```
   The application will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### Clock-In Endpoints

- **Create Clock-In Record**: `POST /clock-in`
  - **Request Body**: `ClockInRecord`
  - **Response**: `{ "id": "<inserted_id>" }`

- **Filter Clock-In Records**: `GET /clock-in/filter`
  - **Query Parameters**: 
    - `email` (Optional): Filter by email.
    - `location` (Optional): Filter by location.
    - `insert_date` (Optional): Filter by insert date (ISO format).

- **Retrieve Clock-In Record by ID**: `GET /clock-in/{id}`
  - **Path Parameter**: `id` (ObjectId of the clock-in record)
  - **Response**: `ClockInRecord`

- **Delete Clock-In Record by ID**: `DELETE /clock-in/{id}`
  - **Path Parameter**: `id` (ObjectId of the clock-in record)
  - **Response**: `{ "msg": "Clock-in record deleted" }`

- **Update Clock-In Record by ID**: `PUT /clock-in/{id}`
  - **Path Parameter**: `id` (ObjectId of the clock-in record)
  - **Request Body**: `UpdateClockIn`
  - **Response**: `{ "msg": "Clock-in record updated" }`

### Items Endpoints

- **Create Item**: `POST /items`
  - **Request Body**: `Item`
  - **Response**: `{ "id": "<inserted_id>" }`

- **Retrieve All Items**: `GET /items`
  - **Response**: `List[Item]`

- **Retrieve Item by ID**: `GET /items/{id}`
  - **Path Parameter**: `id` (ObjectId of the item)
  - **Response**: `Item`

- **Update Item by ID**: `PUT /items/{id}`
  - **Path Parameter**: `id` (ObjectId of the item)
  - **Request Body**: `UpdateItem`
  - **Response**: `{ "msg": "Item updated" }`

- **Delete Item by ID**: `DELETE /items/{id}`
  - **Path Parameter**: `id` (ObjectId of the item)
  - **Response**: `{ "msg": "Item deleted" }`

- **Filter Items**: `POST /items/filter`
  - **Query Parameters**: 
    - `email_id` (Optional): Filter by email_id .
    - `expiry_date` (Optional): Minimum expiry_date for filtering items.
    - `insert_date` (Optional): Minimum insert date for filtering items.
    - `quantity` (Optional): Minimum quantity for filtering items.

- **Aggregate Items**: `GET /items/aggregate`
  - **Response**: Aggregated data by email_id.


## Models

- **ClockInRecord**: Model for clock-in records.
- **UpdateClockIn**: Model for updating clock-in records.
- **Item**: Model for items.
- **UpdateItem**: Model for updating items.

## Database Setup

Make sure to have a MongoDB instance running. Update the database connection settings in the `database.py` file.

## License

This project is licensed under the MIT License.

## Acknowledgements

- FastAPI documentation: https://fastapi.tiangolo.com/
- MongoDB documentation: https://docs.mongodb.com/
