package service

import (
    "order-service/internal/database"
    "order-service/internal/model"
    "github.com/google/uuid"
)

func CreateOrder(req model.CreateOrderRequest) (model.Order, error) {
    order := model.Order{
        ID:       uuid.New(),
        UserID:   req.UserID,
        Product:  req.Product,
        Quantity: req.Quantity,
        Status:   model.StatusPending,
    }
    result := database.DB.Create(&order)
    return order, result.Error
}

func GetOrder(id uuid.UUID) (model.Order, error) {
    var order model.Order
    result := database.DB.First(&order, "id = ?", id)
    return order, result.Error
}

func ListOrders(userID string) ([]model.Order, error) {
    var orders []model.Order
    result := database.DB.Where("user_id = ?", userID).Find(&orders)
    return orders, result.Error
}