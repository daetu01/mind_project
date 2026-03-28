package com.dais.what.rank.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Entity
@Getter
@Builder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Table(name = "ranks") // DB에 'ranks'라는 테이블이 생깁니다.
public class Rank {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // 기본키 (자동 증가)

    private int ranking;
    private String guild;
    private String realm;
    private String boss;
    private String progress;
    private Long bestTime;
    private Double score;
    private int memberCount;
    private LocalDate updatedAt;
}
