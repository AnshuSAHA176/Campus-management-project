
import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = "http://127.0.0.1:8000";


export const options = {
  scenarios: {
    dashboard_load: {
      executor: "ramping-vus",
      startVUs: 10,
      stages: [
        { duration: "1m", target: 100 },
        { duration: "1m", target: 250 },
        { duration: "1m", target: 500 },
        { duration: "2m", target: 1000 },
        { duration: "1m", target: 1000 },
        { duration: "1m", target: 0 },
      ],
      gracefulRampDown: "30s",
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<1000"],
  },
};


export function setup() {
  const response = http.post(
    `${BASE_URL}/login/`,
    JSON.stringify({
      email: __ENV.TEST_EMAIL,
      password: __ENV.TEST_PASSWORD,
    }),
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  const loginOK = check(response, {
    "login successful": (r) => r.status === 200,
  });

  if (!loginOK) {
    throw new Error(
      `Login failed: status=${response.status}, body=${response.body}`
    );
  }

  const token = response.json("access");

  if (!token) {
    throw new Error(
      `Access token missing. Login response: ${response.body}`
    );
  }

  return { token };
}

export default function (data) {
  const response = http.get(`${BASE_URL}/dashboard/`, {
    headers: {
      Authorization: `Bearer ${data.token}`,
    },
  });

  check(response, {
    "dashboard returns 200": (r) => r.status === 200,
  });

  if (response.status !== 200) {
    console.error(
      `Dashboard failed: status=${response.status}, body=${response.body}`
    );
  }

  sleep(1);
}
