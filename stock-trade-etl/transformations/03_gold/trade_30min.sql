CREATE or REPLACE MATERIALIZED VIEW gld_stock_trade_30min AS
select
  symbol,
  volume,
  price,
  CAST(timestamp_millis(timestamp) AS DATE) AS trade_date
from
  stock.finhub_silver
