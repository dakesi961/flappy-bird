import pygame, sys, random

def draw_fl():
    scr_cnvs.blit(fl_srf, (fl_x,900))
    scr_cnvs.blit(fl_srf, (fl_x+576,900))

def create_pipe():
    random_pp = random.choice(pipe_h)
    b_pipe = pipe_srf.get_rect(midtop = (700,random_pp))
    t_pipe = pipe_srf.get_rect(midbottom = (700,random_pp - 300))
    return b_pipe,t_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            scr_cnvs.blit(pipe_srf,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_srf, False, True)
            scr_cnvs.blit(flip_pipe, pipe)

def chck_collis(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    
    return True

def rotate_bird(bird):
    new_b = pygame.transform.rotozoom(bird, -bird_mvm * 3, 1)
    return new_b
            
def bird_anim():
    new_bird = bird_frm[bird_idx]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_srf = font.render(str(int(score)), True, (255,255,255))
        score_rect = score_srf.get_rect(center=(288,100))
        scr_cnvs.blit(score_srf,score_rect)
    if game_state == 'game_over':
        score_srf = font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_srf.get_rect(center=(288,250))
        scr_cnvs.blit(score_srf,score_rect)

        high_score_srf = font.render(f'High score: {int(high_score)}', True, (255,255,255))
        high_score_rect = score_srf.get_rect(center=(288,800))
        scr_cnvs.blit(high_score_srf,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
scr_cnvs = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
font = pygame.font.Font('fnt.ttf',36)

g = 0.25
bird_mvm = 0
game_active = True
score = 0
high_score = 0

bg_srf = pygame.image.load('assets/sprites/background-day.png').convert()
bg_srf = pygame.transform.scale2x(bg_srf)

bg_nght = pygame.image.load('assets/sprites/background-night.png').convert()
bg_nght = pygame.transform.scale2x(bg_nght)

fl_srf = pygame.image.load('assets/sprites/base.png').convert()
fl_srf = pygame.transform.scale2x(fl_srf)
fl_x = 0

bird_dw = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha())
bird_frm = [bird_dw, bird_mid, bird_up]
bird_idx = 2
bird_srf = bird_frm[bird_idx]
bird_rect = bird_srf.get_rect(center = (100, 512))

BIRDFLIP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLIP, 200)

pipe_srf = pygame.image.load('assets/sprites/pipe-green.png').convert()
pipe_srf = pygame.transform.scale2x(pipe_srf)
pipe_lst = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_h = [400,600,800]

game_over_srf = pygame.transform.scale2x(pygame.image.load('assets/sprites/message.png').convert_alpha())
game_over_rect = game_over_srf.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
death_sound = pygame.mixer.Sound('assets/audio/hit.wav')
score_sound = pygame.mixer.Sound('assets/audio/point.wav')
ssc = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                bird_mvm = 0
                bird_mvm -= 12
                flap_sound.play()

            if event.key == pygame.K_UP and game_active == False:
                game_active = True
                pipe_lst.clear()
                bird_rect.center = (100,512)
                bird_mvm = 0
                score = 0


        if event.type == SPAWNPIPE:
            pipe_lst.extend(create_pipe())


        if event.type == BIRDFLIP:
            if bird_idx < 2:
                bird_idx += 1    
            else:
                bird_idx = 0
            
            bird_srf, bird_rect = bird_anim()
        
    if game_active:
        scr_cnvs.blit(bg_srf, (0,0))
        bird_mvm += g
        rotated_bird = rotate_bird(bird_srf)
        bird_rect.centery += bird_mvm
        scr_cnvs.blit(rotated_bird, bird_rect)
        game_active = chck_collis(pipe_lst)

        pipe_lst = move_pipes(pipe_lst)
        draw_pipes(pipe_lst)

        score += 0.01

        score_display('main_game')

        """
        if score >= 3:
            scr_cnvs.blit(bg_nght, (0,0))
            bird_mvm += g
            rotated_bird = rotate_bird(bird_srf)
            bird_rect.centery += bird_mvm
            scr_cnvs.blit(rotated_bird, bird_rect)
            game_active = chck_collis(pipe_lst)

            pipe_lst = move_pipes(pipe_lst)
            draw_pipes(pipe_lst) 
        """

        ssc -= 1
        if ssc <= 0:
            score_sound.play()
            ssc = 100
    else:
        scr_cnvs.blit(game_over_srf,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        

    fl_x -= 1
    draw_fl()
    if fl_x <= -576:
        fl_x = 0
    scr_cnvs.blit(fl_srf, (fl_x,900))

    pygame.display.update()
    clock.tick(120)