from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class Conta(Base):
    __tablename__ = 'contas'
    id = Column(Integer, primary_key=True, index=True)
    saldo = Column(Float, default=0)
    movimentacoes = relationship("Movimentacao", back_populates="conta")
