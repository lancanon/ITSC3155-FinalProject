from . import orders, order_details, menu_items, customers, customer_feedback, rating_reviews, payment_info, promotions, resource_management

from ..dependencies.database import engine



def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    customer_feedback.Base.metadata.create_all(engine)
    rating_reviews.Base.metadata.create_all(engine)
    payment_info.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    resource_management.Base.metadata.create_all(engine)


