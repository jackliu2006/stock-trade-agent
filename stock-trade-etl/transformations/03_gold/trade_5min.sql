CREATE or REPLACE MATERIALIZED VIEW gld_stock_trade_5min AS
select
  s.symbol,
  sum(s.volume) volume_sum,
  avg(s.price) price_avg,
  from_unixtime(floor(s.timestamp / 1000 / 300) * 300) as timewindow
from
  stock.finhub_silver s
group by
  symbol,
  timewindow