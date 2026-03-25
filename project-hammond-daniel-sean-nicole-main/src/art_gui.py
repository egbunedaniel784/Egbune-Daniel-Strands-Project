from ui import ArtGUIBase
import pygame
import sys
import math
import click
class ArtGUI9Slice(ArtGUIBase):
    def __init__(self, frame_width: int):
        self.frame_width = frame_width

    def draw_background(self, surface: pygame.Surface) -> None:
        width = surface.get_width()
        height = surface.get_height()
        clrs = [
            (121, 110, 212),
            (157, 207, 177),
            (199, 100, 115),
            (255, 0, 0),
            (128, 190, 108),
            (0, 255, 255),
            (0, 0, 255),
            (255, 230, 0),
            (247, 201, 198)   
        ]
        frame_size = self.frame_width
        pygame.draw.rect(surface, clrs[0], (0, 0, frame_size, frame_size))
        pygame.draw.rect(surface, clrs[1], (frame_size, 0, width - 2 * frame_size, frame_size))
        pygame.draw.rect(surface, clrs[2], (width - frame_size, 0, frame_size, frame_size))
        pygame.draw.rect(surface, clrs[3], (0, frame_size, frame_size, height - 2 * frame_size))
        pygame.draw.rect(surface, clrs[4], (frame_size, frame_size, width - 2 * frame_size, height - 2 * frame_size))
        pygame.draw.rect(surface, clrs[5], (width - frame_size, frame_size, frame_size, height - 2 * frame_size))
        pygame.draw.rect(surface, clrs[6], (0, height - frame_size, frame_size, frame_size))
        pygame.draw.rect(surface, clrs[7], (frame_size, height - frame_size, width - 2 * frame_size, frame_size))
        pygame.draw.rect(surface, clrs[8], (width - frame_size, height - frame_size, frame_size, frame_size))

class ArtGUIPlaid(ArtGUIBase):
    def __init__(self, frame_width: int):
        self.frame_width = frame_width

    def draw_background(self, surface: pygame.Surface) -> None:
        width = surface.get_width()
        height = surface.get_height()
        background_color = (220, 235, 250)
        stripes1 = [
            (65, 105, 225, 180),
            (100, 149, 237, 180),
            (30, 144, 255, 180)
        ]
        stripes2 = [
            (176, 224, 230, 150),                           
            (135, 206, 250, 150),                             
            (173, 216, 230, 150)                             
        ]
        surface.fill(background_color)
        stripe_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        stripe_surface.set_alpha(255)
        stripes1_width = max(self.frame_width // 2, 10)
        stripes2_width = max(self.frame_width // 4, 5)
        stripes1_count = max(5, width // (stripes1_width * 4))
        stripes2_count = max(6, height // (stripes2_width * 4))
        for i in range(stripes1_count):
            stripe_y = i * (height / stripes1_count)
            color = stripes1[i % len(stripes1)]
            pygame.draw.rect(stripe_surface, color, 
                            (0, stripe_y, width, stripes1_width))
        for i in range(stripes2_count):
            stripe_x = i * (width / stripes2_count)
            color = stripes2[i % len(stripes2)]
            pygame.draw.rect(stripe_surface, color, 
                            (stripe_x, 0, stripes2_width, height))
        surface.blit(stripe_surface, (0,0))

class ArtGUIHoneycomb(ArtGUIBase):
    def __init__(self, frame_width: int):
        self.frame_width = frame_width
        
    def draw_background(self, surface: pygame.Surface) -> None:
        width = surface.get_width()
        height = surface.get_height()
        background_color = (250, 240, 190)
        honeycomb_colors = [
            (255, 215, 0),
            (218, 165, 32),
            (184, 134, 11),
            (210, 180, 140)
        ]
        surface.fill(background_color)
        hex_size = max(self.frame_width, 15)
        h_spacing = hex_size * 1.75
        v_spacing = hex_size * 1.5
        cols = int(width / h_spacing) + 2
        rows = int(height / v_spacing) + 2
        for row in range(rows):
            for col in range(cols):
                offset = h_spacing / 2 if row % 2 else 0
                x = col * h_spacing + offset
                y = row * v_spacing
                if x + hex_size < 0 or x - hex_size > width or y + hex_size < 0 or y - hex_size > height:
                    continue
                color_idx = (row + col) % len(honeycomb_colors)
                color = honeycomb_colors[color_idx]
                vertices = []
                for i in range(6):
                    angle = math.pi / 3 * i
                    vx = x + hex_size * math.cos(angle)
                    vy = y + hex_size * math.sin(angle)
                    vertices.append((vx, vy))
                pygame.draw.polygon(surface, color, vertices)
                pygame.draw.polygon(surface, (0, 0, 0), vertices, 1)

class ArtGUIBinaryTree(ArtGUIBase):
    def __init__(self, frame_width: int):
        self.frame_width = frame_width
        
    def draw_background(self, surface: pygame.Surface) -> None:
        width = surface.get_width()
        height = surface.get_height()
        background_color = (56, 190, 252)
        node_color = (84, 245, 66)
        edge_color = (117, 55, 30)
        surface.fill(background_color)      
        node_radius = min(width, height) / 20
        level_height = (height - 2 * self.frame_width) / 5
        nodes = {}
        root_x = width / 2
        root_y = self.frame_width + level_height / 2
        nodes[1] = (root_x, root_y)
        nodes[2] = (width / 4, root_y + level_height)
        nodes[3] = (3 * width / 4, root_y + level_height)
        nodes[4] = (width / 8, root_y + 2 * level_height)
        nodes[5] = (3 * width / 8, root_y + 2 * level_height)
        nodes[6] = (5 * width / 8, root_y + 2 * level_height)
        nodes[7] = (7 * width / 8, root_y + 2 * level_height)
        nodes[8] = (width / 16, root_y + 3 * level_height)
        nodes[9] = (3 * width / 16, root_y + 3 * level_height)
        nodes[10] = (5 * width / 16, root_y + 3 * level_height)
        nodes[11] = (7 * width / 16, root_y + 3 * level_height)
        nodes[12] = (9 * width / 16, root_y + 3 * level_height)
        nodes[13] = (11 * width / 16, root_y + 3 * level_height)
        nodes[14] = (13 * width / 16, root_y + 3 * level_height)
        nodes[15] = (15 * width / 16, root_y + 3 * level_height)
        for parent in range(1, 8):
            left_child = parent * 2
            right_child = parent * 2 + 1
            pygame.draw.line(surface, edge_color, nodes[parent], nodes[left_child], 3)
            pygame.draw.line(surface, edge_color, nodes[parent], nodes[right_child], 3)
        for node_id, (x, y) in nodes.items():
            pygame.draw.circle(surface, node_color, (int(x), int(y)), int(node_radius))
            pygame.draw.circle(surface, edge_color, (int(x), int(y)), int(node_radius), 2)

@click.command()
@click.option('-a', '--art', 'category', required=True, type=click.Choice([
    '9slices', 'cat0', 'cat1', 'cat2', 'cat3', 'cat4', 'trees', 'graphs'
], case_sensitive=False), help="Frame type to display.")
@click.option('-f', '--frame', 'frame_width', type=int, help="Frame width in pixels.")
@click.option('-w', '--width', 'total_width', type=int, help="Total width in pixels.")
@click.option('-h', '--height', 'total_height', type=int, help="Total height in pixels.")
def main(category, frame_width, total_width, total_height):

    category = category.lower()
    frame_classes = {
        '9slices': ArtGUI9Slice,
        'cat0': ArtGUI9Slice,
        'cat2': ArtGUIPlaid,
        'cat3': ArtGUIHoneycomb,
        'cat4': ArtGUIBinaryTree,
        'trees': ArtGUIBinaryTree,
    }

    if category not in frame_classes:
        click.echo(f"Category '{category}' is not supported.")
        sys.exit(1)

    if category in ['cat4', 'trees']:
        frame_width = 30
        total_width = 720
        total_height = 560
    else:
        if frame_width is None or total_width is None or total_height is None:
            click.echo("Frame width, total width, and height must be provided for this category.")
            sys.exit(1)

    pygame.init()
    surface = pygame.display.set_mode((total_width, total_height))
    clock = pygame.time.Clock()
    art = frame_classes[category](frame_width)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        art.draw_background(surface)
        pygame.display.flip()
        clock.tick(24)

if __name__ == "__main__":
    main()

