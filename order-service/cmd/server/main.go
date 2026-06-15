package main

import (
    "log"
    "os"
    "order-service/internal/handler"
    "github.com/gin-gonic/gin"
)

func main() {
    if os.Getenv("ENV") == "production" {
        gin.SetMode(gin.ReleaseMode)
    }

    r := gin.Default()

    r.GET("/health", func(c *gin.Context) {
        c.JSON(200, gin.H{"status": "ok", "service": "order-service"})
    })

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