# 1단계: 빌드 환경
FROM gradle:8.5-jdk21 AS build
WORKDIR /app
COPY . .
RUN chmod +x ./gradlew
# 빌드 시에도 프로파일을 명시하고 싶다면 아래와 같이 수정 가능 (선택사항)
RUN ./gradlew clean build -x test

# 2단계: 실행 환경
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app

# 빌드 단계에서 생성된 jar 파일 복사
# (참고: 빌드 시 plain.jar가 같이 생길 수 있으므로 명확하게 지정하는 게 좋습니다)
COPY --from=build /app/build/libs/*-SNAPSHOT.jar app.jar

EXPOSE 8080

# --- 이 부분이 핵심입니다! ---
# -Dspring.profiles.active=dev 설정을 추가하여 실행합니다.
ENTRYPOINT ["java", "-Dspring.profiles.active=dev", "-jar", "app.jar"]