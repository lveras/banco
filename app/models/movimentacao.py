import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Movimentacao(Base):
    __tablename__ = 'movimentacoes'
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)
    valor = Column(Float, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    conta_id = Column(Integer, ForeignKey("contas.id", ondelete='CASCADE'))
    conta = relationship("Conta", back_populates="movimentacoes")
