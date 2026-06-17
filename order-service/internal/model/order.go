package model

import (
    "time"
    "github.com/google/uuid"
)

type OrderStatus string

const (
    StatusPending   OrderStatus = "pending"
    StatusConfirmed OrderStatus = "confirmed"
    StatusCancelled OrderStatus = "cancelled"
)

type Order struct {
    ID        uuid.UUID   `gorm:"type:uuid;primary_key" json:"id"`
    UserID    string      `gorm:"not null" json:"user_id"`
    Product   string      `gorm:"not null" json:"product"`
    Quantity  int         `gorm:"not null" json:"quantity"`
    Status    OrderStatus `gorm:"type:varchar(20);default:'pending'" json:"status"`
    CreatedAt time.Time   `json:"created_at"`
    UpdatedAt time.Time   `json:"updated_at"`
}

type CreateOrderRequest struct {
    UserID   string `json:"user_id" binding:"required"`
    Product  string `json:"product" binding:"required"`
    Quantity int    `json:"quantity" binding:"required,min=1"`
}