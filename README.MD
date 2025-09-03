`Docs will be polished soon :)`
# 📦 PasteBin V1.7
**PasteBin** is a *high-performance*, *event-driven* pastebin service built with a clean **microservice architecture**.
Each service is *fully isolated* and communicates through an asynchronous Kafka-based message system.
The project provides creation, publication, and lifetime-controlled access to text-based pastes, along with user registration and authentication.

Thanks to its modular design, PasteBin is easily *scalable*, *extensible*, and *production-ready*.

## 🏗️ Architecture 
### 🧱 Services
- **API Gateway** — responsible for distributing requests between services
- **Auth Service** — responsible for user registration and login
    - Stores basic information about users
- **Paste Service** — core service, responsible for the main work with pastes
    - Basic CRUD
    - Publication, control of the life time of pastes
    - Controls access to pastes


## 🛠️ Tech stack
- **Architecture pattern**: Microservices ✨
- **Message broker**: Kafka 💬
- **Http tools**: Httpx 🔧
- **Database**: PostgreSQL 🐘 
- **Language**: Python 🐍
- **Framework**: FastaAPI ⚡️
- **Containerization**: Docker 🐋 
- **ORM**: SQLAlchemy ⚗️ 
- **Auth**: JWT 🔒

---

## 🔧 Features
- **Event-Driven** — architecture powered by **Kafka**
    - **Fully asynchronous** Kafka consumer & producer implemented with **aiokafka**
- **Completely isolated services** — each service can be independently deployed to the repository and work correctly
    - Each service has its own **Dockerfile** with the service context that is **not related to the outside**
    - Each service was written as if it **would work in a separate repository**
- **One-command deploy** — Docker compose set up and ready for deployment

## ⚙️ How to setup and run
1. Clone repository:
```bash
git clone https://github.com/pixisprod/pastebin.git
cd pastebin
```
2. Prepare the `.env` file in each service.
```bash
cp .env.example .env
```
### 🐋 Docker
3. From the project root run:
```
docker-compose up --build
```
The project will be available at `http://your.ip.address:8080/`