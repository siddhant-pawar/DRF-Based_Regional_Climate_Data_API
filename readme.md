# Django Weather Data Fetcher

This project fetches weather data from a public API and stores it in a Django database. It is configured to run inside a Docker container.

## Prerequisites

- Docker installed on your machine.
- Basic knowledge of Django and Docker.

## Project Structure

jsonapis/ 
├── datasender/ 
│ ├── management/ 
│ │ └── commands/ 
│ │ └── fetch_weather_data.py 
│ ├── migrations/ 
│ ├── models.py 
│ ├── views.py 
│ └── ... ├── temp/ 
│ ├── AirFrost.txt 
│ ├── Raindays1mm.txt 
│ └── ... 
├── manage.py 
├── requirements.txt 
├── Dockerfile 
└── entrypoint.sh


## Configuration

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
