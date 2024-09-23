# Django Weather Data Fetcher

## About the Web App

The **Django Weather Data Fetcher** is a web application designed to collect, store, and manage weather data from a public API. Built with Django and Docker, this application streamlines the process of fetching and analyzing weather information.

### Key Features

- **Data Collection**: Automatically retrieves weather data from a specified public API.
- **Storage and Management**: Stores weather data in a structured database using Django's ORM, allowing for easy querying and management.
- **Dynamic Data Handling**: Utilizes a flexible JSON field to accommodate varying weather data metrics.
- **User-Friendly Interface**: Provides a web interface for users to view and interact with the collected weather data.
- **Containerized Deployment**: Simplifies setup and deployment using Docker, ensuring a consistent development and production environment.

### Use Cases

This web app is ideal for researchers, developers, and organizations interested in monitoring weather patterns, conducting analyses, or integrating weather data into their applications.

## Prerequisites

- Docker installed on your machine.
- Basic knowledge of Django and Docker.



## Configuration

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository


Step 2: Create a .env File
Create a .env file in the root directory of your project to manage sensitive data. You can use the following template:
```
DJANGO_SECRET_KEY='your_secret_key_here'
DEBUG=False
SUPERUSER_NAME=admin
SUPERUSER_EMAIL=admin@example.com
SUPERUSER_PASSWORD=securepassword

```
Step 3: Build and Run the Docker Container
Build and run the Docker container with the following command:
```
docker-compose up --build

```
This command will:

Build the Docker image as defined in your Dockerfile.
Start the Django application and run any necessary migrations.


Step 4: Access the Application
Once the container is running, you can access the application at:

```
http://localhost:8000
```

Running the Weather Data Fetch Command
To fetch the weather data, you can run the following command inside the container:
```
docker-compose exec web python manage.py test

```


License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Any contributions are welcome!

