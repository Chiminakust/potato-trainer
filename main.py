import pygame
pygame.init()
from random import randint


class PotatoTrainer:

    def __init__(self):
        self.w = 1000
        self.h = 1200
        self.tw = 75
        self.th = 75
        self.max_targets = 10
        self.targets = [None] * self.max_targets
        self.tidx = 0 # target index
        self.screen = pygame.display.set_mode([self.w, self.h])

        self.ADD_TARGET_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_TARGET_EVENT, 500)


    def get_num_targets(self):
        return sum(x is not None for x in self.targets)


    def add_target(self):
        if self.get_num_targets() >= self.max_targets:
            return

        self.targets[self.tidx] = (randint(0, self.w - self.tw), randint(0, self.h - self.th), self.tw, self.th)

        self.tidx += 1
        if self.tidx >= self.max_targets:
            self.tidx = 0


    def detect_hit(self, pos, rect):
        """Check if pos is inside rect.

            Args:
                pos: (x, y) integer tuple of the coordinates of the click
                rect: (left, top, width, height) integer tuple of the rectangle
        """
        x, y = pos
        x1, y1, w, h = rect
        return (x1 <= x <= x1 + w) and (y1 <= y <= y1 + h)


    def target_hit(self, pos):
        """Return the index of the target that was hit, False otherwise."""

        # iterate over targets
        for i, t in enumerate(self.targets):
            if t is None:
                continue
            # check for collision
            if self.detect_hit(pos, t):
                return i
        else:
            return False


    def handle_click(self, pos):
        tid = self.target_hit(pos)
        if tid:
            # remove target which was hit
            self.targets[tid] = None
        else:
            # remove oldest (start at tidx) target which is not None
            i = self.tidx
            for _ in range(self.max_targets):
                if self.targets[i]:
                    self.targets[i] = None
                    return
                else:
                    i += 1
                    if i >= self.max_targets:
                        i = 0
    

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.ADD_TARGET_EVENT:
                    self.add_target()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                    
            self.screen.fill((240, 240, 240))
            
            # draw targets
            for t in self.targets:
                if t:
                    pygame.draw.rect(self.screen, (40, 40, 40), t)

            
            # display drawings
            pygame.display.flip()

        pygame.quit()
        

if __name__ == '__main__':
    game = PotatoTrainer()
    game.run()


