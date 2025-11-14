"""

Welcome to the world of self-driving cars!
This lets you program a racing car that drives itself around a track.

HOW IT WORKS:
- The car has a "laser scanner" that measures distances to walls
- We use this information to decide where to turn and how fast to go
- You can modify the functions below to make your car drive better!
- You have to write the main driving logic in the drive_car() function

List of functions you can use in your driving logic:
- get_current_speed(): Get current speed including any boosts
- clean_laser_data(laser_ranges): Remove rear laser measurements (we only care about seeing the front and sides, ignore back lasers)
- find_distance_changes(laser_ranges): Detect big changes in laser data
- find_walls_and_corners(distance_changes): Identify walls and corners to decide when to turn
- decide_where_to_turn(laser_ranges, important_points): Decide steering angle (How much do we turn? Negative = left, Positive = right)
- decide_how_fast(steering_angle, laser_ranges): Decide speed based on situation (you want to slow down when turning sharply, or when walls are close, speed up when the way is straight and clear))

"""

import numpy as np

class Driver:
    def __init__(self):
        # CAR SETTINGS - Try changing these numbers!
        self.car_speed = 0.5          # How fast should your car go? (0.1 to 1.0)
        self.turn_sensitivity = 0.6   # How quickly should your car turn? (0.1 to 2.0)
        self.safety_distance = 0.3    # How far to stay from walls? (0.1 to 1.0)
        
        # Riskier:
        self.racing_mode = False      # Set to True for faster racing
        self.aggressive_turns = False # Set to True for sharper turns

        # Speed adjustment factors
        self.speed_boost = 1.0        # Speed multiplier (1.0 = normal, can be changed with go_faster/go_slower)
# MAIN DRIVING FUNCTION - The brain of our car!

    def drive_car(self, laser_ranges, car_state=None):
        """
        MAIN FUNCTION: This is where all the driving decisions happen!

        This function is called by the racing simulator many times per second
        to control the car. It decides where to turn and how fast to go.
        
        
        You want to use the functions defined above to help make these decisions. Play around with them
        and see how they affect your ca
        Input:r's driving!

            laser_ranges: List of distances from the laser scanner
            car_state: Information about the car (speed, position, etc.) - optional

        Outputs:
            speed, steering_angle - how fast to go and where to turn
        """



        steering_angle = 0

        speed = self.car_speed

        return speed, steering_angle


    def go_faster(self, amount=0.1):
        """
        Make the car go faster!

        Use this function to increase your car's speed. Great for straight sections!
        You can call this function in your drive_car() method when you want to speed up.

        Input:
            amount: How much faster to go (default: 0.1, range: 0.01 to 0.5)

        Example usage in drive_car():
            if you're on a straight part of the track:
                self.go_faster(0.2)
        """
        self.speed_boost = min(2.0, self.speed_boost + amount)  # Don't go faster than 2x normal speed

    def go_slower(self, amount=0.1):
        """
        Make the car go slower!

        Use this function to decrease your car's speed. Good for tricky corners!
        You can call this function in your drive_car() method when you need to slow down.

        Input:
            amount: How much slower to go (default: 0.1, range: 0.01 to 0.5)

        Example usage in drive_car():
            if you see a sharp turn ahead:
                self.go_slower(0.2)
        """
        self.speed_boost = max(0.1, self.speed_boost - amount)  # Don't go slower than 0.1x normal speed

    def reset_speed(self):
        """
        Reset the car speed back to normal!

        Use this function to go back to your original car_speed setting.
        Call this in your drive_car() method when you want to return to normal speed.
        """
        self.speed_boost = 1.0
        print(f"Speed reset to normal! Speed boost: {self.speed_boost:.1f}x")

    def get_current_speed(self):
        """
        Get your current speed including any speed boosts!

        Outputs:
            float: Your current speed (car_speed * speed_boost)

        Use this in your drive_car() method to get the speed to return:
            return self.get_current_speed(), steering_angle
        """
        return self.car_speed * self.speed_boost

    def clean_laser_data(self, laser_ranges):
        """
        Clean up the laser scanner data by removing measurements from behind the car.

        WHY: The car can't see behind it, so we ignore those measurements to avoid confusion.

        Input:
            laser_ranges: List of distances measured by the laser scanner

        Outputs:
            Cleaned list of laser distances (only the front and sides)
        """
        # Remove 1/8 of the measurements from the beginning and end (behind the car)
        eighth = len(laser_ranges) // 8
        cleaned_data = laser_ranges[eighth:-eighth]

        return cleaned_data

    
    # WALL DETECTION - Find walls and obstacles

    def find_distance_changes(self, laser_ranges):
        """
        Find big changes between laser measurements to detect walls.

        WHY: When there's a big difference between adjacent laser points,
             it usually means there's a wall or obstacle there!

        Input:
            laser_ranges: List of distances measured by the laser scanner

        Outputs:
            List of differences between adjacent laser measurements
        """
        changes = [0.0]  # Start with 0 for the first measurement

        for i in range(1, len(laser_ranges)):
            difference = abs(laser_ranges[i] - laser_ranges[i-1])
            changes.append(difference)

        return changes

    def find_walls_and_corners(self, distance_changes):
        """
        Find important points that represent walls and corners.

        WHY: We need to know where the walls are so we can avoid them!

        Input:
            distance_changes: List of differences between laser measurements

        Outputs:
            List of important wall/corner points that need attention
        """
        important_points = []

        for i, change in enumerate(distance_changes):
            # If there's a big change, it might be a wall or corner
            if change > self.turn_sensitivity:
                important_points.append(i)


        return important_points

    # ============================================================================
    # STEERING - Decide where to turn the car
    # ============================================================================

    def decide_where_to_turn(self, laser_ranges, important_points):
        """
        Decide which direction the car should turn to stay safe.

        WHY: duh

        Input:
            laser_ranges: List of distances measured by the laser scanner
            important_points: List of wall/corner locations to avoid

        Outputs:
            Steering angle: negative = turn left, positive = turn right
        """

        # METHOD 1: Simple - Turn toward the farthest distance
        max_distance = max(laser_ranges)
        best_direction = laser_ranges.index(max_distance)

        # METHOD 2: Advanced - Avoid important points (walls)
        if self.aggressive_turns and important_points:
            # Find the middle gap between important points
            if len(important_points) >= 2:
                gaps = []
                for i in range(len(important_points) - 1):
                    gap_center = (important_points[i] + important_points[i+1]) // 2
                    gaps.append(gap_center)

                if gaps:
                    # Choose the biggest gap
                    best_gap = max(gaps, key=lambda x: laser_ranges[x])
                    best_direction = best_gap

        # Convert direction to steering angle
        # 0 = straight ahead, negative = left, positive = right
        center = len(laser_ranges) // 2
        raw_steering = (best_direction - center) / center

        # Limit how much we can turn
        max_turn = 0.8 if self.racing_mode else 0.5
        steering_angle = max(-max_turn, min(max_turn, raw_steering))


        return steering_angle

    def decide_how_fast(self, steering_angle, laser_ranges):
        """
        Decide how fast the car should go based on the situation.

        WHY: We should slow down when turning sharply or when walls are close!

        Input:
            steering_angle: How much we're turning
            laser_ranges: List of distances measured by the laser scanner

        Outputs:
            Speed value (0.0 = stopped, 1.0 = maximum speed)
        """

        # Base speed
        speed = self.car_speed

        # Slow down for sharp turns
        if abs(steering_angle) > 0.5:
            speed *= 0.7  # Reduce speed by 30% for sharp turns
        elif abs(steering_angle) > 0.3:
            speed *= 0.85  # Reduce speed by 15% for moderate turns

        # Slow down when walls are close
        min_distance = min(laser_ranges)
        if min_distance < self.safety_distance:
            speed *= 0.5  # Slow down a lot when very close to walls

        # Racing mode - go faster on straight sections
        if self.racing_mode and abs(steering_angle) < 0.2 and min_distance > self.safety_distance * 2:
            speed = min(1.0, speed * 1.3)  # Go 30% faster on clear straight sections


        return speed

    
# dont worry about this
    def process_lidar(self, ranges, state=None):
        return self.drive_car(ranges, state)
