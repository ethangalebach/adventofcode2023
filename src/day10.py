import utils
import time
import numpy as np
import networkx as nx
from shapely import Polygon, Point
import geopandas as gpd
import itertools

input_path = utils.get_input_path(__file__)

def traverse(c, pipe, grid):
    y,x=c
    node=pipe.nodes[c]
    if (node.get('tile') == '|' and node.get('indir') == "up") or \
       (node.get('tile') == 'L' and node.get('indir') == "left") or \
       (node.get('tile') == 'J' and node.get('indir') == "right"):
            indir="up"
            newc=(y-1,x)
            tile=grid[y-1,x]
    if (node.get('tile') == '|' and node.get('indir') == "down") or \
       (node.get('tile') == 'F' and node.get('indir') == "left") or \
       (node.get('tile') == '7' and node.get('indir') == "right"):
            indir="down"
            newc=(y+1,x)
            tile=grid[y+1,x]
    if (node.get('tile') == '-' and node.get('indir') == "right") or \
       (node.get('tile') == 'L' and node.get('indir') == "down") or \
       (node.get('tile') == 'F' and node.get('indir') == "up"):
            indir="right"
            newc=(y,x+1)
            tile=grid[y,x+1]
    if (node.get('tile') == '-' and node.get('indir') == "left") or \
       (node.get('tile') == 'J' and node.get('indir') == "down") or \
       (node.get('tile') == '7' and node.get('indir') == "up"):
            indir="left"
            newc=(y,x-1)
            tile=grid[y,x-1]
    pipe.add_node(newc,indir=indir,tile=tile,step=node.get('step')+1)
    pipe.add_edge(c,newc)
    return newc


def get_pipe(grid,start):
    pipe = nx.DiGraph()
    pipe.add_node(start,step=0)
    maxy, maxx = (d-1 for d in grid.shape)
    y = start[0]
    x = start[1]
    c1 = c2 = None
    if y > 0 and grid[y-1,x] in ('7','F','|'):
        c1 = (y-1,x)
        c1dir='up'
        c1tile=grid[y-1,x]
    if y < maxy and grid[y+1,x] in ('L','J','|'):
        if c1:
            c2 = (y+1,x)
            c2dir='down'
            c2tile=grid[y+1,x]
        else:
            c1 = (y+1,x)
            c1dir='down'
            c1tile=grid[y+1,x]
    if x > 0 and grid[y,x-1] in ('L','F','-'):
        if c1:
            c2 = (y,x-1)
            c2dir='left'
            c2tile=grid[y,x-1]
        else:
            c1 = (y,x-1)
            c1dir='left'
            c1tile=grid[y,x-1]
    if x < maxx and grid[y,x+1] in ('7','J','_'):
        if c1:
            c2 = (y,x+1)
            c2dir='right'
            c2tile=grid[y,x+1]
        else:
            c1 = (y,x+1)
            c1dir='right'
            c1tile=grid[y,x+1]
    pipe.add_node(c1,indir=c1dir,tile=c1tile,step=1)
    pipe.add_node(c2,indir=c2dir,tile=c2tile,step=1)
    pipe.add_edge(start,c1)
    pipe.add_edge(start,c2)
    while c1 != c2:
        c1 = traverse(c1, pipe, grid)
        c2 = traverse(c2, pipe, grid)
    return pipe


def get_grid(path):
    grid = None
    line_num = 0
    with open(path) as f:
        for line in f:
            if line.strip():
                if 'S' in line:
                    start = (line_num, line.index('S'))
                if isinstance(grid, np.ndarray):
                    grid = np.append(grid,[list(line.strip())],axis=0)
                else:
                    grid = np.array([list(line.strip())])
                line_num += 1
    return grid,start


def get_answer(path, part:int):
    grid,start = get_grid(path)
    pipe = get_pipe(grid,start)
    if part == 1:
        return max(data.get('step') for node, data in pipe.nodes(data=True))
    if part == 2:
        points = list(itertools.product(*list(range(d) for d in grid.shape)))
        ordered_nodes = list(pipe.nodes)[::2] + list(pipe.nodes)[::-2]
        polygon = Polygon(ordered_nodes)
        gdf_points = gpd.GeoDataFrame(geometry=[Point(p) for p in points])
        gdf_polygon = gpd.GeoDataFrame(geometry=[polygon])
        #rtrees ftw
        points_in_polygon = gpd.sjoin(
             gdf_points, gdf_polygon, how="inner", predicate='within')
        return len(points_in_polygon)


def run(part:int, test_expected):
    test_path = utils.get_test_path(__file__, part)
    test_answer = get_answer(test_path, part=part)
    assert test_answer ==  test_expected, (
        f"got {test_answer}, should be {test_expected}"
    )
    start_time = time.time()
    answer = get_answer(input_path, part=part)
    end_time = time.time()
    duration = 1000*(end_time - start_time)
    print(f"Part {part} Answer: {answer}, in {duration} ms")


if __name__ == "__main__":
    run(part=1,test_expected=8)
    run(part=2,test_expected=10)