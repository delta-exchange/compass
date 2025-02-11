from src.util import DateTimeUtil
from src.database.engine import LedgerEngine
from src.database.model import ProductModel

class ProductService:
    @staticmethod
    def get_between(since, to, batch_size = 10000):
        session = LedgerEngine.get_session()
        products = session.query(ProductModel).filter(ProductModel.created_at > since, ProductModel.created_at <= to).order_by(ProductModel.created_at).limit(batch_size).all()
        return products
    
    @staticmethod
    def get_by_product_symbols(product_symbols):
        session = LedgerEngine.get_session()
        products = session.query(ProductModel).filter(ProductModel.symbol.in_(product_symbols)).all()
        return products