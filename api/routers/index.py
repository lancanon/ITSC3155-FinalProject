from . import orders, order_details, menu_items, resource_management, customers, customer_feedback, rating_reviews, payment_info, promotions


def load_routes(app):
    app.include_router(menu_items.router)
    app.include_router(orders.router)
    app.include_router(promotions.router)
    app.include_router(payment_info.router)   
    app.include_router(rating_reviews.router)
    app.include_router(order_details.router) 
    app.include_router(resource_management.router)
    app.include_router(customers.router)
    app.include_router(customer_feedback.router)
    
    