import pygame
from world_config import DisplayMode, ascii_color_map
# TODO: Make a Map Rendering Function file
# Use this to handle all aspects of the world gen
# as the complexity of this project grows.

def draw_tilemap(window, world_map, tile_size, font, display_mode, generate_image=False, filename=None):
    for y, row in enumerate(world_map):
        for x, tile in enumerate(row):
            
            color = ascii_color_map.get(tile.raw_symbol, (255, 255, 255)) # set color
            
            image_surface = pygame.Surface((len(world_map) * tile_size, len(world_map) * tile_size))
            
            if display_mode == DisplayMode.ASCII_MODE:
                text_surface = font.render(tile.raw_symbol, True, color)
                window.blit(text_surface, (x * tile_size, y * tile_size))
            elif display_mode == DisplayMode.PIXEL_MODE:
                # Render tile as a solid colored pixel
                pygame.draw.rect(window, color, (x * tile_size, y * tile_size, tile_size, tile_size))
            else:
                print(f"Error: Invalid map render mode provided. Receieved display_mode = {display_mode}")
                return
            
            if generate_image:
                pygame.image.save(image_surface, filename)
                generate_image = False

    
    