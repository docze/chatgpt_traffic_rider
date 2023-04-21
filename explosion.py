import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.frames = []
        self.load_frames()
        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()

    def load_frames(self):
        # Load the explosion image as a Surface object
        image = pygame.image.load("assets/explosion.png").convert_alpha()
        # Calculate the number of frames in the image (assuming each frame is 32px wide)
        num_frames = image.get_width() // 32
        # Extract each frame of the animation as a separate Surface object
        for i in range(num_frames):
            frame = image.subsurface((i*32, 0, 32, 32))
            self.frames.append(frame)

    def update(self):
        # Check if it's time to update the animation
        now = pygame.time.get_ticks()
        elapsed = now - self.last_update
        if elapsed > self.animation_speed * 1000:
            # Update the current frame and reset the timer
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                # If we've reached the end of the animation, destroy the explosion object
                self.kill()
            else:
                self.last_update = now

    def draw(self, screen):
        # Draw the current frame of the animation
        self.image = self.frames[self.current_frame]
        screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def kill(self):
        # Remove the explosion object from the game
        # (This could be done using a sprite group or some other mechanism)
        pass
