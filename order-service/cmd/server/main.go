package main

import (
    "context"
    "log"
    "os"
    "order-service/internal/database"
    "order-service/internal/handler"
    "order-service/internal/model"
    "github.com/gin-gonic/gin"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
    "go.opentelemetry.io/otel/sdk/trace"
)

func initTracer() {
    ctx := context.Background()
    exporter, err := otlptracehttp.New(ctx,
        otlptracehttp.WithEndpoint("jaeger:4318"),
        otlptracehttp.WithInsecure(),
    )
    if err != nil {
        log.Fatalf("Error creando exporter: %v", err)
    }
    provider := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
    )
    otel.SetTracerProvider(provider)
}

func main() {
    initTracer()
    database.Connect()
    database.DB.AutoMigrate(&model.Order{})

    if os.Getenv("ENV") == "production" {
        gin.SetMode(gin.ReleaseMode)
    }

    r := gin.Default()
    r.Use(otelgin.Middleware("order-service"))

    r.GET("/health", func(c *gin.Context) {
        c.JSON(200, gin.H{"status": "ok", "service": "order-service"})
    })

    r.GET("/metrics", gin.WrapH(promhttp.Handler()))

    orders := r.Group("/orders")
    {
        orders.POST("", handler.CreateOrder)
        orders.GET("", handler.ListOrders)
        orders.GET("/:id", handler.GetOrder)
    }

    port := os.Getenv("PORT")
    if port == "" {
        port = "8002"
    }

    log.Printf("Order service corriendo en puerto %s", port)
    r.Run(":" + port)
}