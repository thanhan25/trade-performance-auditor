class TradeAuditorError(Exception):
    """Base domain error for all trade performance auditing tasks."""

    pass


class DataWarehouseIngestionError(TradeAuditorError):
    """Raised when log data extraction, filtering, or warehouse loading fails."""

    pass


class QueryExecutionError(TradeAuditorError):
    """Raised when analytical queries or reporting tools hit runtime exceptions."""

    pass
