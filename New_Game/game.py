import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
STONE_INTERVAL = 30
GAMR_OVER_DISPLAY_TIME = 60
START_SCENE = "start"
PLAY_SCENE = "play"

class Stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 1
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Wannn | Sion")
        pyxel.mouse(True)
        
        # Pastikan file resource ada, atau tangani dengan try-except
        pyxel.load("my_resource.pyxres")
        pyxel.playm(0, loop=True)
        self.current_scene = START_SCENE
        pyxel.run(self.update, self.draw)

    def reset_play_scene(self):
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5  # Simpan posisi Y player
        
        # Inisialisasi stones list
        self.stones = []
        self.is_collision = False
        self.game_over_display_timer = GAMR_OVER_DISPLAY_TIME 

    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.current_scene = PLAY_SCENE
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE

            
    def update_play_scene(self):\
    # Fungsi update stones
        if self.is_collision:
            if self.game_over_display_timer > 0:
                 self.game_over_display_timer -= 1
            else:
                self.current_scene = START_SCENE
            return
            
        # Update posisi player
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 12:
            self.player_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT) and self.player_x > -4:
            self.player_x -= 1

        # Generate batu baru
        if pyxel.frame_count % STONE_INTERVAL == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))
        
        # Update posisi batu dan deteksi tabrakan
        for stone in self.stones.copy():
            stone.update()
            
            # Deteksi tabrakan dengan player
            if (self.player_x <= stone.x + 8 and
                stone.x <= self.player_x + 16 and
                self.player_y <= stone.y + 8 and
                stone.y <= self.player_y + 16):
                self.is_collision = True
            
            # Hapus batu yang keluar dari layar
            if stone.y >= SCREEN_HEIGHT:
                self.stones.remove(stone)



    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        if self.current_scene == START_SCENE:
            self.update_start_scene()

        if self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    
    def draw_start_scene(self):
        pyxel.blt(0, 0, 0, 32, 0, 160, 120)
        pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10, 
                   "CLick start", pyxel.COLOR_PINK)
        
    def draw_play_scene(self):
         pyxel.cls(pyxel.COLOR_DARK_BLUE)

        # Gambar semua batu
         for stone in self.stones:
            stone.draw()
        
        # Gambar player
         pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)
        
        # Tampilkan pesan Game Over jika terjadi tabrakan
         if self.is_collision:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "Game Over", pyxel.COLOR_YELLOW)

        # Jika game over, tidak perlu melakukan update
      
    def draw(self):
       if self.current_scene == START_SCENE:
        self.draw_start_scene()

       if self.current_scene == PLAY_SCENE:
        self.draw_play_scene()


# Jalankan program
App()