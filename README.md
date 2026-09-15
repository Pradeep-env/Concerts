# Concerts

---

## Getting Started & Running the Project

Follow these steps to set up and run the application locally using Docker.

---

### 1. Install Docker & Docker Compose

Ensure Docker and Docker Compose (v2+) are installed on your system.

#### Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker $USER # Optional: avoids needing sudo for docker commands
```
(If you added your user to the docker group, log out and log back in, or run newgrp docker.)

#### Arch Linux
```bash
sudo pacman -Syu --noconfirm docker docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER   # Optional: avoids needing sudo for docker commands
```
(If you added your user to the docker group, log out and log back in, or run newgrp docker.)

#### Windows & macOS
- Download and install Docker Desktop. Ensure Docker Desktop is running before proceeding.
- Refer: https://docs.docker.com/get-started/get-docker/

---

### 2. Clone the Repository

### Shell (for ssh login)
```bash
git clone git@github.com:Pradeep-env/Concerts.git
cd Concerts/
```

#### URL Clone
```bash
git clone https://github.com/Pradeep-env/Concerts.git
cd Concerts/
```

---

### 3. Configure Environment Variables

Go to backend/ folder, refer env.example and create .env file with your custom inputs.
Save .env in backend/ folder and copy the file to deploy/ folder.

```bash
cd backend/
cp env.example .env
nano .env     # Update database credentials and custom settings
cp .env ../deploy/
```

---

### 4. Run the Application

- Go to deploy/ folder
- Give execute permission to run.sh
- execute run.sh as sudo or as docker user

```bash
cd ../deploy/
chmod +x run.sh  # give execution permission
sudo ./run.sh
# select option 1 (Development)
# Type y/Y for "Are there database/schema updates?"
```
Docker compose will setup PostgreSQL, nginx and deploy 3 containers of the application.
This is for scaling, load balancing and reverse proxy.

#### Docker commands
Commands to check images, containers and logs.

```bash
# To list containers of this project
sudo docker compose -f docker-compose.dev.yml ps -a

# To list images of this project
sudo docker compose -f docker-compose.dev.yml images

# To check logs
sudo docker compose -f docker-compose.dev.yml logs

# To pause/halt containers:
sudo docker compose -f docker-compose.dev.yml stop

# To resume containers right where they left off:
sudo docker compose -f docker-compose.dev.yml start

```

---

### 5. Django Super user setup
To access /admin endpoint in api which helps to see the database schema and all entries, setup super user.

```bash
sudo docker compose -f docker-compose.dev.yml exec -it app python manage.py createsuperuser
```
After creating superuser go to http://localhost/admin/ and login.

---

### 6. Project APIs
To use and refer API endpoints of the project, go to backend/ folder and check for "API_reference" file in each Django app for APIs of particular apps.

example:
```bash
cd ../backend/accounts/
nano API_reference
```
