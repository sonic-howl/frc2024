import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class SampleTest {
  // You can define constants to use in your tests here
  static final double DELTA = 0.01;

  @BeforeEach // this method will run before each test
  void setup() {}

  @AfterEach // this method will run after each test
  void shutdown() {}

  @Test // marks this method as a test
  void sampleTest() {
    assertEquals(123, 123);
  }
}
