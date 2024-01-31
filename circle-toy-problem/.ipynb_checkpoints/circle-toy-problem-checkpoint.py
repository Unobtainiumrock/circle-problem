import numpy as np
import matplotlib.pyplot as plt
from typing import List, Set, Tuple

# My approach:
# We can think of this problem in terms of vectors, their magnitudes, and circles. You sort the list of points in ascending order
# of their vector magnitudes and the magnitudes of these vectors correspond to the radius of a potential largest circle.
# This list is then iterated and on each iteration, we check if there exists a duplicate label seen (duplicate labels are tracked using a Set).
# When we encounter a duplicate label, the previous point visited is the point corresponding to the largest radius we can draw.
# There are two primary edge cases:
    # 1) The last point (i - 1)-th prior to the first duplicate encountered (i)-th shares the same magnitude and label as the point that triggered a duplicate occurrence.
    #    This is handled by making the (i - 2)-th point the valid point; bounds checks are handled as well.
    # 2) There does not exist a valid solution. For example, this can happen if a data set like [([1, 2], 'A'), ([2, 1], 'A')] is given.

# For simplification of this problem, I assume that points that lie "on" the radial shell to be contained within the largest valid circle produced by this radius.

# Define the data type for the structured array
# '2i' means a pair of integers and 'U1' means single-character Unicode string.
data_type = [('coordinate', '2i'), ('label', 'U1')]

def generate_random_data(low: int, high: int, size: int, label_space: List[str]) -> np.ndarray:
    """
    Generates a structured array of random points and corresponding labels. 
    """

    low = -max(abs(low), abs(high))
    high = max(abs(low), abs(high))

    # Create an empty structured array
    random_data_points = np.empty(size, dtype=data_type)

    # Generate and assign random coordinates 
    random_x = rng.integers(low, high, size)
    random_y = rng.integers(low, high, size)
    random_data_points['coordinate'] = np.column_stack((random_x, random_y))

    # Generate and assign random labels
    random_data_points['label'] = np.random.choice(label_space, size=size)

    return random_data_points

def generate_fixed_data(coordinates: np.ndarray, labels: np.ndarray) -> np.ndarray:
    fixed_data_points = np.empty(shape=len(coordinates), dtype=data_type)

    fixed_data_points['coordinate'] = coordinates

    fixed_data_points['label'] = labels

    return fixed_data_points 

def radius_eqn(x: int, y: int, h: int = 0, k: int = 0) -> float:
    """
    Calculates the radius of a circle given a point (x, y) and a center (h, k).
    """
    return np.sqrt((x - h)**2 + (y - k)**2)

# Main script. This is where I randomly generate some data for purposes of testing.
np.random.seed(42)
rng = np.random.default_rng()  
low = 1
high = rng.integers(low + 1, 20)
size = rng.integers(low, 20)
label_space = ['A', 'B', 'C', 'D', 'E', 'F']

def color_map(labels: List[str]) -> List[str]:
    result = []

    for label in labels:
        if label == 'A':
            result.appen('red')
        elif label == 'B':
            result.append('blue')
        elif label == 'C':
            result.append('green')
        elif label == 'D':
            result.append('orange')
        elif label == 'E':
            result.append('purple')
        elif label == 'F':
            result.append('black')
    return result

# Generating random data points with labels
random_data_points = generate_random_data(low, high, size, label_space)

def desmos_formatter(data_points: np.ndarray) -> str:
    """
    Creates something pasteable to put into Desmos to explore and validate approach taken to the problem.

    When pasting into Desmos, adjust the colors of the points to the following scheme
    
    # A is red
    # B is blue
    # C is green
    # D is orange
    # E is purple
    # F is black
    
    These will have to be manually adjusted after pasting, since Desmos doesn't automatically know how to do this.
    """

    magnitudes = np.linalg.norm(data_points['coordinate'], axis=1)
    sorted_indices = np.argsort(magnitudes)
    sorted_data = data_points[sorted_indices]

    coordinates = ""

    for data_point in sorted_data:
        coordinate, _ = data_point
        x, y = coordinate
        coordinates += f"({x}, {y})\n"
    return coordinates

random_desmos_coordinates = desmos_formatter(random_data_points)

print(random_desmos_coordinates)

def find_furthest_valid_point(data: np.ndarray) -> Tuple[np.ndarray, bool]:
    """
    Finds the furthest valid point for which we can create a circle centerted at the origin h = 0, k = 0 with a radius that extends to include it.
    This radius is used in the circle equation r = sqrt[(x - h)^2 + (y - k)^2]
    """
    magnitudes = np.linalg.norm(data['coordinate'], axis=1)
    sorted_indices = np.argsort(magnitudes)
    sorted_data = data[sorted_indices]

    print(f"Sorted random data points: {sorted_data}")

    labels_seen: Set[str] = set()
    last_valid_point = None
    last_unique_label_magnitude = None
    valid_solution = False

    for i, data_point in enumerate(sorted_data):
        current_magnitude = magnitudes[sorted_indices[i]]
        label = data_point['label']

        if label not in labels_seen:
            labels_seen.add(label)
            last_valid_point = data_point['coordinate']
            last_unique_label_magnitude = current_magnitude
            valid_solution = True
        else:
            # Duplicate label found
            if last_unique_label_magnitude != current_magnitude:
                # Different magnitudes, implying the first duplicate label is not the same as the last valid point's label
                return last_valid_point, valid_solution
            elif i > 1 and sorted_data[i - 1]['label'] == label:
                # Implied same magnitude, same label case. Return the point before the last valid point since the current point's label and magnitude are the same as the last valid point's label and magnitude.
                return sorted_data[i - 2]['coordinate'], valid_solution
            else:
                # This would be the case for if we had something like [([1, 2], 'A'), ([2, 1], 'A')], which would mean there does not exist a valid solution.
                return None, False

    return last_valid_point, valid_solution


furthest_point, valid_solution = find_furthest_valid_point(random_data_points)
print(f"Furthest valid point from origin is: {furthest_point}")

if valid_solution:
    furthest_x, furthest_y = furthest_point
    radius = radius_eqn(furthest_x, furthest_y)
    print(f"Radius of the largest valid circle: {radius}")