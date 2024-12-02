from . import orders, order_details, recipes, menu_items, resource_management


def load_routes(app):
    app.include_router(menu_items.router)
    app.include_router(orders.router)   
    app.include_router(order_details.router) 
    app.include_router(recipes.router)
    app.include_router(resource_management.router)