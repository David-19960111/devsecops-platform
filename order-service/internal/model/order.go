package model

import "github.com/google/uuid"

type OrderStatus string

const (
    StatusPending   OrderStatus = "pending"
    StatusConfirmed OrderStatus = "confirmed"
    StatusCancelled OrderStatus = "cancelled"
)

type Order struct {
    ID       uuid.UUID   `json:"id"`
    UserID   string      `json:"user_id"`
    Product  string      `json:"product"`
    Quantity int         `json:"quantity"`
    Status   OrderStatus `json:"status"`
}

type CreateOrderRequest struct {
    UserID   string `json:"user_id" binding:"required"`
    Product  string `json:"product" binding:"required"`
    Quantity int    `json:"quantity" binding:"required,min=1"`
}