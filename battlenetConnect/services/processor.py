from datetime import datetime

class DataProcessor:
    def process(self, profile: dict, equipment: dict, stats: dict, specs: dict) -> dict:
        refined = {
            "아이디": profile.get("id"),
            "이름": profile.get("name"),
            "성별": profile.get("gender", {}).get("name"),
            "종족": profile.get("race", {}).get("name"),
            "직업": profile.get("character_class", {}).get("name"),
            "전문화": profile.get("active_spec", {}).get("name"),
            "서버": profile.get("realm", {}).get("name"),
            "레벨": profile.get("level"),
            "업적점수": profile.get("achievement_points"),
            "마지막접속": self._format_timestamp(profile.get("last_login_timestamp")),
            "평균아이템레벨": profile.get("average_item_level"),
            "착용아이템레벨": profile.get("equipped_item_level"),
            "전투능력치": self._process_combat_stats(stats),
            "특성정보": self._process_talents(specs),
            "장비": [
                {
                    "부위": item.get("slot", {}).get("name"),
                    "아이템명": item.get("name"),
                    "아이템아이디": item.get("item", {}).get("id"),
                    "품질": item.get("quality", {}).get("name"),
                    "아이템레벨": item.get("level", {}).get("value"),
                    "능력치": self._extract_stats(item.get("stats")),
                    "보석홈": self._extract_sockets(item.get("sockets")),
                    "마법부여": self._extract_enchantments(item.get("enchantments"))
                }
                for item in equipment.get("equipped_items", [])
            ]
        }
        return refined

    def _process_combat_stats(self, stats):
        if not stats: return {}
        
        def safe_get(obj, key, subkey="effective"):
            val = obj.get(key)
            if isinstance(val, dict):
                return val.get(subkey)
            return val # Fallback to direct value if not a dict

        return {
            "주능력치": {
                "힘": safe_get(stats, "strength"),
                "민첩": safe_get(stats, "agility"),
                "지능": safe_get(stats, "intellect"),
                "체력": safe_get(stats, "stamina")
            },
            "보조능력치": {
                "치명타": f"{safe_get(stats, 'crit', 'value')}%",
                "가속": f"{safe_get(stats, 'haste', 'value')}%",
                "특화": f"{safe_get(stats, 'mastery', 'value')}%",
                "유연성": f"{safe_get(stats, 'versatility', 'value')}%"
            }
        }

    def _process_talents(self, specs):
        if not specs: return []
        active_spec = next((s for s in specs.get("specializations", []) if s.get("specialization", {}).get("id") == specs.get("active_specialization", {}).get("id")), None)
        if not active_spec: return []
        
        return [
            {
                "이름": t.get("talent", {}).get("name"),
                "설명": t.get("spell_tooltip", {}).get("description"),
                "레벨": t.get("level")
            }
            for t in active_spec.get("loadouts", [{}])[0].get("selected_talents", [])
            if t.get("talent") # Filter for actual talents
        ]

    def _format_timestamp(self, ts):
        if not ts: return None
        dt = datetime.fromtimestamp(ts / 1000.0)
        return dt.strftime('%Y. %m. %d. %p %I:%M:%S').replace('AM', '오전').replace('PM', '오후')

    def _extract_stats(self, stats):
        if not stats: return []
        return [
            {"종류": s.get("type", {}).get("name"), "수치": s.get("value")}
            for s in stats
        ]

    def _extract_sockets(self, sockets):
        if not sockets: return []
        return [
            {
                "종류": s.get("socket_type", {}).get("name"),
                "아이템": {"아이템명": s.get("item", {}).get("name"), "아이템아이디": s.get("item", {}).get("id")} if s.get("item") else None
            }
            for s in sockets
        ]

    def _extract_enchantments(self, enchantments):
        if not enchantments: return []
        return [
            {
                "설명": e.get("display_string"),
                "출처": {"아이템명": e.get("source_item", {}).get("name"), "아이템아이디": e.get("source_item", {}).get("id")} if e.get("source_item") else None
            }
            for e in enchantments
        ]

processor = DataProcessor()
