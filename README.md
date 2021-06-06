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

watchdog Handler:

```
#!/usr/local/bin/python3


import watchdog.events
import watchdog.observers
import time


class Handler(watchdog.events.PatternMatchingEventHandler):
        def __init__(self):
                # Set the patterns for PatternMatchingEventHandler
                #watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.csv'], ignore_directories=True, case_sensitive=False)
                watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*'], ignore_directories=True, case_sensitive=False)

        def on_created(self, event):
                print("Watchdog received created event - % s." % event.src_path)
                # Event is created, you can process it now

        def on_modified(self, event):
                print("Watchdog received modified event - % s." % event.src_path)
                # Event is modified, you can process it now


        def on_deleted(self, event):
                print("Deleted - % s." % event.src_path)


if __name__ == "__main__":
        src_path = r"./"
        event_handler = Handler()
        observer = watchdog.observers.Observer()
        observer.schedule(event_handler, path=src_path, recursive=True)
        observer.start()
        try:
                while True:
                        time.sleep(1)
        except KeyboardInterrupt:
                observer.stop()
        observer.join()

```

```
#!/usr/local/bin/python3


import redis
import sys

def scan_srch(pattern):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        count = 0
        foo=[]
        for key in r.scan_iter(match=pattern,count=100):
            count += 1
            print(key)
            foo.append(key)
        print(count)
       # print(list)
        return list

foo=scan_srch('*7*')
print(foo)


```
