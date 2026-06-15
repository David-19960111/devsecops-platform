package service

import (
    "errors"
    "order-service/internal/model"
    "github.com/google/uuid"
)

// Base de datos en memoria por ahora
var orders = map[uuid.UUID]model.Order{}

func CreateOrder(req model.CreateOrderRequest) model.Order {
    order := model.Order{
        ID:       uuid.New(),
        UserID:   req.UserID,
        Product:  req.Product,
        Quantity: req.Quantity,
        Status:   model.StatusPending,
    }
    orders[order.ID] = order
    return order
}

func GetOrder(id uuid.UUID) (model.Order, error) {
    order, exists := orders[id]
    if !exists {
        return model.Order{}, errors.New("order not found")
    }
    return order, nil
}

func ListOrders(userID string) []model.Order {
    result := []model.Order{}
    for _, order := range orders {
        if order.UserID == userID {
            result = append(result, order)
        }
    }
    return result
}