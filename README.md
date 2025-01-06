
# Project Deployment Guide

## Overview
This project is a microservices-based architecture consisting of three main services:
1. **User Service**: Handles user management and authentication.
2. **Blog Service**: Manages blog posts and related operations.
3. **Comment Service**: Handles comments on blog posts.

All services are backed by a PostgreSQL database. Docker Compose is used to orchestrate the services locally, and the application can be deployed to AWS using EC2 and Docker Compose.

---

## Project Structure
plaintext
- /db
  - data/            # Database persistent volume
  - init.sql         # Initialization script for setting up the database
- /user-service      # Source code for the User Service
- /blog-service      # Source code for the Blog Service
- /comment-service   # Source code for the Comment Service
- docker-compose.yml # Docker Compose configuration file
- README.md          # Project documentation


---

## Prerequisites
Before deploying the project, ensure the following tools and accounts are available:

1. **AWS Account**
2. **Docker and Docker Compose**
3. **AWS CLI (Command Line Interface)**
4. **PostgreSQL client** (optional for database testing)
5. **Git**

---

## Deployment Steps
### 1. Launch an EC2 Instance

1. **Create an EC2 instance:**
   - Go to the AWS Management Console and navigate to the **EC2** service.
   - Launch a new instance with the following configurations:
     - **AMI**: Amazon Linux 2 or Ubuntu 20.04/22.04.
     - **Instance Type**: t2.medium or larger.
     - **Security Group**: Allow the following ports: 22 (SSH), 5432 (PostgreSQL), 5001-5003 (Microservices).
   - Attach an Elastic IP to the instance for a static public IP address.

2. **Connect to the instance via SSH:**
   bash
   ssh -i <YOUR_KEY_PAIR>.pem ec2-user@<EC2_PUBLIC_IP>
   

3. **Update the system and install Docker:**
   bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y docker.io docker-compose
   sudo usermod -aG docker $USER
   

4. **Re-login to apply Docker group changes:**
   bash
   exit
   ssh -i <YOUR_KEY_PAIR>.pem ec2-user@<EC2_PUBLIC_IP>
   

---

### 2. Setup and Deploy the Application

1. **Transfer project files to the EC2 instance:**
   bash
   scp -i <YOUR_KEY_PAIR>.pem -r ./<PROJECT_FOLDER> ec2-user@<EC2_PUBLIC_IP>:~/
   

2. **Navigate to the project directory:**
   bash
   cd <PROJECT_FOLDER>
   

3. **Modify `DATABASE_URI` in `docker-compose.yml` for local PostgreSQL:**
   Ensure the `DATABASE_URI` points to the local PostgreSQL container:
   yaml
   DATABASE_URI=postgresql://user:password@db/<DATABASE_NAME>
   

4. **Start the application using Docker Compose:**
   bash
   docker-compose up --build -d
   

---

### 3. Validate Deployment

1. **Verify running containers:**
   bash
   docker ps
   

2. **Access the services in your browser or API tools:**
   - User Service: `http://<EC2_PUBLIC_IP>:5001`
   - Blog Service: `http://<EC2_PUBLIC_IP>:5002`
   - Comment Service: `http://<EC2_PUBLIC_IP>:5003`

3. **Test API Endpoints:**
   Use Postman or `curl` to verify API functionality.
   bash
   curl -X GET http://<EC2_PUBLIC_IP>:5001/api/v1/users
   

---

## Local Development and Testing
### Running Locally with Docker Compose
1. **Build and start the services:**
   bash
   docker-compose up --build
   
2. **Access the services:**
   - User Service: `http://localhost:5001`
   - Blog Service: `http://localhost:5002`
   - Comment Service: `http://localhost:5003`

### Stopping Services
bash
docker-compose down


---

## Environment Variables
The following environment variables must be set for each service:

| Variable         | Description                                    |
|------------------|------------------------------------------------|
| `DATABASE_URI`   | PostgreSQL connection string                  |
| `JWT_SECRET_KEY` | Secret key for JWT authentication             |

---

## Future Enhancements
- Implement centralized logging with AWS CloudWatch.
- Set up monitoring with AWS CloudWatch or Datadog.

---

## License
This project is licensed under the MIT License. See `LICENSE` for more details.
