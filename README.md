# 📊 1C-Bitrix Observability Pack

[![CI](https://github.com/ranas-mukminov/onec-bitrix-observability-pack/actions/workflows/ci.yml/badge.svg)](https://github.com/ranas-mukminov/onec-bitrix-observability-pack/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

Production-ready observability suite for monitoring Russian enterprise stacks built on **1C:Enterprise**, **1C-Bitrix**, and their databases (PostgreSQL, MySQL, MS SQL Server). This toolkit provides Prometheus exporters, Grafana dashboards, alerting rules, and an AI-powered diagnostics assistant for mission-critical business systems.

## Key Features

- **Purpose-Built Exporters** — Prometheus exporters for 1C cluster metrics (sessions, locks, jobs) and Bitrix performance data (PHP-FPM, cache, components)
- **Ready-to-Use Dashboards** — Three-tier Grafana dashboards: executive overview, DBA/admin panels, and deep-dive troubleshooting
- **Production Alerting** — Prometheus rules based on Four Golden Signals (Latency, Traffic, Errors, Saturation)
- **Database Coverage** — Integration with PostgreSQL, MySQL, and MS SQL Server exporters
- **AI Diagnostics** — Machine learning module for anomaly detection and plain-language recommendations
- **Container-Ready** — Docker Compose for testing, Kubernetes manifests for production
- **Privacy-First** — AI assistant runs locally, no external API calls by default
- **Open Source** — Apache 2.0 license, Python codebase with full type hints

## Architecture

```
1C Cluster ────▶ onec_exporter ───┐
                                   │
Bitrix Site ────▶ bitrix_exporter ─┼──▶ Prometheus ──▶ Grafana
                                   │         │
Databases ──────▶ DB exporters ────┘         └──▶ Alertmanager
                                                      │
                                             AI Assistant
```

**Components:**
- **Exporters**: Scrape metrics from 1C (RAS API), Bitrix (PHP-FPM/Nginx), and databases
- **Prometheus**: Time-series database, scrapes exporters every 15s
- **Grafana**: Visualization with pre-built dashboards
- **Alertmanager**: Routes alerts via email/Slack/PagerDuty
- **AI Assistant**: Analyzes patterns, detects anomalies, generates recommendations

## Requirements

**OS**: Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+  
**Hardware**: 2+ CPU cores, 4 GB RAM (8 GB with AI module), 20 GB disk  
**Software**: Docker 20.10+ & Compose 2.0+ OR Python 3.10+  
**Network**: Access to 1C RAS port (1545), database ports, outbound to Docker Hub/PyPI  
**Permissions**: sudo for Docker, 1C ClusterAdmin role, read-only DB user

## Quick Start

```bash
# Clone repository
git clone https://github.com/ranas-mukminov/onec-bitrix-observability-pack.git
cd onec-bitrix-observability-pack

# Configure connection parameters
cp docker-compose.example.yml docker-compose.yml
nano docker-compose.yml  # Edit ONEC_CLUSTER_HOST, credentials, DB connection string

# Start monitoring stack
docker-compose up -d

# Access interfaces
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
# 1C Metrics: http://localhost:8000/metrics
```

Import dashboards: Grafana → Dashboards → Import → Select files from `dashboards/grafana/`

## Installation

### Docker Compose (Recommended)

```bash
# Install Docker
sudo apt-get install -y docker.io docker-compose  # Ubuntu/Debian
sudo dnf install -y docker docker-compose && sudo systemctl enable --now docker  # RHEL/Rocky

# Deploy
docker-compose up -d

# Verify
docker-compose ps
curl http://localhost:8000/metrics | head
```

### Kubernetes

```bash
# Create namespace
kubectl create namespace monitoring

# Configure secrets
kubectl create secret generic onec-credentials \
  --from-literal=username=admin \
  --from-literal=password=<YOUR_PASSWORD> \
  -n monitoring

# Deploy exporters
kubectl apply -f examples/k8s/deployment_onec_exporter.yaml
kubectl apply -f examples/k8s/deployment_bitrix_exporter.yaml

# Install Prometheus stack (Helm)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

Update Prometheus ConfigMap with scrape targets from `examples/prometheus/prometheus.yml`.

### Native Installation (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt-get install -y python3.10 python3-pip

# Install 1C exporter
cd exporters/onec
pip3 install .

# Create systemd service
sudo tee /etc/systemd/system/onec-exporter.service > /dev/null <<EOF
[Unit]
Description=1C Prometheus Exporter
After=network.target

[Service]
Type=simple
User=prometheus
Environment="ONEC_CLUSTER_HOST=<YOUR_1C_SERVER>"
Environment="ONEC_ADMIN_USER=<USERNAME>"
Environment="ONEC_ADMIN_PASSWORD=<PASSWORD>"
ExecStart=/usr/local/bin/onec-exporter
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now onec-exporter
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ONEC_CLUSTER_HOST` | 1C cluster server IP | Required |
| `ONEC_CLUSTER_PORT` | RAS port | `1545` |
| `ONEC_ADMIN_USER` | Cluster admin username | Required |
| `ONEC_ADMIN_PASSWORD` | Cluster admin password | Required |
| `PROMETHEUS_LISTEN_PORT` | Exporter HTTP port | `8000` |
| `LOG_LEVEL` | DEBUG/INFO/WARNING | `INFO` |

### Prometheus Scrape Config

```yaml
scrape_configs:
  - job_name: 'onec_exporter'
    static_configs:
      - targets: ['onec_exporter:8000']
        labels:
          cluster: 'production'

  - job_name: 'bitrix_exporter'
    static_configs:
      - targets: ['bitrix_exporter:8080']
```

## Usage

**Start/stop services:**
```bash
docker-compose up -d          # Start all
docker-compose restart onec_exporter  # Restart one
docker-compose logs -f grafana        # View logs
docker-compose down           # Stop all
```

**Access monitoring:**
- Grafana: `http://<SERVER_IP>:3000`
- Prometheus: `http://<SERVER_IP>:9090`

**Example PromQL queries:**
```promql
# 1C active sessions
onec_cluster_sessions_active{cluster="production"}

# Bitrix PHP-FPM request rate
rate(bitrix_phpfpm_requests_total[5m])
```

**AI Assistant:**
```bash
docker-compose exec ai_assistant python -m ai_assistant.cli \
  --prometheus-url http://prometheus:9090 \
  --query "onec_cluster_sessions_active > 100" \
  --time-range 1h
```

## Update/Upgrade

```bash
# Backup configuration
cp docker-compose.yml docker-compose.yml.backup

# Pull updates
git pull origin main

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verify
curl http://localhost:8000/metrics
```

## Troubleshooting

**Issue**: 1C exporter shows "Connection Refused"  
**Solution**: Check `ONEC_CLUSTER_HOST`, verify RAS is running (`telnet <HOST> 1545`), check firewall.

**Issue**: No data in Grafana  
**Solution**: Verify Prometheus targets (`http://localhost:9090/targets`), check exporter metrics (`curl http://localhost:8000/metrics`).

**Issue**: Port 8000 already in use  
**Solution**: Change port in `docker-compose.yml`: `ports: - "8001:8000"`

**View logs:**
```bash
docker-compose logs --tail=100 -f onec_exporter
sudo journalctl -u onec-exporter -f  # systemd
```

## Security

- **Change default passwords**: `docker-compose exec grafana grafana-cli admin reset-admin-password <NEW_PASSWORD>`
- **Restrict access**: Use firewall rules, do NOT expose ports 8000/8080/9090 to Internet
- **Enable HTTPS**: Use Nginx/Traefik reverse proxy with Let's Encrypt
- **Use secrets**: Store credentials in Docker/Kubernetes secrets, not plain text
- **Read-only DB users**: Exporters need only SELECT privileges
- **Regular updates**: `docker-compose pull && docker-compose up -d`

## Project Structure

```
exporters/          # Prometheus exporters (onec, bitrix)
dashboards/grafana/ # Grafana JSON dashboards (overview, admin, deepdive)
alerts/prometheus/  # Alert rules YAML
ai/                 # AI diagnostics module
examples/           # Sample configs (prometheus.yml, k8s manifests)
scripts/            # CI/test scripts
tests/              # Unit & integration tests
docker-compose.example.yml  # Full stack template
```

## Contributing

1. Fork and clone: `git clone https://github.com/<YOUR_USER>/onec-bitrix-observability-pack.git`
2. Create branch: `git checkout -b feature/my-feature`
3. Run tests: `./scripts/dev_run_all_tests.sh`
4. Commit: `git commit -m "Add feature"`
5. Push and open PR

**Code standards**: PEP 8, type hints, `black` formatting, 80%+ test coverage. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache License 2.0. See [LICENSE](LICENSE) and [LEGAL.md](LEGAL.md) for details.

**Key points**: Free for commercial use, modification allowed, no warranty provided.

## Author and Commercial Support

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)  
**Website**: [run-as-daemon.ru](https://run-as-daemon.ru)

### Professional Services

Commercial support available for production deployments:
- Turnkey monitoring setup for 1C/Bitrix infrastructure
- Custom dashboards and alerting configuration
- Performance audits and optimization consultingContact via [run-as-daemon.ru](https://run-as-daemon.ru) or GitHub issues.

## Disclaimer

NOT an official product of 1C Company or 1C-Bitrix. Provided "as is" without warranty. User responsible for configuration and compliance with data protection laws (152-FZ, GDPR). See [LEGAL.md](LEGAL.md).
