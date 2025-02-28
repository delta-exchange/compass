from src.util import DateTimeUtil
from src.database.engine import LedgerEngine
from src.database.model import ProductModel

class ProductService:
    @staticmethod
    def get_between(since, to, batch_size = 10000):
        session = LedgerEngine.get_session()
        products = session.query(ProductModel).filter(ProductModel.updated_at > since, ProductModel.updated_at <= to).order_by(ProductModel.updated_at).limit(batch_size).all()
        return products
    
    @staticmethod
    def get_by_product_symbols(product_symbols):
        session = LedgerEngine.get_session()
        products = session.query(ProductModel).filter(ProductModel.symbol.in_(product_symbols)).all()
        return products
    
    @staticmethod
    def get_by_product_ids(product_ids):
        session = LedgerEngine.get_session()
        products = session.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()
        return products