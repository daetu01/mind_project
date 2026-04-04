class LeaderboardProcessor:
    def __init__(self):
        # Mapping Spec ID -> (Class Name, Spec Name)
        # Just a few common ones for demonstration, 
        # In a real app, this should be fetched from /data/wow/playable-specialization/index
        self.spec_to_class = {
            250: ("죽음의 기사", "혈기"), 251: ("죽음의 기사", "냉기"), 252: ("죽음의 기사", "부정"),
            577: ("악마사냥꾼", "파멸"), 581: ("악마사냥꾼", "복수"),
            102: ("드루이드", "조드"), 103: ("드루이드", "야드"), 104: ("드루이드", "수드"), 105: ("드루이드", "회드"),
            253: ("사냥꾼", "야냥"), 254: ("사냥꾼", "격냥"), 255: ("사냥꾼", "생냥"),
            62: ("마법사", "비법"), 63: ("마법사", "화법"), 64: ("마법사", "냉법"),
            268: ("수도사", "양조"), 270: ("수도사", "운무"), 269: ("수도사", "풍운"),
            65: ("성기사", "신기"), 66: ("성기사", "보기"), 70: ("성기사", "징기"),
            256: ("사제", "수사"), 257: ("사제", "신사"), 258: ("사제", "암사"),
            259: ("도적", "암살"), 260: ("도적", "무법"), 261: ("도적", "잠행"),
            262: ("주술사", "정술"), 263: ("주술사", "고술"), 264: ("주술사", "복술"),
            265: ("흑마법사", "고흑"), 266: ("흑마법사", "악흑"), 267: ("흑마법사", "파흑"),
            71: ("전사", "무전"), 72: ("전사", "분전"), 73: ("전사", "방전"),
            1467: ("기오만", "황폐"), 1468: ("기오만", "보존"), 1473: ("기오만", "증강")
        }

    def process(self, data: dict) -> dict:
        """
        Processes Mythic Leaderboard data to extract class distribution.
        """
        rankings = data.get("leading_groups", [])
        total_groups = len(rankings)
        
        distribution = {}
        for group in rankings:
            members = group.get("members", [])
            for m in members:
                spec_id = m.get("specialization", {}).get("id")
                class_info = self.spec_to_class.get(spec_id)
                
                if class_info:
                    class_name, spec_name = class_info
                    key = f"{class_name} ({spec_name})"
                else:
                    key = f"Unknown (ID: {spec_id})"
                
                distribution[key] = distribution.get(key, 0) + 1
        
        # Sort results by count descending
        sorted_dist = dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
        
        return {
            "던전명": data.get("name"),
            "총_기록수": total_groups,
            "직업_분포": sorted_dist
        }

leaderboard_processor = LeaderboardProcessor()
