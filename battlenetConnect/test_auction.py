import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "battlenetConnect")))

from services.auction_processor import auction_processor

def test_auction_processing():
    # Mock data: 
    # Item 101: 3 auctions with unit_price (commodity)
    # Item 202: 2 auctions with buyout (gear)
    mock_data = {
        "auctions": [
            {"item": {"id": 101}, "unit_price": 100, "quantity": 10},
            {"item": {"id": 101}, "unit_price": 200, "quantity": 5},
            {"item": {"id": 101}, "unit_price": 150, "quantity": 1},
            {"item": {"id": 202}, "buyout": 1000},
            {"item": {"id": 202}, "buyout": 2000},
            {"item": {"id": 303}, "bid": 500} # No buyout/unit_price, should be ignored
        ]
    }
    
    result = auction_processor.process(mock_data)
    
    print("Result:", result)
    
    summaries = result["인기_아이템_요약"]
    assert len(summaries) == 2 # 101 and 202
    
    # Check Item 101
    item101 = next(i for i in summaries if i["아이템아이디"] == 101)
    assert item101["수량"] == 3
    assert item101["최저가"] == 100
    assert item101["최고가"] == 200
    assert item101["평균가"] == 150.0
    
    # Check Item 202
    item202 = next(i for i in summaries if i["아이템아이디"] == 202)
    assert item202["수량"] == 2
    assert item202["최저가"] == 1000
    assert item202["최고가"] == 2000
    assert item202["평균가"] == 1500.0
    
    print("Test passed!")

if __name__ == "__main__":
    try:
        test_auction_processing()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
