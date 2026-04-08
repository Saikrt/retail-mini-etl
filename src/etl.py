import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta
import random


def create_synthetic_data():
    """Create synthetic orders data with some missing values"""
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'USB Cable', 'Desk Chair', 'Desk Lamp', 'Phone Stand']
    
    data = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(1, 31):  # 30 rows
        order_date = base_date + timedelta(days=random.randint(0, 90))
        product = random.choice(products)
        
        # Occasionally leave quantity blank (about 20% of the time)
        if random.random() < 0.2:
            quantity = ''
        else:
            quantity = random.randint(1, 10)
        
        unit_price = round(random.uniform(10.0, 500.0), 2)
        
        data.append({
            'order_id': f'ORD{i:03d}',
            'order_date': order_date.strftime('%Y-%m-%d'),
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price
        })
    
    return pd.DataFrame(data)


def extract():
    """Extract data from CSV or create synthetic data if file doesn't exist"""
    raw_file = 'data/raw/orders.csv'
    
    if not os.path.exists(raw_file):
        print("Creating synthetic data...")
        os.makedirs(os.path.dirname(raw_file), exist_ok=True)
        df = create_synthetic_data()
        df.to_csv(raw_file, index=False)
        print(f"Created {raw_file} with {len(df)} rows")
    else:
        print(f"Reading existing data from {raw_file}")
        df = pd.read_csv(raw_file)
    
    return df


def transform(df):
    """Transform the data: clean types, fill missing values, calculate revenue"""
    print("Transforming data...")
    
    # Replace empty strings with NaN for quantity
    df['quantity'] = df['quantity'].replace('', pd.NA)
    
    # Fill missing quantity with 1
    df['quantity'] = df['quantity'].fillna(1)
    
    # Convert data types
    df['quantity'] = df['quantity'].astype(int)
    df['unit_price'] = df['unit_price'].astype(float)
    
    # Calculate revenue
    df['revenue'] = df['quantity'] * df['unit_price']
    
    # Convert order_date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    print(f"Transformed {len(df)} rows")
    return df


def load(df):
    """Load data to CSV and SQLite database"""
    print("Loading data...")
    
    # Create directories if they don't exist
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('db', exist_ok=True)
    
    # Save to CSV
    csv_path = 'data/processed/orders_clean.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved cleaned data to {csv_path}")
    
    # Save to SQLite
    db_path = 'db/orders.db'
    conn = sqlite3.connect(db_path)
    
    # Replace table if it exists
    df.to_sql('orders_clean', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Saved cleaned data to {db_path}")


def calculate_kpis(df):
    """Calculate and print KPIs"""
    print("\n=== KPIs ===")
    
    total_orders = len(df)
    total_revenue = df['revenue'].sum()
    top_product = df.groupby('product')['revenue'].sum().idxmax()
    
    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Top Product by Revenue: {top_product}")
    
    return {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'top_product_by_revenue': top_product
    }


def main():
    """Main ETL pipeline"""
    print("Starting ETL pipeline...")
    
    # Extract
    df = extract()
    
    # Transform
    df = transform(df)
    
    # Load
    load(df)
    
    # Calculate KPIs
    kpis = calculate_kpis(df)
    
    print("\nETL pipeline completed successfully!")
    return kpis


if __name__ == "__main__":
    main()
