package handler

import (
    "net/http"
    "order-service/internal/model"
    "order-service/internal/service"
    "github.com/gin-gonic/gin"
    "github.com/google/uuid"
)

func CreateOrder(c *gin.Context) {
    var req model.CreateOrderRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    order, err := service.CreateOrder(req)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al crear el pedido"})
        return
    }
    c.JSON(http.StatusCreated, order)
}

func GetOrder(c *gin.Context) {
    id, err := uuid.Parse(c.Param("id"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
        return
    }
    order, err := service.GetOrder(id)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "Pedido no encontrado"})
        return
    }
    c.JSON(http.StatusOK, order)
}

func ListOrders(c *gin.Context) {
    userID := c.Query("user_id")
    if userID == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "user_id es requerido"})
        return
    }
    orders, err := service.ListOrders(userID)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al listar pedidos"})
        return
    }
    c.JSON(http.StatusOK, orders)
}