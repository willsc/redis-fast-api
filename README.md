# redis-fast-api
https://rednafi.github.io/digressions/python/database/2020/05/25/python-redis-cache.html


Sidecar pattern :

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pod-with-sidecar
spec:
 replicas: 3
 selector:
  matchLabels:
     role: sidecar
 template:
    metadata:
      labels:
        role: sidecar
    spec:
      volumes:
        - name: shared-logs
          emptyDir: {}
    # In the sidecar pattern, there is a main application
    # container and a sidecar container.
      containers:

      # Main application container
      - name: app-container
        # Simple application: write the current date
        # to the log file every five seconds
        image: alpine # alpine is a simple Linux OS image
        command: ["/bin/sh"]
        args: ["-c", "while true; do date >> /var/log/app.txt; sleep 5;done"]

        # Mount the pod's shared log file into the app
        # container. The app writes logs here.
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log

      # Sidecar container
      - name: sidecar-container
        # Simple sidecar: display log files using nginx.
        # In reality, this sidecar would be a custom image
        # that uploads logs to a third-party or storage service.
        image: nginx:1.7.9
        ports:
          - containerPort: 80

        # Mount the pod's shared log file into the sidecar
        # container. In this case, nginx will serve the files
        # in this directory.
        volumeMounts:
        - name: shared-logs
          mountPath: /usr/share/nginx/html # nginx-specific mount path

```
