# Databricks notebook source
# MAGIC %pip install torch
# MAGIC import torch
# MAGIC x= torch.linspace(-1, 1, 2000, dtype=torch.float)
# MAGIC print(x)
# MAGIC
# MAGIC z = torch.ones((5), dtype=torch.float)
# MAGIC print(z)

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(1) from stock.finhub_bronze
