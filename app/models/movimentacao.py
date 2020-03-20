from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class Movimentacao(Base):
    __tablename__ = 'movimentacoes'
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)
    valor = Column(Float, index=True)
    conta_id = Column(Integer, ForeignKey("contas.id"))
    conta = relationship("Conta", back_populates="movimentacoes")
