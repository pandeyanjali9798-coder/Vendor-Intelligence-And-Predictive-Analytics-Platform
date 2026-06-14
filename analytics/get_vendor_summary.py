import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text
import logging
from ingestion_mysql import ingest_mysql

logging.basicConfig(
    Filename = "logs/get_vendor_summary.log",
    level = logging.DEBUG,
    format = "%(asctime)s-%(levelname)s-%(message)s",
    filemode = "a"
)


def create_vendor_summary(engine):
     """ This function will merge the different tables to get overall vendor summary and add new columns in the resultant data."""
     vendor_sales_summary = pd.read_sql("""WITH Freight_summary AS(
     SELECT 
        VendorNumber,
        SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
     ),
     Purchases_summary AS (
        SELECT
              p.VendorNumber,
              p.VendorName,
              p.Brand,
              p.Description,
              p.PurchasePrice,
              pp.Price AS ActualPrice,
              pp.Volume,
              SUM(p.Quantity) AS TotalPurchaseQuantity,
              SUM(p.Dollars) AS TotalPurchaseDollar
        FROM purchases p
        JOIN purchase_prices pp
        ON p.Brand = pp.Brand
        WHERE p.PurchasePrice >0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    
     ),
     Sales_summary AS (
        SELECT 
           VendorNo,
           Brand,
           SUM(SalesQuantity) AS TotalSalesQuantity,
           SUM(SalesDollars) AS TotalSalesDollars,
           SUM(SalesPrice) AS TotalSalesPrice,
           SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo,Brand
     )
     SELECT 
          ps.VendorNumber,
          ps.VendorName,
          ps.Brand,
          ps.Description,
          ps.PurchasePrice,
          ps.ActualPrice,
          ps.Volume,
          ps.TotalPurchaseQuantity,
          ps.TotalPurchaseDollar,
          ss.TotalSalesQuantity,
          ss.TotalSalesDollars,
          ss.TotalSalesPrice,
          ss.TotalExciseTax,
          fs.FreightCost
       FROM Purchases_summary ps
       LEFT JOIN Sales_summary ss
         ON ps.VendorNumber = ss.VendorNo
       AND ps.Brand = ss.Brand
       LEFT JOIN Freight_summary fs
         ON ps.VendorNumber = fs.VendorNumber 
       ORDER BY TotalPurchaseDollar DESC
     """, engine)
     return vendor_sales_summary


def clean_data(df):
     '''' This function will clean the data'''
      #changing the datatype to float
     df['Volume'] = df['Volume'].astype('float64')

      # fill the null values with 0 
     df.fillna(0, inplace=True)

      #remove extra space from categorical columns
     df['VendorName'] = df['VendorName'].str.strip()
     df['Description'] = df['Description'].str.strip()

      # creating the new columns from better analysis
     df['TotalPurchaseQuantity'] = df['TotalPurchaseQuantity'].astype('int64')
     df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollar']
     df['ProfitMargin'] = (df['GrossProfit']/df['TotalSalesDollars'])*100
     df['StockTurnover'] = (df['TotalSalesQuantity']/df['TotalPurchaseQuantity'])
     df['SalestoPurchasesRatio'] = (df['TotalSalesDollars']/df['TotalPurchaseDollar'])

      # removing inf to column 
     df['ProfitMargin'] =  (df['ProfitMargin'].replace([np.inf, -np.inf], 0))

     return df

if __name__ == "__main__":
     #creating database connection
     engine = create_engine("mysql+pymysql://root:Anjali%409798@127.0.0.1:3306/inventory_database")

     logging.info('Creating vendor_sales_summary table......')
     summary_df = create_vendor_summary(engine)
     logging.info(summary_df.head())

     logging.info('Cleaning_data....')
     clean_df = clean_data(summary_df)
     logging.info(clean_df.head())

     logging.info('ingesting data...')
     ingest_mysql(clean_df,'vendor_sales_summary',engine)
     logging.info('Completed')
      