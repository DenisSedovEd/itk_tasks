import time
import threading
import pytest
from redis import Redis
from rate_limiter import RateLimiter


class TestRateLimiter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.redis = Redis(host='localhost', port=6379, db=0)
        self.redis.flushdb()  # Clean Redis before each test
        self.client_id = "test_client"
        self.rate_limiter = RateLimiter(max_requests=3, time_window=2)  # 3 requests per 2 seconds

    def test_single_request_allowed(self):
        assert self.rate_limiter.test(self.client_id) is True

    def test_multiple_requests_within_limit(self):
        for _ in range(3):
            assert self.rate_limiter.test(self.client_id) is True

    def test_exceeding_limit(self):
        # First 3 requests should pass
        for _ in range(3):
            assert self.rate_limiter.test(self.client_id) is True

        # 4th request should be blocked
        assert self.rate_limiter.test(self.client_id) is False

    def test_window_reset_after_time(self):
        # Use up all requests
        for _ in range(3):
            self.rate_limiter.test(self.client_id)

        # Wait for the time window to reset
        time.sleep(2.1)

        # Should allow new requests
        assert self.rate_limiter.test(self.client_id) is True

    def test_concurrent_requests(self):
        results = []

        def make_request():
            results.append(self.rate_limiter.test(self.client_id))

        # Create multiple threads to simulate concurrent requests
        threads = []
        for _ in range(5):  # More than the limit
            t = threading.Thread(target=make_request)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Only 3 requests should be allowed
        assert sum(results) == 3

    def test_different_clients_dont_interfere(self):
        client1 = "client1"
        client2 = "client2"

        # Both clients should be able to make 3 requests each
        for _ in range(3):
            assert self.rate_limiter.test(client1) is True
            assert self.rate_limiter.test(client2) is True

        # Both should be blocked on the 4th request
        assert self.rate_limiter.test(client1) is False
        assert self.rate_limiter.test(client2) is False


if __name__ == "__main__":
    # Manual test without pytest
    limiter = RateLimiter(max_requests=3, time_window=2)
    client = "test_client"

    print("Testing basic rate limiting (3 requests per 2 seconds):")
    for i in range(5):
        allowed = limiter.test(client)
        print(f"Request {i + 1}: {'Allowed' if allowed else 'Blocked'}")

    print("\nWaiting for time window to reset...")
    time.sleep(2.1)
    print(f"After reset: {'Allowed' if limiter.test(client) else 'Blocked'}")