from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Index
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    discount_percentage = Column(Float, nullable=False)  
    expiration_date = Column(Date, nullable=False)  
    is_active = Column(Boolean, default=True)  

    # index for frequent queries
    __table_args__ = (
        Index("idx_promotion_code", "code"),
        Index("idx_promotion_active", "is_active"),
    )
