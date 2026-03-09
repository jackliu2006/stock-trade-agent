CREATE or REPLACE MATERIALIZED VIEW gld_stock_trade_day AS
select
  s.symbol,
  sum(s.volume) volume_sum,
  avg(s.price) price_avg,
  max(s.price) price_max,
  min(s.price) price_min,
  FROM_UNIXTIME(FLOOR(s.timestamp / 1000 / 86400) * 86400) AS timewindow
from
  stock.finhub_silver s
group by
  symbol,
  timewindow