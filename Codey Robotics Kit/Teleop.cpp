// Motor driver pin definitions
int lmt1 = 5; 
int lmt2 = 3; 
int rmt1 = 6; 
int rmt2 = 11; 

void setup() {
  // Initialize serial communication at 9600 bps
  Serial.begin(9600);
  
  // Set motor pins as outputs
  pinMode(lmt1, OUTPUT);
  pinMode(lmt2, OUTPUT);
  pinMode(rmt1, OUTPUT);
  pinMode(rmt2, OUTPUT);
  
  Serial.println("Controls: 'w' = Forward, 's' = Stop, 'x' = Backward");
}

void loop() {
  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming character
    
    // Execute movement based on the key pressed
    if (command == 'w' || command == 'W') {
      forward();
      Serial.println("Moving Forward");
    } 
    else if (command == 'x' || command == 'X') {
      backward();
      Serial.println("Moving Backward");
    } 
    else if (command == 's' || command == 'S') {
      stopRobot();
      Serial.println("Stopped");
    }
  }
}

// Function to move the robot forward
void forward() {
  analogWrite(lmt1, 150);
  analogWrite(lmt2, 0);
  analogWrite(rmt1, 150);
  analogWrite(rmt2, 0);
}

// Function to move the robot backward
void backward() {
  analogWrite(lmt1, 0);
  analogWrite(lmt2, 150);
  analogWrite(rmt1, 0);
  analogWrite(rmt2, 150);
}

// Function to stop the robot
void stopRobot() {
  analogWrite(lmt1, 0);
  analogWrite(lmt2, 0);
  analogWrite(rmt1, 0);
  analogWrite(rmt2, 0);
}
