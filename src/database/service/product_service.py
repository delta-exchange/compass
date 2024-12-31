from src.util import DateTimeUtil
from src.database.engine import LedgerEngine
from src.database.model import ProductModel

class ProductService:
    @staticmethod
    def get_batch_by_created_at(batch, limit = 500, created_at = DateTimeUtil.get_24hrs_ago()):
        offset = (batch -1) * limit
        session = LedgerEngine.get_session()
        products = session.query(ProductModel).filter(ProductModel.created_at > created_at).order_by(ProductModel.created_at).limit(limit).offset(offset).all()
        return products
    
    @staticmethod
    def get_by_product_symbols(product_symbols):
        if len(product_symbols) == 0: 
            return {}
        session = LedgerEngine.get_session()
        products = session.query(ProductModel).filter(ProductModel.symbol.in_(product_symbols)).all()
        return dict(map(lambda product: (product.symbol, product), products))