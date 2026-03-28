package com.dais.what.rank.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Date;

public class RankDto {

    @Getter
    @Builder
    public static class GET {
        private int rank;
        private String guild;
        private String realm;
        private String boss;
        private String progress;
        private Long bestTime;
        private Double score;
        private int memberCount;

        @JsonFormat(pattern = "yyyy-MM-dd")
        private LocalDate updatedAt; // 기록 달성 시간
    }
}
