# Hands-On Exercise: Deploying Microservices with Kubernetes

## 📌 **Overview**
In this hands-on exercise, you'll learn how to:
- Build and containerize two simple **Flask-based microservices**.
- Deploy them to **Minikube** using **Kubernetes**.
- Scale one of the services to handle more requests.

---

## 🔧 **Pre-requisites**
Make sure you have the following installed:

### ✅ **Required Tools**
1. **Docker** → [Download here](https://docs.docker.com/get-docker/)
2. **Minikube** → [Install guide](https://minikube.sigs.k8s.io/docs/start/)
3. **kubectl** → [Install guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

To verify installation, run:
```sh
minikube start
kubectl version --client
```
If Minikube starts successfully, you're ready!

---

## 🚀 **Step 1: Write the Microservices**
We'll create **two services**:
1. **backend-service** → A simple API that returns a message.
2. **frontend-service** → Calls the backend and displays the response in an HTML page.

### 📌 **backend-service (Flask API)**
Create a folder `backend-service` and add `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from the Backend!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Create a `requirements.txt` file:
```txt
flask
```

---

### 📌 **frontend-service (Flask + HTML Page)**
Create a folder `frontend-service` and add `app.py`:

```python
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get('http://backend-service:5000')
    return f"The backend said: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Create a `requirements.txt` file:
```txt
flask
requests
```

---

## 🐳 **Step 2: Containerize the Microservices with Docker**

Inside **each service folder**, create a `Dockerfile`:

```Dockerfile
# Use a lightweight Python image
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### 🔹 **Important: Use Minikube's Docker Environment**
Minikube runs its **own Docker daemon**, separate from the Docker installed on your machine. To make sure Minikube can access the images you build, you must run this command **before building**:

```sh
eval $(minikube docker-env)
```
This makes all `docker build` commands target **Minikube's internal Docker** instead of your regular system Docker.

### 🔹 **Build the Images**
Run these commands inside the service folders (after setting the Docker environment):

```sh
docker build -t backend-service ./backend-service
docker build -t frontend-service ./frontend-service
```

You can verify the images exist in Minikube's Docker with:
```sh
docker images
```

---

## 💡 **Optional: Running both services locally with Docker Compose**
If you want to test locally (outside Kubernetes), use Docker Compose to run both services and let them communicate.
Create a `docker-compose.yaml` file:

```yaml
version: '3'
services:
  backend-service:
    build: ./backend-service
    ports:
      - "5000:5000"

  frontend-service:
    build: ./frontend-service
    ports:
      - "8080:5000"
    depends_on:
      - backend-service
```

Run both services with:
```sh
docker-compose up --build
```
Access the frontend at [http://localhost:8080](http://localhost:8080).

---

## ⎈ **Step 3: Deploy to Kubernetes (Minikube)**

### **📌 3.1 Create Kubernetes Deployment & Service for backend-service**
Create `backend-deployment.yaml` in a `k8s/` folder:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: backend-service
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 5000
    targetPort: 5000
  type: ClusterIP
```

Apply it:
```sh
kubectl apply -f k8s/backend-deployment.yaml
```

### **📌 3.2 Create Kubernetes Deployment & Service for frontend-service**
Create `frontend-deployment.yaml` in the same `k8s/` folder:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: frontend-service
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
  - protocol: TCP
    port: 5000
    targetPort: 5000
  type: NodePort
```

Apply it:
```sh
kubectl apply -f k8s/frontend-deployment.yaml
```

Expose it to the browser:
```sh
minikube service frontend-service
```

---

## 📈 **Step 4: Scale the Backend Service**
Now let’s **scale the backend** to handle more requests:
```sh
kubectl scale deployment backend-deployment --replicas=3
```
Check running pods:
```sh
kubectl get pods
```
Test if load balancing works:
```sh
kubectl port-forward service/backend-service 5001:5000
curl http://localhost:5001
```

---

## 🎯 **Why We Do This**
- It simulates a **real-world microservice deployment**.
- You see how Kubernetes handles:
    - **Deployments** (app updates, rollbacks).
    - **Service Discovery** (backend-service hostname works automatically).
    - **Scaling** (horizontal scaling with replicas).
- You understand why **imagePullPolicy** matters when using local images with Minikube.

---

## 🏆 **Bonus Challenge**
- Try increasing frontend replicas!
- Add a health check endpoint (`/health`) to your backend.

---

🚀 **You’ve just built and deployed your first Kubernetes microservices!**

