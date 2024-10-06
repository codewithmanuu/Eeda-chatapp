# Eeda-chatapp

## Description

Eeda is a real-time WebSocket-based chat application built with Django. It allows multiple users to communicate seamlessly, send friend requests, and manage a list of friends. The application ensures real-time message delivery and updates, with features to enhance user interaction and connection.


## Technologies Used

- **Backend**: Django, Django Channels, WebSockets, Redis
- **Frontend**: HTML, CSS, JavaScript (jQuery), kanban bunndle
- **Backend**: Django, Django Channels, WebSockets, Redis
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose

## Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/codewithmanuu/Eeda-chatapp.git

 **Make sure to provide a .env file for local development., craete one by copying from sampleenv.txt file.**

2. **Build and start the services using Docker Compose:**

   ```bash
   sudo docker-compose up --build

   ```windows
   docker-compose up --build

3. **Make migrations and migrate -- optional**

   ```bash
   - sudo docker-compose exec django python manage.py makemigratios SocialMediaApp
   - sudo docker-compose exec django python manage.py migrate

   ```windows
   - docker-compose exec django python manage.py makemigratios SocialMediaApp
   - docker-compose exec django python manage.py migrate

3. **Create a superuser for accessing the Django admin panel:**

   ```bash
   sudo docker-compose exec django python manage.py createsuperuser

   ```windows
   docker-compose exec django python manage.py createsuperuser


## Usage

- Access the application at http://localhost:8000
- register as a new user.
- Login using the email and password.
- Send Friend Requests and Connect with friends and start chatting.
- Access the Django admin panel at http://localhost:8000/admin/


## Development

1. **Use the following command to stop and remove containers:**

   ```bash
   sudo docker-compose down

   ```windows
   docker-compose down

2. **Use the following command to rebuild images and start services:**

   ```bash
   sudo docker-compose up --build

   ```windows
   docker-compose up --build

## Contact

- For questions or comments, please reach out <mailto:manukrishna.s2001@gmail.com>
