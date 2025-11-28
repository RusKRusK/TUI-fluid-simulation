import random
import math

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

class FluidSimulation:
    AIR = 0
    WALL = 1
    WATER = 2

    def __init__(self, width=80, height=24):
        self.width = width
        self.height = height
        self.walls = [[False for _ in range(width)] for _ in range(height)]
        self.particles = []
        self.initial_walls = None
        self.initial_particles = None
        
        # 物理定数
        self.gravity = 0.05
        self.max_velocity = 2.0
        self.damping = 0.3
        self.friction = 0.99
        
        # パラメータ
        self.smoothing_radius = 2.0  # 探索半径
        self.repulsion_force = 0.5   # 反発力
        self.cohesion_force = 0.03   # 凝集力

    def load_from_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.height = len(lines)
            self.width = max(len(line.rstrip('\n')) for line in lines) if lines else 0
            
            self.walls = [[False for _ in range(self.width)] for _ in range(self.height)]
            self.particles = []
            
            for y, line in enumerate(lines):
                for x, char in enumerate(line.rstrip('\n')):
                    if x < self.width:
                        if char == '@':
                            self.walls[y][x] = True
                        elif char == '#':
                            self.particles.append(Particle(x + 0.5 + random.uniform(-0.1, 0.1), y + 0.5))
                            
            self.initial_walls = [row[:] for row in self.walls]
            self.initial_particles = [(p.x, p.y) for p in self.particles]
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def reset(self):
        if self.initial_walls:
            self.walls = [row[:] for row in self.initial_walls]
            self.particles = [Particle(x, y) for x, y in self.initial_particles]

    def update(self):
        grid_cells = {}
        for p in self.particles:
            cx, cy = int(p.x), int(p.y)
            key = (cx, cy)
            if key not in grid_cells:
                grid_cells[key] = []
            grid_cells[key].append(p)

        for p in self.particles:
            p.vy += self.gravity
            
            cx, cy = int(p.x), int(p.y)
            
            # 周囲の粒子を探す
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    check_key = (cx + dx, cy + dy)
                    if check_key in grid_cells:
                        for neighbor in grid_cells[check_key]:
                            if neighbor is p:
                                continue
                            
                            dist_x = p.x - neighbor.x
                            dist_y = p.y - neighbor.y
                            dist_sq = dist_x**2 + dist_y**2
                            
                            if 0.0001 < dist_sq < self.smoothing_radius**2:
                                dist = math.sqrt(dist_sq)
                                q = dist / self.smoothing_radius
                                
                                if q < 0.5:
                                    # 近すぎる -> 強く反発
                                    force = (0.5 - q) * self.repulsion_force
                                else:
                                    # ちょうどいい距離 -> 弱く引き合う
                                    force = -1 * (q - 0.5) * (1.0 - q) * self.cohesion_force
                                
                                # 力をベクトルに分解して適用
                                fx = (dist_x / dist) * force
                                fy = (dist_y / dist) * force
                                
                                p.vx += fx
                                p.vy += fy

        # 位置の更新と壁衝突
        for p in self.particles:
            p.vx *= self.friction
            p.vy *= self.friction
            
            speed_sq = p.vx**2 + p.vy**2
            if speed_sq > self.max_velocity**2:
                scale = self.max_velocity / math.sqrt(speed_sq)
                p.vx *= scale
                p.vy *= scale

            next_x = p.x + p.vx
            next_y = p.y + p.vy
            
            # X衝突
            cx = int(next_x)
            cy = int(p.y)
            if cx < 0 or cx >= self.width or (0 <= cy < self.height and self.walls[cy][cx]):
                p.vx *= -self.damping
                p.x += p.vx 
            else:
                p.x = next_x

            # Y衝突
            cx = int(p.x)
            cy = int(next_y)
            if cy < 0 or cy >= self.height or (0 <= cx < self.width and self.walls[cy][cx]):
                p.vy *= -self.damping
                p.vx *= 0.9 
                p.y += p.vy
            else:
                p.y = next_y

    def get_render_text(self):
        # レンダリング部分
        render_grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                if self.walls[y][x]:
                    render_grid[y][x] = "[bold white]█[/]"

        for p in self.particles:
            x, y = int(p.x), int(p.y)
            if 0 <= x < self.width and 0 <= y < self.height:
                if not self.walls[y][x]:
                    render_grid[y][x] = "[bold #0067AC]█[/]"
        
        return "\n".join("".join(row) for row in render_grid)