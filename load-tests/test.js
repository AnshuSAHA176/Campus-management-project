
import http from "k6/http";
import { check, sleep } from "k6";
import { Counter } from "k6/metrics";
import exec from "k6/execution";

const BASE_URL = "http://127.0.0.1:8000";

const dashboardStatuses = new Counter("dashboard_statuses");

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

  if (response.status !== 200) {
    throw new Error(
      `Login failed: status=${response.status}, body=${response.body}`
    );
  }

  const token = response.json("access");

  if (!token) {
    throw new Error("Access token missing from login response");
  }

  console.log("Login successful");
  return { token };
}

export default function (data) {
  const response = http.get(`${BASE_URL}/dashboard/`, {
    headers: {
      Authorization: `Bearer ${data.token}`,
    },
    // Don't retry failed requests automatically.
    redirects: 0,
  });

  dashboardStatuses.add(1, {
    status: String(response.status),
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
