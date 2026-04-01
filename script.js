import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },  // 1분 동안 유저를 50명까지 서서히 올림
    { duration: '3m', target: 50 },  // 3분 동안 50명 유지
    { duration: '1m', target: 0 },   // 1분 동안 다시 0명으로 내림
  ],
};

export default function () {
  // 내 API 주소로 변경하세요!
  http.get('https://daiswhat.com/api/raids'); 
  sleep(1); // 1초마다 한 번씩 요청
}