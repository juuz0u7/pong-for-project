from Settings import *
class Button:
    def __init__(self, x, y, width, height, image, onclickFunction=None, is_lvl=False, action=None):
        self.buttonSurf = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.image = pygame.transform.scale(image, (width // 2, height // 1.2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.action = action

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)


        self.alreadyPressed = False
        if is_lvl:
            objects_lvl.append(self)
        else:
            objects.append(self)

    def process(self):
        global START_game, button_time
        mousePos = pygame.mouse.get_pos()  # (x, y)

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                START_game = pygame.time.get_ticks()

                if not self.alreadyPressed and START_game - button_time > 650:
                    self.onclickFunction()
                    button_time = pygame.time.get_ticks()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False


        screen.blit(self.buttonSurface, self.buttonRect)
