# Implement Cloud Security Fundamentals on Google Cloud: Challenge Lab

```sql
gcloud config set compute/zone us-east4-a
```

### create role 
```
nano role-creation.yaml
```

```
title: "custom-role"
description: "Permissions"
stage: "ALPHA"
includedPermissions:
- storage.buckets.get
- storage.objects.get
- storage.objects.list
- storage.objects.update
- storage.objects.create
```

```
gcloud iam roles create "custom-role" --project $DEVSHELL_PROJECT_ID --file role-creation.yaml
```

### create service account
```
gcloud iam service-accounts create orca-private-cluster-419-sa --display-name "Service Account for kubernet"
```
### create a private cluster kubernetes
```sql
gcloud beta container clusters create orca-cluster-204 \
  --enable-private-nodes \
  --enable-ip-alias \
  --enable-private-endpoint \
  --enable-master-authorized-networks\
  --network orca-build-vpc\
  --subnetwork orca-build-subnet \
  --zone=us-east4-a \
  --service-account=orca-private-cluster-419-sa@qwiklabs-gcp-03-e72983809f06.iam.gserviceaccount.com\
  --master-authorized-networks 192.168.10.2/32
```

### in bastionhost compute, get credentials 
```
gcloud container clusters get-credentials orca-cluster-204
```


### task 5: create deployment
```
kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0
```

### expose the port 
```
kubectl expose deployment hello-server --name orca-hello-service --type LoadBalancer --port 80 --target-port 8080
```
