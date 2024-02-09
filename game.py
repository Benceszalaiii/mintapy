import pygame
import random
from settings import WIDTH, BG_COLOR, FONT_COLOR, HEIGHT, FPS



class Samurai(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        samurai_fw_1: pygame.Surface = pygame.image.load('Samurai_Char/Run__001.png').convert_alpha()
        samurai_fw_2: pygame.Surface = pygame.image.load('Samurai_Char/Run__002.png').convert_alpha()
        samurai_fw_3: pygame.Surface = pygame.image.load('Samurai_Char/Run__003.png').convert_alpha()
        self.samurai_fw: list[pygame.Surface] = [samurai_fw_1, samurai_fw_2, samurai_fw_3]
        samurai_bw_1: pygame.Surface = pygame.image.load('Samurai_Char/Run__B__001.png').convert_alpha()
        samurai_bw_2: pygame.Surface = pygame.image.load('Samurai_Char/Run__B__002.png').convert_alpha()
        samurai_bw_3: pygame.Surface = pygame.image.load('Samurai_Char/Run__B__003.png').convert_alpha()
        self.samurai_bw: list[pygame.Surface] = [samurai_bw_1, samurai_bw_2, samurai_bw_3]
        samurai_attack_1: pygame.Surface = pygame.image.load('Samurai_Char/Attack__001.png').convert_alpha()
        samurai_attack_2: pygame.Surface = pygame.image.load('Samurai_Char/Attack_003.png').convert_alpha()
        samurai_attack_3: pygame.Surface = pygame.image.load('Samurai_Char/Attack__005.png').convert_alpha()
        self.samurai_attack: list[pygame.Surface] = [samurai_attack_1, samurai_attack_2, samurai_attack_3]
        self.attack_mode: bool = False
        self.samurai_index: float = 0
        self.samurai_forward: bool = True
        self.image = self.samurai_fw[self.samurai_index]
        self.rect: pygame.Rect = self.image.get_rect(midbottom=(WIDTH/2, HEIGHT-149))
        self.speed: int = 5
        self.on_ground: bool = True
        self.gravity: int = 1
        self.jump_speed: int = -16
        self.dy: int = 0

    def samurai_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.attack_mode: bool = True
            self.attack_animation()
        else:
            self.attack_mode: bool = False
            self.image = pygame.image.load('Samurai_Char/Idle__001.png')
            rect_center = self.rect.center
            self.rect = self.image.get_rect(center=rect_center)

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.x_movement(self.speed)
            self.samurai_forward: bool = True
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.x_movement(-self.speed)
            self.samurai_forward: bool = False
        if keys[pygame.K_UP] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.dy += self.gravity
        self.rect.y += self.dy

    def jump(self):
        self.on_ground: bool = False
        self.dy = self.jump_speed

    def y_movement_collision(self):
        for pf_rect in platform_rects:
            if self.rect.colliderect(pf_rect):
                self.rect.bottom = pf_rect.top
                self.dy = 0
                self.on_ground = True

    def x_movement(self, dx):
        self.rect.x += dx
        self.x_movement_animation()

    def x_movement_animation(self):
        if self.samurai_index < len(self.samurai_fw) - 1:
            self.samurai_index += 0.2
        else:
            self.samurai_index = 0

        if self.samurai_forward:
            self.image = self.samurai_fw[int(self.samurai_index)]
        else:
            self.image = self.samurai_bw[int(self.samurai_index)]

    def attack_animation(self):
        if self.samurai_index < len(self.samurai_fw) - 1:
            self.samurai_index += 0.2
        else:
            self.samurai_index = 0
        self.image = self.samurai_attack[int(self.samurai_index)]

    def update(self):
        self.samurai_input()
        self.apply_gravity()
        self.y_movement_collision()


class Fruit(pygame.sprite.Sprite):
    def __init__(self, fruit_type: str):
        super().__init__()
        if fruit_type == 'pear':
            self.image = pygame.image.load('craftpix-net-772742-free-fruit-vector-icon-pack-for-rpg/PNG/shadow/24.png').convert_alpha()
            
            
        elif fruit_type == 'banana':
            self.image = pygame.image.load('craftpix-net-772742-free-fruit-vector-icon-pack-for-rpg/PNG/shadow/44.png').convert_alpha()
            
            
        else:
            self.image = pygame.image.load('craftpix-net-772742-free-fruit-vector-icon-pack-for-rpg/PNG/shadow/2.png').convert_alpha()
            
            
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH-20), -20))

    def destroy(self):
        if self.rect.top > HEIGHT:
            self.kill()

    def update(self):
        self.rect.y += 5
        self.destroy()


def collision_sprite():
    if samurai.sprite.attack_mode:
        if pygame.sprite.spritecollide(samurai.sprite, fruit_group, True):
            return True
    else:
        return False


def display_score():
    score_surf = game_font.render('score: ' + str(score), True, FONT_COLOR)
    score_rect = score_surf.get_rect(topleft=(10, 10))
    screen.blit(score_surf, score_rect)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('mintapy')
clock = pygame.time.Clock()

platform_surf = pygame.image.load('surface.png').convert_alpha()
platform_rects = [platform_surf.get_rect(midtop=(WIDTH/2, HEIGHT-150)),
                    platform_surf.get_rect(midtop=(WIDTH+250, HEIGHT-200))]

samurai = pygame.sprite.GroupSingle()
samurai.add(Samurai())

fruit_group = pygame.sprite.Group()

fruit_timer: int = pygame.USEREVENT + 1
pygame.time.set_timer(fruit_timer, 1000)

score: int = 0
game_font = pygame.font.SysFont('arial', 30, bold=True)

running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == fruit_timer:
            fruit_group.add(Fruit(random.choice(['pear', 'banana', 'strawberry'])))

    screen.fill(BG_COLOR)
    for platform_rect in platform_rects:
        screen.blit(platform_surf, platform_rect)

    samurai.draw(screen)
    samurai.update()
    pygame.draw.rect(screen, 'gray', samurai.sprite.rect, 2)

    fruit_group.draw(screen)
    fruit_group.update()

    if collision_sprite():
        score += 1
    display_score()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()