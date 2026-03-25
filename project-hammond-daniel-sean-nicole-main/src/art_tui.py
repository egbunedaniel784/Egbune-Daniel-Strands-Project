import sys
import random
from ui import ArtTUIBase
import click

class ArtTUIWrappers(ArtTUIBase):
    COLORS = [
        "\033[41m",
        "\033[42m",
        "\033[43m"
    ]
    def __init__(self, num_wrappers: int, interior_width: int, height: int):
        self.num_wrappers = num_wrappers
        self.interior_width = interior_width
        self.height = height

    def print_top_edge(self) -> None:
        for layer in range(self.num_wrappers):
            width = self.interior_width + 2 * (self.num_wrappers - layer)
            color = self.COLORS[layer % len(self.COLORS)]
            print(color + " " * width)

    def print_bottom_edge(self) -> None:
        for layer in range(self.num_wrappers - 1, -1, -1):
            width = self.interior_width + 2 * (self.num_wrappers - layer)
            color = self.COLORS[layer % len(self.COLORS)]
            print(color + " " * width)

    def print_left_bar(self) -> None:
        for layer in range(self.num_wrappers):
            color = self.COLORS[layer % len(self.COLORS)]
            print(color + " ", end="")
        print(" ", end="")

    def print_right_bar(self) -> None:
        print(" ", end="")
        for layer in range(self.num_wrappers - 1, -1, -1):
            color = self.COLORS[layer % len(self.COLORS)]
            print(color + " ", end="")

    def render(self) -> None:
        self.print_top_edge()
        for i in range(self.height):
            self.print_left_bar()
            print(" " * self.interior_width, end="")
            self.print_right_bar()
            print()
        self.print_bottom_edge()

class ArtTUIPolkaDots(ArtTUIBase):
    """
    Implementation of ArtTUIBase that creates a frame of polka dots.
    The frame surrounds an interior of specified width and height.
    """
    def __init__(self, frame_width: int, interior_width: int):
        self.frame_width = frame_width
        self.interior_width = interior_width
        self.dots = ['o', '*']
    
    def print_top_edge(self) -> None:
        for _ in range(self.frame_width):
            total_width = self.interior_width + 2 * (self.frame_width + 1)
            row = ''
            for i in range(total_width):
                if random.random() < 0.3:
                    row += random.choice(self.dots)
                else:
                    row += ' '
            print(row)
    
    def print_bottom_edge(self) -> None:
        self.print_top_edge()
    
    def print_left_bar(self) -> None:
        bar = ''
        for _ in range(self.frame_width):
            if random.random() < 0.3:
                bar += random.choice(self.dots)
            else:
                bar += ' '
        print(f"{bar} ", end="")
    
    def print_right_bar(self) -> None:
        bar = ''
        for _ in range(self.frame_width):
            if random.random() < 0.3:
                bar += random.choice(self.dots)
            else:
                bar += ' '
        print(f" {bar}")


class TUI:
    def __init__(self, art: ArtTUIBase, width: int, height: int):
        self._art = art
        self._width = width
        self._height = height
        self.print_display()
    
    def print_display(self) -> None:
        self._art.print_top_edge()
        for _ in range(self._height):
            self._art.print_left_bar()
            print(self._width * " ", end="")
            self._art.print_right_bar()
        self._art.print_bottom_edge()

@click.command()
@click.option('-a', '--art', 'frame_type', required=True,
              type=click.Choice(['cat0', 'cat1', 'cat4', 'wrappers', 'polkadots'], case_sensitive=False),
              help="Specify the kind of frame to display.")
@click.option('-f', '--frame', 'frame_width', type=int,
              help="Specify the frame width (or number of wrappers for 'wrappers').")
@click.option('-w', '--width', 'interior_width', type=int,
              help="Specify the interior width (columns).")
@click.option('-h', '--height', 'interior_height', type=int,
              help="Specify the interior height (rows).")
def main(frame_type, frame_width, interior_width, interior_height):
    if frame_type.lower() == "cat4":
        click.echo("cat4 frame is not supported in TUI.")
        return

    if frame_type.lower() in ["cat0", "wrappers"]:
        if frame_width is None or interior_width is None or interior_height is None:
            click.echo("Missing parameters: wrappers require --frame, --width, and --height.")
            return
        art = ArtTUIWrappers(frame_width, interior_width, interior_height)
        art.render()

    elif frame_type.lower() in ["cat1", "polkadots"]:
        if frame_width is None or interior_width is None or interior_height is None:
            click.echo("Missing parameters: polkadots require --frame, --width, and --height.")
            return
        art = ArtTUIPolkaDots(frame_width, interior_width)
        TUI(art, interior_width, interior_height)

    else:
        click.echo(f"Unsupported art type: {frame_type}")

if __name__ == "__main__":
    main()

