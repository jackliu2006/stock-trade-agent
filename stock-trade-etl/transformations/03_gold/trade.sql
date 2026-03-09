CREATE or REPLACE STREAMING TABLE gld_stock_trade
CLUSTER BY (trade_date) AS
select
  symbol,
  volume,
  price,
  CAST(timestamp_millis(timestamp) AS DATE) AS trade_date,
  date_format(timestamp_millis(timestamp), 'HH:mm:ss') AS trade_time,
  conditions
from
  STREAM(stock.finhub_silver)