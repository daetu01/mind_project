package com.dais.what.rank.controller;

import com.dais.what.rank.domain.Rank;
import com.dais.what.rank.dto.RankDto;
import com.dais.what.rank.repository.RankRepository;
import com.dais.what.rank.service.RankService;
import lombok.AllArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


@RestController
@RequiredArgsConstructor
public class RankController {

    private final RankService rankService; // Repository 대신 Service 주입

    @GetMapping("/api/raids")
    public ResponseEntity<Map<String, Object>> getRanks(@RequestParam(defaultValue = "1") int page,
                                                      @RequestParam(defaultValue = "10") int size) {

        // Redis는 0-based index이므로 계산이 필요함
        // 1페이지: 0 ~ 9
        // 2페이지: 10 ~ 19
        int start = (page - 1) * size;
        int end = start + size - 1;

        // 1. 현재 페이지 데이터 가져오기
        List<RankDto.GET> rankList = rankService.getTopRanks(start, end);

        // 2. 전체 데이터 개수 가져오기
        long totalCount = rankService.getTotalCount();

        // 3. 총 페이지 수 계산 (올림 처리)
        int totalPages = (int) Math.ceil((double) totalCount / size);

        // 4. 응답 맵 구성
        Map<String, Object> response = new HashMap<>();
        response.put("data", rankList);          // 랭킹 리스트
        response.put("totalCount", totalCount);  // 전체 아이템 개수
        response.put("totalPages", totalPages);  // 총 페이지 수
        response.put("currentPage", page);       // 현재 페이지 번호
        return ResponseEntity.ok(response);
    }

}
