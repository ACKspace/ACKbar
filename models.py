from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import func
from database import Base
from sqlalchemy.orm import relationship
import enum

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    balance = Column(Integer, nullable=False)
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, balance={self.balance!r}"

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)
    barcodes = relationship("Barcode", back_populates="product", cascade="all, delete")
    def __repr__(self):
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price!r}, amount={self.amount!r}"

class Barcode(Base):
    __tablename__ = "barcode"
    id = Column(Integer, primary_key=True)
    barcode = Column(String(30), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="barcodes")
    def __repr__(self):
        return f"Barcode(id={self.id!r}, barcode={self.barcode!r}, product_id={self.product_id!r}"

class BankStorting(Base):
    __tablename__ = "bankstorting"
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    bedrag = Column(Integer, nullable=False)
    code = Column(String(30), nullable=False)

class KasMutatieSoort(enum.Enum):
    start	= 0
    storting	= 1
    afroming	= 2
    correctie	= 3

class KasMutatie(Base):
    __tablename__ = "kasmutatie"
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    mutatiesoort = Column(Enum(KasMutatieSoort))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    bedrag = Column(Integer, nullable=False)
    def __repr__(self):
        return f"Kasmutatie(id={self.id!r}, time_created={self.time_created!r}, mutatiesoort={self.mutatiesoort!r}, user_id={self.user_id!r}, bedrag={self.bedrag!r})"

class VoorraadMutatieSoort(enum.Enum):
    start	= 0
    koop	= 1
    donatie	= 2
    correctie	= 3

class VoorraadMutatie(Base):
    __tablename__ = "voorraadmutatie"
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    mutatiesoort = Column(Enum(VoorraadMutatieSoort))
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    hoeveelheid = Column(Integer, nullable=False)
    bedrag = Column(Integer, nullable=False)

class Font(Base):
    __tablename__ = "font"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    score = Column(Integer, nullable=False)
    def __repr__(self):
        return f"Font(id={self.id!r}, name={self.name!r}, score={self.score!r}"
