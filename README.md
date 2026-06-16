# DevSecOps Platform

Plataforma de microservicios con seguridad integrada, CI/CD y observabilidad.

## Servicios

| Servicio             | Puerto | Tecnología |
|----------------------|--------|------------|
| api-gateway          | 3000   | Node.js    |
| user-service         | 8001   | Python     |
| order-service        | 8002   | Go         |
| notification-service | 8003   | Python     |

## Requisitos

- Docker
- Docker Compose
- Git
- Grafana
- Prometheus 
- Github Actions 

## Inicio rápido

```bash
docker compose up -d
```