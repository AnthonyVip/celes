import dask.dataframe as dd
from core.settings import settings


class DataManager:
    def __init__(self):
        self.data_path = settings.data_path
        self.ddf = dd.read_parquet(
            self.data_path,
            engine="pyarrow",
            columns=[
                'KeyEmployee',
                'KeyDate',
                'Qty',
                'Amount',
                'KeyProduct',
                'KeyStore'
            ]
        )
        self.ddf['KeyDate'] = dd.to_datetime(
            self.ddf['KeyDate'],
            format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce'
        )

    def get_sales_by_period(
        self,
        start_date: str,
        end_date: str,
        key: str,
        key_value: str
    ):
        filtered_ddf = self.ddf[
            (self.ddf[key] == key_value) &
            (self.ddf['KeyDate'] >= start_date) &
            (self.ddf['KeyDate'] <= end_date)
        ]

        if len(filtered_ddf) == 0:
            return {
                "status": False,
                "message": "No se encontraron resultados"
            }

        result = filtered_ddf[['Qty', 'Amount']].sum().compute()

        return {
            "status": True,
            "cantidad": result['Qty'],
            "total": round(result['Amount'], 2),
        }

    def get_avg_sales_by_period(
        self,
        key: str,
        key_value: str
    ):
        filtered_ddf = self.ddf[
            (self.ddf[key] == key_value)
        ]

        if len(filtered_ddf) == 0:
            return {
                "status": False,
                "message": "No se encontraron resultados"
            }

        total_sales = filtered_ddf[['Qty']].sum().compute()

        average_sales = total_sales / len(filtered_ddf)

        return {
            "status": True,
            "average_sales": round(average_sales, 2),
            "total_sales": int(total_sales)
        }
