from fastapi import APIRouter, Body, HTTPException, status

from schemas.celes import (
    SalesPeriodByEmployeeRequest,
    SalesPeriodResponse,
    SalesPeriodbyProductRequest,
    SalesPeriodbyStoreRequest,
    AvgSalesResponse,
    AvgEmployeeRequest,
    AvgProductRequest,
    AvgStoreRequest
)
from modules.datamart import DataManager

router = APIRouter()

data_manager = DataManager()


@router.post(
    "/sales_period_by_employee",
    response_model=SalesPeriodResponse
)
def sales_period_by_employee(
    request: SalesPeriodByEmployeeRequest = Body(...)
):
    response = data_manager.get_sales_by_period(
        start_date=request.start_date,
        end_date=request.end_date,
        key="KeyEmployee",
        key_value=request.key_employee
    )

    if not response["status"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )

    return response


@router.post(
    "/sales_period_by_product",
    response_model=SalesPeriodResponse
)
def sales_period_by_product(
    request: SalesPeriodbyProductRequest = Body(...)
):
    response = data_manager.get_sales_by_period(
        start_date=request.start_date,
        end_date=request.end_date,
        key="KeyProduct",
        key_value=request.key_product
    )

    if not response["status"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )

    return response


@router.post(
    "/sales_period_by_store",
    response_model=SalesPeriodResponse
)
def sales_period_by_store(
    request: SalesPeriodbyStoreRequest = Body(...)
):
    response = data_manager.get_sales_by_period(
        start_date=request.start_date,
        end_date=request.end_date,
        key="KeyStore",
        key_value=request.key_store
    )

    if not response["status"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )

    return response


@router.post(
    "/avg_sales_by_employee",
    response_model=AvgSalesResponse
)
def avg_sales_by_employee(
    request: AvgEmployeeRequest = Body(...)
):
    response = data_manager.get_avg_sales_by_period(
        key="KeyEmployee",
        key_value=request.key_employee
    )

    if not response["status"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )

    return response


@router.post(
    "/avg_sales_by_product",
    response_model=AvgSalesResponse
)
def avg_sales_by_product(
    request: AvgProductRequest = Body(...)
):
    response = data_manager.get_avg_sales_by_period(
        key="KeyProduct",
        key_value=request.key_product
    )

    if not response["status"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )

    return response


@router.post(
    "/avg_sales_by_store",
    response_model=AvgSalesResponse
)
def avg_sales_by_store(
    request: AvgStoreRequest = Body(...)
):
    response = data_manager.get_avg_sales_by_period(
        key="KeyStore",
        key_value=request.key_store
    )

    if not response["status"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )

    return response
