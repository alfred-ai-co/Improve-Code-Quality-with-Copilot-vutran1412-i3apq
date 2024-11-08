# Alfred AI FastAPI Project Management API

This project is a Project Management API built with FastAPI, SQLAlchemy, and SQLite. The API allows users to manage projects and their associated tickets.

## Folder Structure

```bash
app/
├── api/
│ ├── errors/
│ │ ├── http_error.py
│ │ ├── validation_error.py
│ ├── routes/
│ │ ├── api.py
│ │ ├── home.py
├── core/
│ ├── config.py
│ ├── events.py
├── db_models/
│ ├── base.py
│ ├── crud.py
│ ├── session.py
├── main.py
├── project_management.db
```

## .env Instructions

Create a `.env` file in the `app/` directory with the following contents:

```env
APP_ENV=dev
```

## Using the Dockerfile

### Build the Docker Image

To build the image, navigate to the root directory of the project and run:

```bash
docker build -t <image_name> .
```

### Run the Docker Image

To run the docker container with the environment variables, run:

```bash
docker run --env-file app/.env -p 8000:8000 <image_name>
```

This command will:

- Use the environment variables in the `.env` file
- Map the container's port 8000 to the host's port 8000
- Run the container in the background
- Start the FastAPI application with the `dev` flag for FastAPI (separate from the environment variable to enable debug mode)

# Project Management API Documentation

The Project Management API is designed to facilitate the management of projects and tickets within those projects. It provides a set of endpoints for creating, retrieving, updating, and deleting both projects and tickets.

## Endpoints

### Project Endpoints

| Operation                 | HTTP Method | Endpoint                 | Description                       |
| ------------------------- | ----------- | ------------------------ | --------------------------------- |
| **Create a new project**  | `POST`      | `/projects/`             | Create a new project              |
| **Retrieve a project**    | `GET`       | `/projects/{project_id}` | Retrieve a specific project by ID |
| **Update a project**      | `PUT`       | `/projects/{project_id}` | Update a specific project by ID   |
| **Delete a project**      | `DELETE`    | `/projects/{project_id}` | Delete a specific project by ID   |
| **Retrieve all projects** | `GET`       | `/projects/`             | Retrieve all projects             |

### Ticket Endpoints

| Operation                | HTTP Method | Endpoint               | Description                      |
| ------------------------ | ----------- | ---------------------- | -------------------------------- |
| **Create a new ticket**  | `POST`      | `/tickets/`            | Create a new ticket              |
| **Retrieve a ticket**    | `GET`       | `/tickets/{ticket_id}` | Retrieve a specific ticket by ID |
| **Update a ticket**      | `PUT`       | `/tickets/{ticket_id}` | Update a specific ticket by ID   |
| **Delete a ticket**      | `DELETE`    | `/tickets/{ticket_id}` | Delete a specific ticket by ID   |
| **Retrieve all tickets** | `GET`       | `/tickets/`            | Retrieve all tickets             |

## High-Level Overview

The Project Management API is built using FastAPI, SQLAlchemy, and SQLite. It follows a RESTful architecture, allowing clients to perform CRUD (Create, Read, Update, Delete) operations on projects and tickets.

### Data Flow

1. **Request Handling**: Clients send HTTP requests to the API endpoints.
2. **Dependency Injection**: The FastAPI framework uses dependency injection to provide a database session (`db`) to the endpoint functions.
3. **CRUD Operations**: The endpoint functions use CRUD classes (`ProjectCRUD`, `TicketCRUD`) to interact with the database.
4. **Database Operations**: The CRUD classes execute SQL queries using SQLAlchemy to perform the requested operations on the database.
5. **Response**: The results of the database operations are returned to the client as HTTP responses.

### Key Components

- **FastAPI**: The web framework used to build the API.
- **SQLAlchemy**: The ORM (Object-Relational Mapping) library used to interact with the SQLite database.
- **SQLite**: The database used to store project and ticket data.
- **CRUD Classes**: Classes that encapsulate the logic for creating, reading, updating, and deleting projects and tickets.

### Example Workflow

1. **Creating a Project**:

   - Client sends a `POST` request to `/projects/` with project data.
   - The `create_project` endpoint function is called.
   - The `ProjectCRUD.create` method is used to insert the new project into the database.
   - The created project is returned to the client.

2. **Retrieving a Project**:
   - Client sends a `GET` request to `/projects/{project_id}`.
   - The `get_project` endpoint function is called.
   - The `ProjectCRUD.get` method is used to fetch the project from the database.
   - The project data is returned to the client.

## Running the Application Locally

To run the application locally, make sure you have Python installed. Then follow these steps at the root directory of the project:

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `uvicorn app.main:app --reload`
3. Navigate to `http://localhost:8000` to view the application

- Note: The application will run in debug mode by default. To disable debug mode, set the `APP_ENV` environment variable to `prod`.

## API Documentation

The API documentation is available at `/docs` when the application is running. It provides details on the available endpoints and their usage.

## License

This project is licensed under the MIT License. See the License file for details.
