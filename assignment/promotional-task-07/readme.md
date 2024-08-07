# CONTAINERIZE AND DEPLOY A SIMPLE APP TO KUBERNETES - MY APPROACH
I created this directory structure to create, containerize and deploy a simple app to Kubernetes cluster using Minikube.

Directory Structure
```bash
├── kubernetes
│ ├── app.py
│ ├── deployment.yaml
│ ├── Dockerfile
│ ├── requirements.txt
│ └── service.yaml
└── readme.md
```

## STEP 1 - CREATE APPLICATION

Using the python programming language, I created a simple flask app that returns "Hello, Welcome to Kodecamp DevOps Bootcamp". See the code below

```bash
# Import Flask
from flask import Flask


app = Flask(__name__)

# Route Traffic to Index
@app.route("/")
def index():
    return "Hello, Welcome to KodeCamp DevOps Bootcamp!"

# Run App
if __name__ == "__main__":
    # host 0.0.0.0 ensures that the app is accessible from outside the container
    app.run(host="0.0.0.0", port=8000)
```

To be able to run the flask app successfully, we need to install Flask. I created a `requirements.txt` file with the necessary app dependencies as python requires using the command `pip3 freeze > requirements.txt`.

```bash
blinker==1.8.2
click==8.1.7
Flask==3.0.3
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==2.1.5
Werkzeug==3.0.3

```

## STEP 2 - BUILD APP WITH DOCKER

To build the app with docker, I wrote the Dockerfile to containerize the application.

`Dockerfile`

```bash
# Python Docker Image
FROM python:3

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run app.py when the container launches
CMD ["python3", "app.py"]

```

I now ran the following command to build the app

```bash
# Build Docker Image
docker build -t kc-kube-app .
```

And then ran it locally

```bash
# Run Docker Container
docker run -p 8000:8000 kc-kube-app
```
Response
![doc-kub-app-running](https://github.com/user-attachments/assets/44621298-790d-4623-a2c5-942a652bf8f7)

## STEP 3 - PUSH APP IMAGE TO DOCKER HUB

To push the locally built image to to docker hub, I logged in to docker from the terminal by running

```bash
docker login
```

and entering my docker hub login credentials.

After that I prepared the image by tagging it before pushing it to docker hub

```bash
docker tag kc-kube-app daveamegs/kc-kube-app

```

Now push

```bash
docker push daveamegs/kc-kube-app

```

## STEP 4 - DEPLOY APP TO MINIKUBE CLUSTER

To deploy the app to a cluster on kubernetes using minikube, I created the kubernetes manifest files `deployment.yaml` and `service.yaml`.

`deployment.yaml`
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kc-minikube-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kc-kube-app
  template:
    metadata:
      labels:
        app: kc-kube-app
    spec:
      containers:
      - name: kc-minikube-app-deployment
        image: daveamegs/kc-kube-app
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "512Mi"
            cpu: "1000m"
          requests:
            memory: "256Mi"
            cpu: "500m"

```

`service.yaml`
```bash
apiVersion: v1
kind: Service
metadata:
  name: kc-minikube-app-service
spec:
  selector:
    app: kc-kube-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP

```

To finally deploy the app to minikube, I ran the following commands to start minikube and apply the kubernetes deployment and service files.
```bash
# Start Minikube
minikube start

```

Apply `deployment.yaml` and `service.yaml` files
```bash
# Apply Deployment
kubectl apply -f deployment.yaml

# Apply Service
kubectl apply -f service.yaml

```

## STEP 5 - TEST DEPLOYMENT BY PORT-FORWARDING
To now test if the app is really deployed to minikube cluster, I port-forwarded the service to `8080` to see if it still handle requests or connections correctly.
```bash
# Port-Forward Service
kubectl port-forward service/kc-minikube-app-service 8080:80

```
Response
![doc-kube-port-forwarded](https://github.com/user-attachments/assets/c6e38654-47f3-4e73-9e70-3afc58135b7f)

Connection is being handled correctly
![doc-kube-handle-connection](https://github.com/user-attachments/assets/8a28f7a3-87c0-48f8-b51a-6cb88a920b1f)

Live Website 
![doc-kube-web-working](https://github.com/user-attachments/assets/f88c6acf-fa2d-4abd-a271-9e6c5f0f594c)

## ISSUES I FACED
In my case, everything was straightforward. The only issue was I could not port-forward the kubernetes service. I was getting errors. I later realized it was because I installed `kubectl` after starting `minikube`. Everything worked well after restarting my laptop.

## Docker Image
[docker image](https://hub.docker.com/r/daveamegs/kc-kube-app)
