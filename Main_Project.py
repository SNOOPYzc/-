import pygame,sys,random
from pygame.locals  import *

pygame.init()

#Set button
button_width = 150
button_height = 40

#Set Screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 730

#color
white = (255, 255, 255)
gray = (150, 150, 150) 
green = (0, 255, 0)
red =  (255, 0, 0)
magen = (255, 0, 255)
black = (0, 0, 0)

pygame.display.set_caption("Wolf")
font = pygame.font.Font('Font/HeartThin.ttf',20)
bg = pygame.image.load('BG/Pixel05.png')
bg_rect = bg.get_rect()
pygame.mixer.music.load('music/Lukrembo - Marshmallow.mp3')
pygame.mixer.music.play(0)
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))

#Create a Button Function

def draw_text(text, x, y, font_size=20, color=black):
    font = pygame.font.Font('Font/HeartThin.ttf',font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(screen, x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

class MENU():
    def main_menu(screen):
        global start_button_rect, quit_button_rect
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        main = Main()
                        main.run(screen)
                    elif quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            screen.blit(bg, (0, 0))

            start_button_rect = pygame.Rect(540, 200, button_width, button_height)
            draw_button(screen, start_button_rect.x, start_button_rect.y, button_width, button_height, "Start", gray)

            quit_button_rect = pygame.Rect(540, 400, button_width, button_height)
            draw_button(screen, quit_button_rect.x, quit_button_rect.y, button_width, button_height, "Quit", gray)

            pygame.display.flip()

    def over_menu(screen):
        global start_button_rect, quit_button_rect
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if again_button.collidepoint(mouse_pos):
                        MENU.main_menu(screen)
                    elif quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
        
            again_button = pygame.Rect(540, 200, button_width, button_height)
            draw_button(screen, again_button.x, again_button.y, button_width, button_height, "play again", gray)

            quit_button_rect = pygame.Rect(540, 400, button_width, button_height)
            draw_button(screen, quit_button_rect.x, quit_button_rect.y, button_width, button_height, "Quit", gray)
    
            pygame.display.flip()

class Wolf(pygame.sprite.Sprite):

    ACTIONS = ['Idle','Run']

    def __init__(self,action = 'RUN',x = 10, y = 560, frame = 0):
        super().__init__()

        self.action = action
        self.x = x  #
        self.y = y  #
        self.frame = frame
        self.deltatime = 0
        self.image = None
        self.rect = pygame.Rect(self.x,self.y,0,0)

        self.rect.topleft = (x, y)

    def left(self):
        self.x -= 10

    def right(self):
        self.x += 10
    

    def update(self, deltatime):
        self.deltatime += deltatime
        if self.deltatime >= 30:
            self.deltatime -= 30
            self.frame = (self.frame+1)%10
    
    
    def blit(self,screen):
        self.image = pygame.image.load(f'Wolf/Run/{self.action}__{self.frame:03d}.png')
        self.image = pygame.transform.scale(self.image,(self.image.get_width()//2 , self.image.get_height() //2))
        self.update_rect()  # เรียกใช้เมธอดเพื่อปรับค่า rect
        screen.blit(self.image,self.rect)
    
    def update_rect(self):
        # ปรับค่า rect เพื่อให้สอดคล้องกับขนาดของภาพ
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.rect.x = self.x  # ปรับตำแหน่ง x ใหม่
        self.rect.y = self.y  # ปรับตำแหน่ง y ใหม่

class Star(pygame.sprite.Sprite):
    def __init__(self, x = 1200, y = 700):
        super().__init__()
        self.image = pygame.image.load('Object/Star.png')
        self.image = pygame.transform.scale(self.image,(self.image.get_width()//5 , self.image.get_height() //5))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.speed = 10

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

    def update_rect(self):
        # ปรับค่า hit box ให้สอดคล้องกับขนาดภาพ
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

class Main:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Wolf jump")
        self.score = 0
        self.max_score = self.load_max_score()  # โหลดคะแนนสูงสุดจากไฟล์
        self.star_spawn_count = {500: 0, 700: 0}  # เก็บจำนวนครั้งที่ดาวเกิดที่แต่ละ y
    
    def load_max_score(self):
        try:
            with open('max_score.txt', 'r') as file:
                max_score = int(file.read())
        except FileNotFoundError:
            max_score = 0
        return max_score
    
    def save_max_score(self, max_score):
        with open('max_score.txt', 'w') as file:
            file.write(str(max_score))
    
    
    
    def run(self,screen):
        
        Player = Wolf()
        Player_sprites = pygame.sprite.Group()
        Player_sprites.add(Player)

        self.all_sprites = pygame.sprite.Group()  # สร้าง Group สำหรับรวม sprite ทั้งหมด
        self.stars = pygame.sprite.Group() 
        star = Star()  
        self.all_sprites.add(star)
        self.stars.add(star)
        
        clock = pygame.time.Clock()

        
        game_over = False
        jumping = False
        jump_count = 10  # จำนวนเครื่องหมายจำนวนนับที่ใช้ในการกระโดด

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_max_score(self.max_score)  # บันทึกคะแนนสูงสุดเมื่อปิดโปรแกรม
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        Player.left()
                    elif event.key == pygame.K_d:
                        Player.right()
                    elif event.key == pygame.K_SPACE and not jumping:  # กระโดดเมื่อกด SPACE และไม่ได้อยู่ในกระบวนการกระโดดอยู่แล้ว
                        jumping = True
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                Player.left()
            if keys[pygame.K_d]:
                Player.right()

            self.display_surface.blit(bg, (0, 0))

            self.all_sprites.update()  # อัพเดททุก sprite ใน Group
            self.all_sprites.draw(self.display_surface)  # วาด sprite ทุกตัวใน Group ลงบนหน้าจอ

            text = f'Score: {self.score}        Max Score:{self.max_score}'# แสดงคะแนนและคะแนนสูงสุดบนหน้าจอ
            draw_text(text,SCREEN_WIDTH - 200,50)# แสดงคะแนนและคะแนนสูงสุดบนหน้าจอ

            text = f'{clock.get_fps():.2f}FPS'
            draw_text(text, 50, 50)  # แสดง FPS บนหน้าจอ
            
            deltatime = clock.tick(60)
            Player.update(deltatime)

            self.score += 1
            # ถ้าคะแนนปกติมากกว่าคะแนนสูงสุด ให้อัปเดตคะแนนสูงสุด
            if self.score > self.max_score:
                self.max_score = self.score

            if jumping:
                if jump_count >= -10:
                    neg = 1
                    if jump_count < 0:
                        neg = -1
                    Player.y -= (jump_count ** 2) * 0.5 * neg  # ปรับตำแหน่งตามการกระโดด
                    jump_count -= 1
                else:
                    jumping = False
                    jump_count = 10
            

            Player.blit(self.display_surface)  # วาดตัวละครหมาลงบนหน้าจอ
            
            if pygame.sprite.spritecollide(Player,self.stars,False):
                game_over = True
                MENU.over_menu(screen)

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)

            self.save_max_score(self.max_score)  # บันทึกคะแนนสูงสุดเมื่อเกมเสร็จสิ้น
            
            # ให้สร้างดาวใหม่ถ้าดาวเลยขอบจอ
            for star in self.stars:
                if star.rect.right <= 0:
                    # สุ่มเลือกค่า y_pos โดยไม่ซ้ำกันเกิน 3 ครั้ง
                    y_pos = self.random_y_pos()
                    star.rect.bottomleft = (SCREEN_WIDTH, y_pos)
                    break

    def random_y_pos(self):
        # สุ่มเลือกค่า y_pos โดยไม่ซ้ำกันเกิน 3 ครั้ง
        y_pos = random.choice([500, 700])
        while self.star_spawn_count[y_pos] >= 3:
            y_pos = random.choice([500, 700])
        self.star_spawn_count[y_pos] += 1
        return y_pos
        
if __name__ == '__main__':
    MENU.main_menu(screen)