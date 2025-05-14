from collections import Counter
from pathlib import Path
from typing import List
import argparse

import numpy as np
from scipy.spatial.distance import jensenshannon

# Below is from Nhat. I made some modifications to make sure it works with ProcPainter.

class Map:
    """Constructs a map object from a 2D representation, i.e. a list of strings."""
    def __init__(self, map: List[str]):
        self.map = map
        
    def flatten(self):
        return " ".join(self.map)
    

def hamming_distance(map1: Map, map2: Map) -> int:
    """Returns the Hamming distance between two maps. Lower values indicate more similar maps."""
    return sum([1 for i, j in zip(map1.flatten(), map2.flatten()) if i != j])

def js_divergence(map1: Map, map2: Map) -> float:
    """Returns the Jensen-Shannon divergence between two maps. Lower values indicate more similar maps."""
    def map_to_hist(map: Map):
        return Counter(map.flatten())

    hist1 = map_to_hist(map1)
    hist2 = map_to_hist(map2)
    keys = set(hist1.keys()) | set(hist2.keys())
    hist1 = np.array([hist1[key] for key in keys])
    hist2 = np.array([hist2[key] for key in keys])
    return jensenshannon(hist1, hist2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()                                               
    parser.add_argument("map1", type=str)
    parser.add_argument("map2", type=str)
    parser.add_argument("--hamming", "-m", action='store_true', help='Evaluates maps using Hamming distance')
    parser.add_argument("--jensen", "-j", action='store_true', help='Evaluates maps using Jensen Shannon divergence.')
    parser.add_argument("--all", "-a", action='store_true', help='Evaluates maps using Jensen Shannon divergence.')
    args = parser.parse_args()
    
    map1 = Path(args.map1).read_text().splitlines()
    map2 = Path(args.map2).read_text().splitlines()
    
    if map1 and map2:
        map1 = Map(map1)
        map2 = Map(map2)
    else: 
        print("Please provide two valid map files!")
        exit()
    
    if len(map1.flatten()) != len(map2.flatten()):
        print("Maps are not the same size. Terminating evaluation.")
        exit()
        
    print("MAP 1")
    print(map1.flatten())
    print("MAP 2")
    print(map2.flatten())
    
    if args.hamming:
        h_dist = hamming_distance(map1, map2)
        print("Hamming Distance:", h_dist)
        # print(h_dist)
        
    if args.jensen:
        js_div = js_divergence(map1, map2)
        print(f"Jensen-Shannon Divergence: {f"{js_div:.3f}"}")
        # print(js_div)
        
    if args.all:
        h_dist = hamming_distance(map1, map2)
        js_div = js_divergence(map1, map2)
        print("Hamming Distance:", h_dist)
        print(f"Jensen-Shannon Divergence: {f"{js_div:.3f}"}")
        
    # Check that maps are the same size.
    # print(len(map1.flatten()))
    # print(len(map2.flatten()))

    