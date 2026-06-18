# 🔐 DevSecOps Platform

![CI Pipeline](https://github.com/David-19960111/devsecops-platform/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/kubernetes-ready-blue?logo=kubernetes)

Plataforma de microservicios con seguridad integrada en cada etapa del ciclo de vida — desde el código hasta producción.

---

## 📐 Arquitectura

```
Cliente → API Gateway (Node.js) → User Service (Python)
                               → Order Service (Go)
                               → Notification Service (Python)
```

Todos los servicios internos son accesibles solo a través del API Gateway. Las Network Policies de Kubernetes refuerzan este aislamiento a nivel de red.

---

## 🛠️ Stack Tecnológico

### Servicios
| Servicio | Tecnología | Puerto | Descripción |
|---|---|---|---|
| api-gateway | Node.js + Express | 3000 | Enrutamiento, autenticación JWT, rate limiting |
| user-service | Python + FastAPI | 8001 | Registro y login de usuarios |
| order-service | Go + Gin | 8002 | Gestión de pedidos |
| notification-service | Python + FastAPI | 8003 | Envío de notificaciones |

### Infraestructura
| Herramienta | Uso |
|---|---|
| PostgreSQL | Base de datos para users y orders |
| Docker + Docker Compose | Containerización y orquestación local |
| Kubernetes | Orquestación en producción |
| HashiCorp Vault | Gestión de secrets |

### Observabilidad
| Herramienta | Uso | Puerto |
|---|---|---|
| Prometheus | Métricas | 9090 |
| Grafana | Dashboards | 3001 |
| Loki + Promtail | Logs centralizados | 3100 |
| Jaeger | Distributed tracing | 16686 |

### Seguridad (DevSecOps)
| Herramienta | Etapa | Descripción |
|---|---|---|
| GitLeaks | CI | Escaneo de secrets en commits |
| Semgrep | CI | SAST para Node.js |
| Bandit | CI | SAST para Python |
| Trivy | CI | Escaneo de imágenes Docker |
| Cosign | CI | Firma de imágenes |
| OWASP ZAP | CI | DAST contra la app corriendo |
| Network Policies | K8s | Zero trust entre servicios |

---

## 🚀 Inicio Rápido

### Requisitos
- Docker y Docker Compose
- Git

### Correr localmente

```bash
# Clonar el repositorio
git clone https://github.com/David-19960111/devsecops-platform.git
cd devsecops-platform

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Levantar todos los servicios
docker compose up -d

# Verificar que todo está corriendo
docker compose ps
```

### Verificar los servicios

```bash
curl http://localhost:3000/health  # API Gateway
curl http://localhost:8001/health  # User Service
curl http://localhost:8002/health  # Order Service
curl http://localhost:8003/health  # Notification Service
```

### Flujo de autenticación

```bash
# Registrar un usuario
curl -X POST http://localhost:8001/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@test.com", "password": "12345678", "full_name": "Tu Nombre"}'

# Login - guarda el token
curl -X POST http://localhost:8001/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@test.com", "password": "12345678"}'

# Usar el token en rutas protegidas
curl http://localhost:3000/privado \
  -H "Authorization: Bearer <token>"
```

---

## 📊 Observabilidad

| Dashboard | URL | Credenciales |
|---|---|---|
| Grafana | http://localhost:3001 | admin / admin |
| Prometheus | http://localhost:9090 | - |
| Jaeger | http://localhost:16686 | - |
| Vault | http://localhost:8200 | token: dev-token |

---

## ☸️ Kubernetes

```bash
# Aplicar todos los manifiestos
kubectl apply -f k8s/base/

# Ver pods corriendo
kubectl get pods

# Ver servicios
kubectl get svc

# Ver network policies
kubectl get networkpolicies
```

---

## 🔒 Pipeline CI/CD

El pipeline corre automáticamente en cada push a `main` o `master`:

```
Secret Scan → SAST → Tests → Build & Scan Imágenes → Push & Sign → DAST
```

1. **Secret Scan** — GitLeaks escanea todo el historial de git
2. **SAST** — Semgrep (Node.js) y Bandit (Python) analizan el código
3. **Tests** — Jest para el gateway, go test para el order service
4. **Build & Scan** — Trivy escanea cada imagen buscando CVEs críticos
5. **Push & Sign** — Sube imágenes a GHCR y las firma con Cosign
6. **DAST** — OWASP ZAP escanea la aplicación corriendo

---

## 📁 Estructura del Proyecto

```
devsecops-platform/
├── api-gateway/          # Node.js - Enrutamiento y autenticación
├── user-service/         # Python FastAPI - Gestión de usuarios
├── order-service/        # Go - Lógica de pedidos
├── notification-service/ # Python FastAPI - Notificaciones
├── k8s/
│   └── base/             # Manifiestos de Kubernetes
├── monitoring/
│   ├── prometheus/       # Configuración de Prometheus
│   ├── loki/             # Configuración de Loki
│   └── promtail/         # Configuración de Promtail
├── scripts/              # Scripts de utilidad
├── .github/
│   └── workflows/        # Pipelines de CI/CD
├── .zap/                 # Reglas de OWASP ZAP
└── docker-compose.yml    # Orquestación local
```

---

## 🔮 Próximos pasos

- [ ] GitOps con ArgoCD
- [ ] Terraform para infraestructura en la nube
- [ ] Helm charts para Kubernetes
- [ ] Tests de integración end-to-end
- [ ] Falco para detección de amenazas en runtime

---

## 📝 Licencia

MIT