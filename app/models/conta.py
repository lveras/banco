from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Conta(Base):
    id = Column(Integer, primary_key=True, index=True)
    movimentacoes = relationship("Movimentacao", back_populates="conta")
