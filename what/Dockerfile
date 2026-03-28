# 1단계: 빌드 환경 (Gradle 8.5 + Java 21)
FROM gradle:8.5-jdk21 AS build
WORKDIR /app
COPY . .
RUN chmod +x ./gradlew
RUN ./gradlew clean build -x test

# 2단계: 실행 환경 (이 부분을 수정하세요!)
# openjdk 대신 eclipse-temurin을 사용합니다.
FROM eclipse-temurin:21-jre-jammy 
WORKDIR /app

# 빌드 단계에서 생성된 jar 파일 복사
COPY --from=build /app/build/libs/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]