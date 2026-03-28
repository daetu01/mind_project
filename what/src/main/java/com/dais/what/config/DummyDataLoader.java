package com.dais.what.config;

import com.dais.what.rank.domain.Rank;
import com.dais.what.rank.repository.RankRepository;
import com.dais.what.rank.service.RankService;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Component
@RequiredArgsConstructor
public class DummyDataLoader implements CommandLineRunner {

    private final RankRepository rankRepository;
    private final RankService rankService;

    @Override
    public void run(String... args) throws Exception {
        if (rankRepository.count() == 0) {
            List<Rank> dummyData = new ArrayList<>();
            Random random = new Random();

            String[] guilds = {"데이스", "아즈샤라전사", "코딩마스터", "공대장님제발", "무적의공대", "루페온의희망", "호드의영광", "얼라이언스짱"};
            String[] realms = {"아즈샤라", "윈드러너", "카자크", "줄진", "하이잘", "데스윙"};
            String[] bosses = {"안수레크", "카이베자", "시카란", "라샤난"};

            for (int i = 1; i <= 100; i++) {
                int randomMembers = 10 + random.nextInt(21);
                long randomTime = 600L + random.nextInt(1000);

                dummyData.add(Rank.builder()
                        .ranking(i)
                        .guild(guilds[random.nextInt(guilds.length)] + " " + i)
                        .realm(realms[random.nextInt(realms.length)])
                        .boss(bosses[random.nextInt(bosses.length)])
                        .progress("8/8")
                        .bestTime(randomTime)
                        .memberCount(randomMembers) // 인원수 추가 확인!
                        .updatedAt(LocalDate.now().minusDays(random.nextInt(30)))
                        .build());
            }

            rankRepository.saveAll(dummyData);
            System.out.println("✅ DB 더미 데이터 100개 저장 완료!");

            // 핵심 수정 포인트: 이제 객체 자체를 넘깁니다.
            initRedisRanking();
            System.out.println("🚀 Redis 랭킹 데이터 동기화 완료!");
        }
    }

    public void initRedisRanking() {
        List<Rank> allRecords = rankRepository.findAll();
        for (Rank r : allRecords) {
            // RankService의 바뀐 메서드 형식에 맞춰 객체(r)를 전달합니다.
            rankService.updateScore(r);
        }
    }
}
