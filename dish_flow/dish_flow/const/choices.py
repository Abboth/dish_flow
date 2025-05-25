ORDER_STATUSES = {
    'NEW': 'new',
    'PREPARING': 'preparing',
    'READY': 'ready',
    'ON_DELIVERY': 'on_delivery',
    'COMPLETED': 'completed',
    'CANCELLED': 'cancelled',
}

STATUS_DISPLAY_NAMES = {
    ORDER_STATUSES['NEW']: "Новый",
    ORDER_STATUSES['PREPARING']: "Готовится",
    ORDER_STATUSES['READY']: "Готов",
    ORDER_STATUSES['ON_DELIVERY']: "В пути",
    ORDER_STATUSES['COMPLETED']: "Завершен",
    ORDER_STATUSES['CANCELLED']: "Отменен",
}
