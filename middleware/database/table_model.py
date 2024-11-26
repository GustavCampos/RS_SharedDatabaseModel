from sqlalchemy import Column, BigInteger, String, ForeignKey, Enum, TIMESTAMP, Sequence
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base


# Declarative ORM base
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(BigInteger, Sequence("client_id_seq"),primary_key=True)
    cpf = Column(String, nullable=False, unique=True)
    complete_name = Column(String, nullable=False)
    
    # Client -< BankAccount
    bank_accounts = relationship("BankAccount", back_populates="owner_obj")
        
class BankAccount(Base):
    __tablename__ = "bank_accounts"
    
    id = Column(BigInteger, Sequence("bkacc_id_seq"),primary_key=True)
    owner = Column(ForeignKey("clients.id"), name="owner",nullable=False)
    balance = Column(BigInteger, nullable=False, default=0)
    password = Column(String, nullable=False)
    
    # Client -< BankAccount
    owner_obj = relationship("Client", back_populates="bank_accounts")
    
    # BankAccount >- Transaction -< BankAccount
    payer_transactions = relationship("Transaction", 
        back_populates="payer_obj",
        foreign_keys="Transaction.payer"
    )
    receiver_transactions = relationship("Transaction", 
        back_populates="receiver_obj", 
        foreign_keys="Transaction.receiver"
    )
    
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(BigInteger, Sequence("transaction_id_seq"), primary_key=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    transaction_type = Column(
        Enum("withdrawal", "deposit", "transfer", name="transaction_types"), 
        name="type", nullable=False
    )
    amount = Column(BigInteger, nullable=False)
    payer = Column(ForeignKey("bank_accounts.id"), nullable=True)
    receiver = Column(ForeignKey("bank_accounts.id"), nullable=True)
    
    # BankAccount >- Transaction -< BankAccount
    payer_obj = relationship("BankAccount", 
        back_populates="payer_transactions", 
        foreign_keys=[payer]
    )
    receiver_obj = relationship("BankAccount", 
        back_populates="receiver_transactions", 
        foreign_keys=[receiver]
    )
    
    @validates('payer')
    def validate_payer(self, key, value):
        if self.transaction_type in ['transfer', 'withdrawal'] and value is None:
            raise ValueError(f"Receiver must exist for {self.transaction_type} transactions.")
        return value

    @validates('receiver')
    def validate_receiver(self, key, value):
        if self.transaction_type in ['transfer', 'deposit'] and value is None:
            raise ValueError(f"Receiver must exist for {self.transaction_type} transactions.")
        return value
