import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Movimentacao(Base):
    __tablename__ = 'movimentacoes'
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    valor = Column(Float)
    taxa = Column(Float)
    saldo_movimentacao = Column(Float)
    saldo_conta_atual = Column(Float)
    conta_origem_id = Column(Integer, default=0)
    conta_destino_id = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    conta_id = Column(Integer, ForeignKey("contas.id", ondelete='CASCADE'))
    conta = relationship("Conta", back_populates="movimentacoes")
