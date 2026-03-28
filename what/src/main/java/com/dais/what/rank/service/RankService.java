package com.dais.what.rank.service;

import com.dais.what.rank.domain.Rank;
import com.dais.what.rank.dto.RankDto;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ZSetOperations;
import org.springframework.stereotype.Service;
import tools.jackson.databind.ObjectMapper;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class RankService {

    private final StringRedisTemplate redisTemplate; // Redis 연동 객체
    private final ObjectMapper objectMapper;
    private static final String RANK_KEY = "raid_ranking";

    /**
     * 점수 업데이트: 시간과 인원수를 조합하여 가중치 점수를 만듭니다.
     * 예: (1000000 / 시간초) + (100 / 인원수) 등등
     */
    public void updateScore(Rank rank) {
        // 1. DTO나 필요한 정보를 JSON으로 변환
        String memberData = objectMapper.writeValueAsString(rank); // Jackson 사용

        // 2. 점수 계산
        double score = (10_000_000 - rank.getBestTime()) + (50 - rank.getMemberCount()) * 100;

        // 3. Redis에 JSON 자체를 저장
        redisTemplate.opsForZSet().add(RANK_KEY, memberData, score);
    }

    public List<RankDto.GET> getTopRanks(int start, int end) {
        Set<ZSetOperations.TypedTuple<String>> range =
                redisTemplate.opsForZSet().reverseRangeWithScores(RANK_KEY, start, end);

        if (range == null) return List.of();

        List<ZSetOperations.TypedTuple<String>> list = new ArrayList<>(range);
        List<RankDto.GET> result = new ArrayList<>();

        for (int i = 0; i < list.size(); i++) {
            ZSetOperations.TypedTuple<String> tuple = list.get(i);
            try {
                Rank rank = objectMapper.readValue(tuple.getValue(), Rank.class);

                result.add(RankDto.GET.builder()
                        .rank(start + i + 1) // 🔥 여기서 실시간 순위를 계산 (1등, 2등...)
                        .guild(rank.getGuild())
                        .realm(rank.getRealm())
                        .boss(rank.getBoss())
                        .progress(rank.getProgress())
                        .bestTime(rank.getBestTime())
                                .memberCount(rank.getMemberCount())
                        .score(tuple.getScore()) // Redis에 저장된 계산된 점수
                        .updatedAt(rank.getUpdatedAt())
                        .build());
            } catch (Exception e) {
                System.out.println("❌ 파싱 에러 발생: " + e.getMessage());
            }
        }
        return result;
    }
    // RankService.java 에 추가
    public long getTotalCount() {
        Long count = redisTemplate.opsForZSet().zCard(RANK_KEY);
        return count != null ? count : 0;
    }
}