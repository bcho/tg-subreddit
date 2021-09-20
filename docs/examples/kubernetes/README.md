# Kustomize Deployment Spec

## Usage

### Step 1: copy and update configurations

```
$ cp -r docs/examples/kubernetes my-deployment
# update secrets
$ $EDITOR my-deployment/kustomization.yaml
# update poll settings
$ $EDITOR my-deployment/my-poll-settings.json
```

### Step 2: apply deployment

```
$ kubectl create namespace tg-subreddit
$ kustomize build my-deployment | kubectl apply -f -
```

### Step 3: update poll settings

It's a common task to update poll settings. We can simply adjust the `my-poll-settings.json` and
reapply the build.

```
$ $EDITOR my-deployment/my-poll-settings.json
$ kustomize build my-deployment | kubectl apply -f -
```