from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class Conta(Base):
    __tablename__ = 'contas'
    id = Column(Integer, primary_key=True, index=True)

    movimentacoes = relationship("Movimentacao", back_populates="conta")
