import pandas as pd
import sys
import os

# Add src to path so we can import etl
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from etl import transform


def test_revenue_column_exists_and_non_negative():
    """Test that revenue column exists and has no negative values"""
    # Create test data with missing quantity
    test_data = pd.DataFrame({
        'order_id': ['ORD001', 'ORD002', 'ORD003'],
        'order_date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'product': ['Laptop', 'Mouse', 'Keyboard'],
        'quantity': [2, '', 1],  # One missing quantity
        'unit_price': [100.0, 25.0, 50.0]
    })
    
    # Transform the data
    transformed = transform(test_data)
    
    # Check that revenue column exists
    assert 'revenue' in transformed.columns, "Revenue column should exist after transformation"
    
    # Check that all revenue values are non-negative
    assert (transformed['revenue'] >= 0).all(), "All revenue values should be non-negative"
    
    # Check specific calculations
    assert transformed.iloc[0]['revenue'] == 200.0, "Revenue should be 2 * 100.0 = 200.0"
    assert transformed.iloc[1]['revenue'] == 25.0, "Revenue should be 1 * 25.0 = 25.0 (missing quantity filled with 1)"
    assert transformed.iloc[2]['revenue'] == 50.0, "Revenue should be 1 * 50.0 = 50.0"


def test_missing_quantity_filled_with_one():
    """Test that missing quantities are filled with 1"""
    # Create test data with missing quantities
    test_data = pd.DataFrame({
        'order_id': ['ORD001', 'ORD002', 'ORD003', 'ORD004'],
        'order_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
        'quantity': [2, '', None, 3],  # Missing values as empty string and None
        'unit_price': [100.0, 25.0, 50.0, 200.0]
    })
    
    # Transform the data
    transformed = transform(test_data)
    
    # Check that no quantities are missing
    assert transformed['quantity'].isna().sum() == 0, "No quantities should be missing after transformation"
    
    # Check that missing values were filled with 1
    assert transformed.iloc[1]['quantity'] == 1, "Empty string quantity should be filled with 1"
    assert transformed.iloc[2]['quantity'] == 1, "None quantity should be filled with 1"
    
    # Check that original non-missing values are preserved
    assert transformed.iloc[0]['quantity'] == 2, "Original quantity should be preserved"
    assert transformed.iloc[3]['quantity'] == 3, "Original quantity should be preserved"
    
    # Check that quantity is integer type
    assert transformed['quantity'].dtype == 'int', "Quantity should be integer type"
