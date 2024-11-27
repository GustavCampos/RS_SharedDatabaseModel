import strawberry
from enum import Enum
from typing import Optional, Union
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper
from database.table_model import \
    Client as ClientModel, \
    BankAccount as BankAccountModel, \
    Transaction as TransactionModel
    

# This is needed because GraphQL does not support 64 bit integers
BigInt = strawberry.scalar(
    Union[int, str],  # type: ignore
    serialize=lambda v: int(v),
    parse_value=lambda v: str(v),
    description="BigInt field",
)

strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()

@strawberry_sqlalchemy_mapper.type(TransactionModel)
class Transaction():
    @strawberry.field
    def payer_obj(self) -> Optional["BankAccount"]:
        # Return None if there's no payer
        return self.payer_obj if self.payer_obj else None

    @strawberry.field
    def receiver_obj(self) -> Optional["BankAccount"] | None:
        # Return None if there's no receiver
        return self.receiver_obj if self.receiver_obj else None

@strawberry.enum
class TransactionType(Enum):
    WITHDRAWAL = "withdrawal"
    DEPOSIT    = "deposit"
    TRANSFER   = "transfer"

@strawberry_sqlalchemy_mapper.type(BankAccountModel)
class BankAccount():
    @strawberry.field
    def owner_obj(self) -> "Client":
        return self.owner_obj
    
    @strawberry.field
    def payer_transactions(self) -> list[Transaction]:
        return self.payer_transactions

    @strawberry.field
    def receiver_transactions(self) -> list[Transaction]:
        return self.receiver_transactions
    
    @strawberry.field
    def transactions(self) -> list[Transaction]:
        combined_transactions = self.payer_transactions + self.receiver_transactions
        return sorted(combined_transactions, key=lambda t: t.timestamp)

@strawberry_sqlalchemy_mapper.type(ClientModel)
class Client:
    @strawberry.field
    def bank_accounts(self) -> list[BankAccount]:
        return self.bank_accounts