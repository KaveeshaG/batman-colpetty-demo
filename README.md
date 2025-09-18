# When Batman Needs ArgoCD to Save Colpetty 🦇

A comprehensive GitOps demonstration using ArgoCD, Kustomize, and GitHub Actions to showcase automated Kubernetes deployments.

## Overview

This repository contains a complete GitOps setup demonstrating how to deploy and manage applications using ArgoCD and Kustomize. The project uses a Batman-themed Flask application to make learning GitOps concepts engaging and memorable.

## Architecture

```
Developer → GitHub → GitHub Actions (CI) → ArgoCD (CD) → K3s Cluster
```

- **GitHub**: Source code and GitOps repository
- **GitHub Actions**: Automated CI pipeline (build, test, push images)
- **ArgoCD**: GitOps continuous delivery
- **Kustomize**: Configuration management for multiple environments
- **K3s**: Lightweight Kubernetes cluster

## Prerequisites

- Ubuntu/Linux server (tested on Ubuntu 22.04)
- Docker
- Git
- kubectl
- At least 2GB RAM and 2 CPU cores

## Repository Structure

```
batman-colpetty-demo/
├── app/                          # Flask application
│   ├── app.py                   # Batman-themed web app
│   ├── Dockerfile               # Multi-platform container build
│   └── requirements.txt         # Python dependencies
├── k8s-manifests/               # Kubernetes configurations
│   ├── base/                    # Common configurations
│   │   ├── kustomization.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   └── overlays/                # Environment-specific configs
│       ├── staging/
│       │   ├── kustomization.yaml
│       │   └── replica-patch.yaml
│       └── production/
│           ├── kustomization.yaml
│           └── replica-patch.yaml
├── .github/workflows/           # CI/CD automation
│   └── ci-cd.yaml              # GitHub Actions workflow
├── argocd/                      # ArgoCD application configs
│   └── application.yaml         # ArgoCD application definitions
└── README.md                    # This file
```

## Quick Start

### 1. Set Up K3s Cluster

```bash
# Install K3s
curl -sfL https://get.k3s.io | sh -

# Configure kubectl for regular user
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config

# Verify cluster is running
kubectl get nodes
```

### 2. Install ArgoCD

```bash
# Create ArgoCD namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```

### 3. Access ArgoCD UI

```bash
# Port forward ArgoCD server (run in background)
kubectl port-forward svc/argocd-server -n argocd 8080:443 &

# Access ArgoCD at: http://localhost:8080
# Username: admin
# Password: (from step 2 above)
```

### 4. Deploy the Batman Application

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/batman-colpetty-demo.git
cd batman-colpetty-demo

# Update ArgoCD application configuration
# Edit argocd/application.yaml and replace YOUR_USERNAME with your GitHub username

# Deploy ArgoCD applications
kubectl apply -f argocd/application.yaml

# Check application status
kubectl get applications -n argocd
```

### 5. Access the Batman Application

```bash
# Port forward the application
kubectl port-forward svc/colpetty-guardian-service -n colpetty-staging 3000:80

# Access the app at: http://localhost:3000
```

## Configuration Management with Kustomize

### Base Configuration
Common resources shared across all environments:
- Deployment template
- Service configuration
- ConfigMap with default values

### Environment Overlays

**Staging Environment:**
- 1 replica for resource efficiency
- Debug logging enabled
- Development-specific configurations

**Production Environment:**
- 3 replicas for high availability
- Optimized logging
- Production-specific configurations

### Customizing Environments

```bash
# Update staging replica count
cd k8s-manifests/overlays/staging
kustomize edit set replicas colpetty-guardian=2

# Update production image
cd ../production
kustomize edit set image batman-app=ghcr.io/your-username/batman-colpetty-demo:v2.0.0

# Preview changes
kustomize build .
```

## CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Builds** multi-platform Docker images (AMD64/ARM64)
2. **Pushes** images to GitHub Container Registry
3. **Updates** Kustomize image references
4. **Commits** changes back to the repository
5. **Triggers** ArgoCD sync automatically

### Triggering Deployments

```bash
# Make a change to the application
echo "# Updated for demo" >> app/README.md

# Commit and push
git add app/
git commit -m "Update Batman app for demo"
git push origin main

# Watch the magic happen:
# 1. GitHub Actions builds new image
# 2. Updates k8s-manifests/
# 3. ArgoCD detects changes
# 4. Syncs to cluster automatically
```

## Monitoring and Observability

### Check Application Health

```bash
# View ArgoCD applications
kubectl get applications -n argocd

# Check pod status
kubectl get pods -n colpetty-staging
kubectl get pods -n colpetty-production

# View application logs
kubectl logs -l app=colpetty-guardian -n colpetty-staging

# Check recent events
kubectl get events -n colpetty-staging --sort-by='.lastTimestamp'
```

### ArgoCD CLI (Optional)

```bash
# Install ArgoCD CLI
curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x /usr/local/bin/argocd

# Login
argocd login localhost:8080 --username admin --password YOUR_PASSWORD --insecure

# View applications
argocd app list

# Sync application manually
argocd app sync colpetty-guardian-staging
```

## Demo Scenarios

### Scenario 1: Normal Deployment
1. Make code changes
2. Push to GitHub
3. Watch GitHub Actions build
4. Observe ArgoCD sync
5. Verify application update

### Scenario 2: Rollback Demo (Villain Attack!)
```bash
# Simulate bad deployment
cd k8s-manifests/overlays/staging
kustomize edit set image batman-app=nginx:fake-malicious-tag
git add . && git commit -m "Joker attack!" && git push

# Watch failure in ArgoCD UI and kubectl

# Quick rollback
git revert HEAD --no-edit && git push

# Watch automatic recovery
```

### Scenario 3: Scaling Demo
```bash
# Scale production for high traffic
cd k8s-manifests/overlays/production
kustomize edit set replicas colpetty-guardian=5
git add . && git commit -m "Scale for Penguin's traffic spike" && git push

# Watch pods scale up automatically
kubectl get pods -n colpetty-production -w
```

## Troubleshooting

### Common Issues

**ArgoCD Application Not Syncing:**
```bash
# Check application status
kubectl describe application colpetty-guardian-staging -n argocd

# Force refresh
kubectl patch application colpetty-guardian-staging -n argocd --type merge -p='{"spec":{"source":{"targetRevision":"HEAD"}}}'
```

**Image Pull Errors:**
```bash
# Check if images exist in registry
# Go to: https://github.com/YOUR_USERNAME/batman-colpetty-demo/pkgs/container/batman-colpetty-demo

# Verify image references in kustomization
cat k8s-manifests/overlays/staging/kustomization.yaml | grep image
```

**Port Forward Issues:**
```bash
# Kill existing port forwards
pkill -f "kubectl port-forward"

# Use different ports
kubectl port-forward svc/argocd-server -n argocd 8081:443
kubectl port-forward svc/colpetty-guardian-service -n colpetty-staging 3001:80
```

### Debug Commands

```bash
# Check cluster status
kubectl get nodes
kubectl get pods --all-namespaces

# Check ArgoCD status
kubectl get pods -n argocd
kubectl logs -f deployment/argocd-server -n argocd

# Check application resources
kubectl get all -n colpetty-staging
kubectl describe deployment colpetty-guardian -n colpetty-staging
```

## Cleanup

```bash
# Remove applications
kubectl delete -f argocd/application.yaml

# Remove ArgoCD
kubectl delete namespace argocd

# Remove application namespaces
kubectl delete namespace colpetty-staging colpetty-production

# Uninstall K3s (optional)
sudo /usr/local/bin/k3s-uninstall.sh
```

## Architecture Benefits

### GitOps Advantages
- **Declarative**: Everything defined in Git
- **Auditable**: Complete change history
- **Reversible**: Easy rollbacks with Git
- **Secure**: Pull-based deployments
- **Scalable**: Multi-cluster management

### ArgoCD Benefits
- **Automated Sync**: Continuous deployment
- **Health Monitoring**: Application status tracking
- **Web UI**: Visual deployment management
- **RBAC**: Role-based access control
- **Hooks**: Pre/post deployment actions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with your K3s cluster
5. Submit a pull request

## Security Notes

- Never commit secrets to Git
- Use Sealed Secrets or external secret management
- Implement proper RBAC in ArgoCD
- Regularly update base images and dependencies
- Monitor for security vulnerabilities

## Resources

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Kustomize Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
- [GitOps Principles](https://opengitops.dev/)
- [K3s Documentation](https://k3s.io/)

## License

MIT License - Feel free to use this for learning and demonstrations.

## Contact

- **GitHub**: @kaveeshag
- **Website**: https://kaveeshagimhana.com
- **Email**: uakaveeshagimhana@gmail.com

---

**Remember: With great power comes great responsibility... to automate your deployments properly!** 🦇
