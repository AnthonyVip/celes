from pydantic import BaseModel
from typing import Union
from datetime import date


class date_model(BaseModel):
    start_date: Union[date, str]
    end_date: Union[date, str]


class SalesPeriodByEmployeeRequest(date_model):
    key_employee: str


class SalesPeriodResponse(BaseModel):
    cantidad: int
    total: float


class SalesPeriodbyProductRequest(date_model):
    key_product: str


class SalesPeriodbyStoreRequest(date_model):
    key_store: str


class AvgSalesResponse(BaseModel):
    average_sales: float
    total_sales: int


class AvgEmployeeRequest(BaseModel):
    key_employee: str


class AvgProductRequest(BaseModel):
    key_product: str


class AvgStoreRequest(BaseModel):
    key_store: str
