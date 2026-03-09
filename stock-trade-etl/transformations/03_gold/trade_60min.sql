CREATE or REPLACE MATERIALIZED VIEW gld_stock_trade_60min AS
select
  s.symbol,
  sum(s.volume) volume_sum,
  avg(s.price) price_avg,
  FROM_UNIXTIME(FLOOR(s.timestamp / 1000 / 3600) * 3600) AS timewindow
from
  stock.finhub_silver s
group by
  symbol,
  timewindow