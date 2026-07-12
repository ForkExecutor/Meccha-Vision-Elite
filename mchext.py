#!/usr/bin/env python3

import random
from collections import namedtuple

# Simple data structure to hold player camouflage data
PlayerData = namedtuple('PlayerData', ['player_id', 'position', 'camouflage_color', 'is_hiding'])

class CamouflageDetector:
    """Algorithm to detect poorly hidden players based on camouflage quality"""
   
    
    def rgb_to_lab(self, r, g, b):
        """Convert RGB to LAB color space for better color difference calculation"""
        # Convert RGB to XYZ (simplified)
        r, g, b = r/255, g/255, b/255
        g = g/12.92 if g <= 0.04045 else ((g+0.055)/1.055)**2.4
        b = b/12.92 if b <= 0.04045 else ((b+0.055)/1.055)**2.4
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        # Convert XYZ to LAB (simplified for demo)
        return (x * 100, y * 100, z * 100)
    
    def color_difference(self, color1, color2):
        """Calculate difference between two colors (higher = more different)"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        # Simple Euclidean distance in RGB space
        return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)
    
    def analyze_position_quality(self, position, environment_colors):
        """
        Analyze if player position is a good hiding spot.
        Returns a quality score from 0 (worst) to 100 (best)
        """
        # In a real implementation, this would check:
        # - Is the player near objects that provide cover?
        # - Is the player in an exposed area?
        # - Does the player's orientation match the environment?
        # Simplified for demo:
        cover_score = random.randint(20, 90)  # Placeholder
        return cover_score
    
    def calculate_camouflage_quality(self, player_color, environment_color):
        """
        Calculate camouflage quality based on color matching.
        Returns a score from 0 (terrible camouflage) to 100 (perfect)
        """
        diff = self.color_difference(player_color, environment_color)
        # Max difference in RGB is ~442, so we scale to 0-100
        quality = max(0, 100 - (diff / 442 * 100))
        return int(quality)
    
    def process_player(self, player_data, environment_color):
        """Process a single player and determine if they should be highlighted"""
        # Calculate camouflage quality
        camo_quality = self.calculate_camouflage_quality(
            player_data.camouflage_color, 
            environment_color
        )
        
        # Calculate position quality
        pos_quality = self.analyze_position_quality(
            player_data.position,
            environment_color
        )
        
        # Overall camouflage score (weighted)
        overall_score = (camo_quality * 0.7) + (pos_quality * 0.3)
        
        # Determine if player should be highlighted
        is_poorly_hidden = overall_score < self.sensitivity and not player_data.is_hiding
        
        result = {
            'player_id': player_data.player_id,
            'camouflage_quality': camo_quality,
            'position_quality': pos_quality,
            'overall_score': overall_score,
            'is_poorly_hidden': is_poorly_hidden
        }
        
        if is_poorly_hidden:
            self.highlight_list.append(player_data.player_id)
        
        return result
    
    def run_detection(self, players, environment_color):
        """Run detection on all players and return results"""
        results = []
        self.highlight_list = []
        
        for player in players:
            result = self.process_player(player, environment_color)
            results.append(result)
        
        return results

# Example usage
if __name__ == "__main__":
    print("=== Mecha Chameleon Camouflage Detector (Demo) ===")
    
    # Create a test environment
    environment = (120, 100, 80)  # RGB for environment
    
    # Create some test players
    players = [
        PlayerData(1, (100, 50, 0), (120, 100, 80), False),   # Perfect match (green grass)
        PlayerData(2, (200, 150, 0), (255, 0, 0), False),      # Red on grass (bad camouflage)
        PlayerData(3, (50, 200, 0), (80, 60, 40), True),       # Hiding, darker color
        PlayerData(4, (300, 100, 0), (200, 200, 200), False),  # Bright white in forest
    ]
    
    detector = CamouflageDetector(sensitivity=70)
    results = detector.run_detection(players, environment)
    
    print(f"\nEnvironment color: {environment}")
    print(f"Sensitivity threshold: {detector.sensitivity}%\n")
    
    for result in results:
        status = "⚠️ POORLY HIDDEN" if result['is_poorly_hidden'] else "✅ OK"
        print(f"Player {result['player_id']}: Quality {result['overall_score']}% - {status}")
    
    print(f"\nHighlighting players with IDs: {detector.highlight_list}")
    print("\n📦 The full assistant with real-time detection is available in Releases.")