# ── Etapa 1: construcción ──────────────────────────
FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go mod tidy
RUN CGO_ENABLED=0 GOOS=linux go build -o server ./cmd/server

# ── Etapa 2: producción ────────────────────────────
FROM alpine:3.19 AS production
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/server .
USER appuser
EXPOSE 8002
CMD ["./server"]