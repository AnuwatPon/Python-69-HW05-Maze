def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
  from collections import deque

def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    rows = len(maze)
    cols = len(maze[0])
    
    # ค้นหาจุดเริ่มต้น 'S' และจุดสิ้นสุด 'E'
    start = None
    end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
                
    if not start or not end:
        return {"distance": -1, "path": []}

    # ทิศทางการเคลื่อนที่ 4 ทิศทาง (ขวา, ลง, ซ้าย, ขึ้น)
    directions = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0)
    }
    
    # การเดินปกติ 4 ทิศทาง
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    def simulate_conveyor(r, c):
        """จำลองการไหลของสายพานแบบฟรี (0 ก้าว)"""
        curr_r, curr_c = r, c
        path_segment = []
        visited_on_belt = set()
        
        while True:
            cell = maze[curr_r][curr_c]
            path_segment.append([curr_r, curr_c])
            
            # ถ้าไม่ใช่อักขระสายพาน ให้หยุดการไหล
            if cell not in directions:
                return (curr_r, curr_c), path_segment, True
            
            # ป้องกันการวนลูปไม่รู้จบ (Infinite loop บนสายพาน)
            if (curr_r, curr_c) in visited_on_belt:
                return None, [], False
            visited_on_belt.add((curr_r, curr_c))
            
            # เลื่อนไปตามทิศทางของสายพาน
            dr, dc = directions[cell]
            next_r, next_c = curr_r + dr, curr_c + dc
            
            # ชนกำแพงหรือตกขอบตาราง ให้ถือว่าก้าวเข้าสายพานนี้ไม่ได้
            if not (0 <= next_r < rows and 0 <= next_c < cols) or maze[next_r][next_c] == '#':
                return None, [], False
            
            curr_r, curr_c = next_r, next_c

    # BFS สำหรับหาเส้นทางที่สั้นที่สุด
    # queue เก็บ (ค่าก้าวเดิน, ตำแหน่งปัจจุบัน (r, c), เส้นทางเดินทาง [path])
    queue = deque([(0, start[0], start[1], [[start[0], start[1]]])])
    visited = {(start[0], start[1]): 0}

    while queue:
        dist, r, c, path = queue.popleft()
        
        if (r, c) == end:
            return {"distance": dist, "path": path}
            
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            
            # ตรวจสอบว่าอยู่ในกริดและไม่ใช่กำแพง
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
                # กรณีตกใส่สายพาน
                if maze[nr][nc] in directions:
                    final_pos, belt_path, valid = simulate_conveyor(nr, nc)
                    if valid and final_pos is not None:
                        fr, fc = final_pos
                        new_dist = dist + 1
                        new_path = path + belt_path
                        
                        if (fr, fc) not in visited or new_dist < visited[(fr, fc)]:
                            visited[(fr, fc)] = new_dist
                            queue.append((new_dist, fr, fc, new_path))
                # กรณีตกใส่ช่องปกติ ('.', 'E')
                else:
                    new_dist = dist + 1
                    new_path = path + [[nr, nc]]
                    if (nr, nc) not in visited or new_dist < visited[(nr, nc)]:
                        visited[(nr, nc)] = new_dist
                        queue.append((new_dist, nr, nc, new_path))
                        
    return {"distance": -1, "path": []}

# --- ทดสอบตามโจทย์ ---
if __name__ == "__main__":
    # ชุดที่ 1
    maze1 = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    print("Test 1 Result:", maze_solver_with_conveyors(maze1))

    # ชุดที่ 2
    maze2 = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    print("Test 2 Result:", maze_solver_with_conveyors(maze2))

    # ชุดที่ 3
    maze3 = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    print("Test 3 Result:", maze_solver_with_conveyors(maze3))
