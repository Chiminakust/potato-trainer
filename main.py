import pygame
import pygame.mouse as mouse
pygame.init()
font = pygame.font.SysFont("monospace", 18)
from random import randint
from time import time


class PotatoTrainer:

    def __init__(self):
        self.banner_h = 200
        self.banner_color = (0, 0, 0)
        self.banner_text_color = (0, 255, 0)
        self.targetzone_h = 1000
        self.target_color = (140, 40, 140)
        self.w = 1000
        self.h = self.targetzone_h + self.banner_h
        self.tw = 75
        self.th = 75

        # targets stuff
        self.max_targets = 10
        self.targets = [None] * self.max_targets
        self.tidx = 0 # target index
        self.screen = pygame.display.set_mode([self.w, self.h])
        self.target_origin = (0, 0)
        margin = 100
        self.target_spawn_zone_x = (margin + self.tw, self.w - self.tw - margin)
        self.target_spawn_zone_y = (margin + self.th, self.h - self.banner_h - self.th - margin)

        # custom event to add new targets at a regular time interval
        self.ADD_TARGET_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_TARGET_EVENT, 100)

        # punish player for being slow
        self.punish_time = 1.0
        self.last_click_time = time()

        # banner stuff (stats)
        self.last_frame_time = time()
        self.hits = 0
        self.misses = 0

        # mouse invisible, now in virtual mode
        mouse.set_visible(False)
        # grab mouse
        pygame.event.set_grab(True)

        # crosshair color, position and dimension
        tmp = 40 # length of crosshair bar
        self.crosshair_x = ((self.w - tmp) / 2 + 1, self.targetzone_h / 2, tmp, tmp / 10)
        self.crosshair_y = (self.w / 2, (self.targetzone_h - tmp) / 2 + 1, tmp / 10, tmp)
        self.crosshair_coord = (self.crosshair_y[0], self.crosshair_x[1])
        self.crosshair_color = (0, 0, 0)

    def get_num_targets(self):
        return sum(x is not None for x in self.targets)


    def add_target(self):
        N = self.get_num_targets()
        if N >= self.max_targets:
            return
        
        # find next free spot
        i = self.tidx
        for _ in range(self.max_targets):
            if self.targets[i] is None:
                self.tidx = i
                break
            else:
                i += 1
                if i >= self.max_targets:
                    i = 0

        x = randint(*self.target_spawn_zone_x)
        y = randint(*self.target_spawn_zone_y)
        x += self.target_origin[0]
        y += self.target_origin[1]
        self.targets[self.tidx] = (
            x,
            y,
            self.tw,
            self.th
        )


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
            return -1


    def handle_hit(self, tid):
        self.hits += 1
        # remove hit target
        self.targets[tid] = None


    def handle_miss(self):
        self.misses += 1
        # remove oldest (start at tidx) target which is not None
        i = 0 if self.tidx + 1 >= self.max_targets else self.tidx + 1
        for _ in range(self.max_targets):
            if self.targets[i]:
                self.targets[i] = None
                return
            else:
                i += 1
                if i >= self.max_targets:
                    i = 0


    def handle_click(self, pos):
        tid = self.target_hit(pos)
        if tid > -1:
            self.handle_hit(tid)
        else:
            self.handle_miss()
    

    def update_targets(self):
        mouse_move = (0, 0)
        prev_mouse_move = mouse_move
        mouse_move = mouse.get_rel()

        # adapt target's origin (for spawning new targets)
        self.target_origin = (self.target_origin[0] - mouse_move[0], self.target_origin[1] - mouse_move[1])

        # draw target spawn zone
        # pygame.draw.rect(self.screen, (0x7f, 0, 0x0),
        #                  (
        #                      self.target_spawn_zone_x[0] + self.target_origin[0],
        #                      self.target_spawn_zone_x[1] + self.target_origin[0],
        #                      self.target_spawn_zone_y[0] + self.target_origin[1],
        #                      self.target_spawn_zone_y[1] + self.target_origin[1],
        #                  )
        # )
        pygame.draw.rect(self.screen, (0x7f, 0, 0x0),
                         (
                             self.target_spawn_zone_x[0] + self.target_origin[0],
                             self.target_spawn_zone_y[0] + self.target_origin[1],
                             self.target_spawn_zone_x[1] - self.target_spawn_zone_x[0],
                             self.target_spawn_zone_y[1] - self.target_spawn_zone_y[0]
                         )
        )
        print(
            self.target_spawn_zone_x[0],
            self.target_spawn_zone_x[1],
            self.target_spawn_zone_y[0],
            self.target_spawn_zone_y[1]
        )

        # adapt target display to inverse of mouse mouvement (first person)
        for i, t in enumerate(self.targets):
            if t:
                self.targets[i] = (t[0] - mouse_move[0], t[1] - mouse_move[1], t[2], t[3])
                pygame.draw.rect(self.screen, self.target_color, self.targets[i])
        prev_mouse_move = mouse_move


    def update_banner(self):
        # define banner origin
        Ox, Oy = 5, self.targetzone_h + 5

        # draw banner
        pygame.draw.rect(self.screen, self.banner_color, (0, self.targetzone_h, self.w, self.banner_h))

        # draw fps counter
        current_frame_time = time()
        fps = int(1 / (current_frame_time - self.last_frame_time))
        self.last_frame_time = current_frame_time
        fps_txt = font.render(f"{fps} fps", 1, self.banner_text_color)
        self.screen.blit(fps_txt, (Ox, Oy))

        # draw score counter
        try:
            accuracy = 100.0 * self.hits / (self.hits + self.misses)
        except ZeroDivisionError:
            accuracy = 100.0
        score_txt = font.render(f"Hit:Miss = {self.hits}:{self.misses} ({accuracy}%)", 1, self.banner_text_color)
        self.screen.blit(score_txt, (Ox, Oy + 20))


    def check_punish(self):
        c = time()
        if c - self.last_click_time >= self.punish_time:
            self.last_click_time = c
            self.handle_miss()


    def draw_crosshair(self):
        pygame.draw.rect(self.screen, self.crosshair_color, self.crosshair_x)
        pygame.draw.rect(self.screen, self.crosshair_color, self.crosshair_y)
        

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.ADD_TARGET_EVENT:
                    self.add_target()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.last_click_time = time()
                    self.handle_click(self.crosshair_coord)
                    
            self.screen.fill((240, 240, 240))

            self.check_punish()

            self.update_targets()
            self.update_banner()
            self.draw_crosshair()

            # display drawings
            pygame.display.flip()

        pygame.quit()
        

if __name__ == '__main__':
    game = PotatoTrainer()
    game.run()


