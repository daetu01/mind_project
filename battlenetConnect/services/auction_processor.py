class AuctionProcessor:
    def process(self, auctions_data: dict) -> dict:
        """
        Summarizes large auction data.
        Returns total count and top 20 items by occurrence as a sample.
        """
        auctions = auctions_data.get("auctions", [])
        total_auctions = len(auctions)
        
        # Group by item ID and collect prices
        item_stats = {}
        for ah in auctions:
            item_id = ah.get("item", {}).get("id")
            if not item_id:
                continue
            
            # Use unit_price (commodities) or buyout (other items)
            price = ah.get("unit_price") or ah.get("buyout")
            if price is None:
                continue

            if item_id not in item_stats:
                item_stats[item_id] = []
            item_stats[item_id].append(price)
        
        # Calculate summary for top 20 items by frequency
        sorted_item_ids = sorted(item_stats.keys(), key=lambda x: len(item_stats[x]), reverse=True)[:20]
        
        요약 = []
        for item_id in sorted_item_ids:
            prices = item_stats[item_id]
            요약.append({
                "아이템아이디": item_id,
                "수량": len(prices),
                "최저가": min(prices),
                "최고가": max(prices),
                "평균가": round(sum(prices) / len(prices), 2)
            })
        
        return {
            "총_경매수": total_auctions,
            "인기_아이템_요약": 요약
        }

auction_processor = AuctionProcessor()
