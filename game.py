import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphics Algorithm Visualizer - Final")

WHITE = (255, 255, 255)
BLACK = (15, 15, 15)
GREEN = (0, 255, 0)
RED = (255, 80, 80)
BLUE = (80, 160, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()

points = []
mode = "DDA"
compare_mode = False
shape = "LINE"

#Transform values
tx, ty = 0, 0
angle = 0
scale = 1
transform_active = False

#Animation
anim_x = 0
direction = 1

#algo
def draw_dda(x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x1, y1

    for _ in range(int(steps)):
        pygame.draw.circle(screen, color, (int(x), int(y)), 2)
        x += x_inc
        y += y_inc


def draw_bresenham(x1, y1, x2, y2, color):
    x, y = x1, y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx):
            pygame.draw.circle(screen, color, (x, y), 2)
            x += sx
            if p >= 0:
                y += sy
                p += 2 * (dy - dx)
            else:
                p += 2 * dy
    else:
        p = 2 * dx - dy
        for _ in range(dy):
            pygame.draw.circle(screen, color, (x, y), 2)
            y += sy
            if p >= 0:
                x += sx
                p += 2 * (dx - dy)
            else:
                p += 2 * dx


#transformation
def transform(x, y, cx, cy):
    #Move to origin (center)
    x -= cx
    y -= cy

    #Scaling
    x *= scale
    y *= scale

    #Rotation
    rad = math.radians(angle)
    xr = x * math.cos(rad) - y * math.sin(rad)
    yr = x * math.sin(rad) + y * math.cos(rad)

    #Move back
    xr += cx
    yr += cy

    #Translation
    xr += tx
    yr += ty

    return int(xr), int(yr)

#drawing
def draw_line(p1, p2, color, algorithm, offset_x=0, apply_transform=True):

    if apply_transform:
        cx = (p1[0] + p2[0]) / 2
        cy = (p1[1] + p2[1]) / 2

        x1, y1 = transform(p1[0], p1[1], cx, cy)
        x2, y2 = transform(p2[0], p2[1], cx, cy)
    else:
        x1, y1 = p1
        x2, y2 = p2

    x1 += offset_x
    x2 += offset_x

    #draw (no recursion)
    if algorithm == "DDA":
        draw_dda(x1, y1, x2, y2, color)
    else:
        draw_bresenham(x1, y1, x2, y2, color)
#triangle
def draw_triangle(p1, p2, p3, color, algorithm, offset_x=0, apply_transform=True):

    if apply_transform:
        cx = (p1[0] + p2[0] + p3[0]) / 3
        cy = (p1[1] + p2[1] + p3[1]) / 3

        t1 = transform(p1[0], p1[1], cx, cy)
        t2 = transform(p2[0], p2[1], cx, cy)
        t3 = transform(p3[0], p3[1], cx, cy)
    else:
        t1, t2, t3 = p1, p2, p3

    #offset after transformation
    t1 = (t1[0] + offset_x, t1[1])
    t2 = (t2[0] + offset_x, t2[1])
    t3 = (t3[0] + offset_x, t3[1])

    #draw
    if algorithm == "DDA":
        draw_dda(*t1, *t2, color)
        draw_dda(*t2, *t3, color)
        draw_dda(*t3, *t1, color)
    else:
        draw_bresenham(*t1, *t2, color)
        draw_bresenham(*t2, *t3, color)
        draw_bresenham(*t3, *t1, color)
#text
def draw_text(text, x, y):
    font = pygame.font.SysFont("Arial", 18)
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))


#main loop
running = True
while running:
    screen.fill(BLACK)
    for p in points:
        pygame.draw.circle(screen,(255,234,248),p,5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            points.append(pygame.mouse.get_pos())

            if shape == "LINE" and len(points) > 2:
                points.clear()

            if shape == "TRIANGLE" and len(points) > 3:
                points.clear()

        if event.type == pygame.KEYDOWN:
            

            #Modes
            if event.key == pygame.K_d:
                mode = "DDA"
            elif event.key == pygame.K_b:
                mode = "BRESENHAM"
            elif event.key == pygame.K_m:
                compare_mode = not compare_mode

            #Shapes
            elif event.key == pygame.K_l:
                shape = "LINE"
                points.clear()
            elif event.key == pygame.K_g:
                shape = "TRIANGLE"
                points.clear()

            #Transformations
            elif event.key == pygame.K_t:
                tx += 20
                ty += 20
                transform_active = True
            elif event.key == pygame.K_r:
                angle += 10
                transform_active = True
            #up    
            elif event.key == pygame.K_s:
                scale += 0.2
                transform_active = True
            elif event.key == pygame.K_z:
                tx, ty = 0, 0
                angle = 0
                scale = 1
                transform_active = False    

            #down
            elif event.key==pygame.K_x:
                scale-=0.2
                if scale<0.2:
                    scale=0.2
                transform_active = True    

            elif event.key == pygame.K_c:
                points.clear()

    #Animation
    anim_x += 2 * direction
    if anim_x > 200 or anim_x < -200:
        direction *= -1

    #Divider
    if compare_mode:
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    #Draw Shapes
    if shape == "LINE" and len(points) == 2:
        p1, p2 = points

        if compare_mode:
            draw_line(p1, p2, GREEN, "DDA", 0)
            draw_line(p1, p2, RED, "BRESENHAM", WIDTH // 2)
        else:
            #ORIGINAL
            draw_line(p1, p2, BLUE, mode, apply_transform=False)

            #Editted
            if transform_active:
                draw_line(p1, p2, YELLOW, mode, apply_transform=True)

        #Animation
        draw_line((p1[0] + anim_x, p1[1]),
                  (p2[0] + anim_x, p2[1]),
                  YELLOW, mode)

    elif shape == "TRIANGLE" and len(points) == 3:
        p1, p2, p3 = points

        if compare_mode:
            draw_triangle(p1, p2, p3, GREEN, "DDA", 0)
            draw_triangle(p1, p2, p3, RED, "BRESENHAM", WIDTH // 2)
        else:
            #ORIGINAL
            draw_triangle(p1, p2, p3, BLUE, mode, apply_transform=False)

            #COPY
            if transform_active:
                draw_triangle(p1, p2, p3, YELLOW, mode, apply_transform=True)

        #Animation
        draw_triangle(
            (p1[0] + anim_x, p1[1]),
            (p2[0] + anim_x, p2[1]),
            (p3[0] + anim_x, p3[1]),
            YELLOW,
            mode
        )

    #Text
    draw_text(f"Mode: {mode}", 10, 10)
    draw_text(f"Shape: {shape}", 10, 30)
    draw_text("D: DDA | B: Bresenham | M: Compare", 10, 55)
    draw_text("L: Line | G: Triangle", 10, 80)
    draw_text("T: Translate | R: Rotate | S: Scale", 10, 105)
    draw_text("C: Clear | Click points to draw", 10, 130)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
