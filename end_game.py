import pygame
import sys

def scorecard_screen(game_stats, background_image_path):
    pygame.init()

    # Window size
    WINDOW_WIDTH, WINDOW_HEIGHT = 1100, 600
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Scorecard")

    # Background image load and scaling here
    background_image = pygame.image.load("images/bg4.png").convert()
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # FONT
    title_font = pygame.font.Font(None, 72)
    table_font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 28)

    # Button
    main_menu_button = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 100, 140, 40)
    exit_button = pygame.Rect(WINDOW_WIDTH // 2 + 10, WINDOW_HEIGHT - 100, 140, 40)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if main_menu_button.collidepoint(mouse_x, mouse_y):
                    print("Return to Main Menu")  # backend integration PLACEHOLDER
                    running = False

                if exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        # background
        window.blit(background_image, (0, 0))

        # Draw winner
        winner_text = f"Winner: {game_stats['winner']}"
        winner_surface = title_font.render(winner_text, True, (200, 200, 200))
        winner_rect = winner_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
        window.blit(winner_surface, winner_rect)

        # Draw the stats table
        stats_headers = ["     ", "Player 1", "Player 2"]
        stats_data = [
            ["Hits", game_stats['player1_hits'], game_stats['player2_hits']],
            ["Misses", game_stats['player1_misses'], game_stats['player2_misses']],
            ["Accuracy (%)", f"{game_stats['player1_accuracy']:.2f}", f"{game_stats['player2_accuracy']:.2f}"],
            ["Turns Taken", game_stats['player1_turns'], game_stats['player2_turns']],
            ["Total Turns Taken", game_stats['turns'], " "]
        ]

        table_start_y = 150
        header_y = table_start_y
        row_height = 40

        # Draw text headers
        for i, header in enumerate(stats_headers):
            header_surface = table_font.render(header, True, (200, 200, 200))
            header_x = 50 + i * 300
            window.blit(header_surface, (header_x, header_y))

        # Draw table rows
        for row_index, row_data in enumerate(stats_data):
            for col_index, cell in enumerate(row_data):
                cell_surface = table_font.render(str(cell), True, (0, 0, 0))
                cell_x = 50 + col_index * 300
                cell_y = table_start_y + (row_index + 1) * row_height
                window.blit(cell_surface, (cell_x, cell_y))

        # Draw the button
        pygame.draw.rect(window, (0, 255, 0), main_menu_button)
        main_menu_text = button_font.render("Main Menu", True, (0, 0, 0))
        window.blit(main_menu_text, (main_menu_button.x + 20, main_menu_button.y + 10))

        pygame.draw.rect(window, (255, 0, 0), exit_button)
        exit_text = button_font.render("Exit", True, (0, 0, 0))
        window.blit(exit_text, (exit_button.x + 50, exit_button.y + 10))

        pygame.display.flip()

