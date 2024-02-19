from app.utils.unitofwork import IUnitOfWork


class BaseService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
