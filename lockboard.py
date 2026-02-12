import pygame
import threading
from evdev import InputDevice, categorize, ecodes

# CHANGE THESE TO YOUR /DEV/INPUT/EVENT PATHS
keyboard = InputDevice('/dev/input/event4')
mouse = InputDevice('/dev/input/event8')

pressed_keys = set()
mouse_buttons = set()
scroll_buttons = set()
scroll_amount = 0


def listen_device(device):
    global scroll_amount

    for event in device.read_loop():

        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            key_names = key_event.keycode

            # keycode can be string, list, or tuple
            if not isinstance(key_names, (list, tuple)):
                key_names = [key_names]

            for key_name in key_names:

                if key_name.startswith("BTN_"):
                    if key_event.keystate == key_event.key_down:
                        mouse_buttons.add(key_name)
                    elif key_event.keystate == key_event.key_up:
                        mouse_buttons.discard(key_name)
                else:
                    if key_event.keystate == key_event.key_down:
                        pressed_keys.add(key_name)
                    elif key_event.keystate == key_event.key_up:
                        pressed_keys.discard(key_name)
        elif event.type == ecodes.EV_REL:
            if event.code == ecodes.REL_WHEEL:
                if event.value > 0:
                    scroll_buttons.add("SCROLL_UP")
                elif event.value < 0:
                    scroll_buttons.add("SCROLL_DOWN")




threading.Thread(target=listen_device, args=(keyboard,), daemon=True).start()
threading.Thread(target=listen_device, args=(mouse,), daemon=True).start()


KEY_LAYOUT = {
    'KEY_W': (70, 10, 60, 60),
    'KEY_A': (10, 80, 60, 60),
    'KEY_S': (80, 80, 60, 60),
    'KEY_D': (150, 80, 60, 60),
    'KEY_F': (220, 80, 60, 60),
    'KEY_SPACE': (150, 150, 130, 60),
    'KEY_LEFTSHIFT': (10, 150, 130, 60),
}

mouse_layout = {
    "BTN_LEFT": (300, 60, 60, 130),
    "BTN_RIGHT": (400, 60, 60, 130),
    "SCROLL_UP": (370, 60, 20, 60),
    "SCROLL_DOWN": (370, 130, 20, 60),
}


pygame.init()
screen = pygame.display.set_mode((500, 250))
pygame.display.set_caption("lockboard")
font = pygame.font.SysFont(None, 32)
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    for key, (x, y, w, h) in KEY_LAYOUT.items():
        color = (0, 200, 0) if key in pressed_keys else (180, 180, 180)
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=5)
        label = font.render(key.replace('KEY_', ''), True, (0, 0, 0))
        label_rect = label.get_rect(center=(x + w//2, y + h//2))
        screen.blit(label, label_rect)

    for btn, (x, y, w, h) in mouse_layout.items():
        active = btn in mouse_buttons or btn in scroll_buttons
        color = (0, 200, 0) if active else (180, 180, 180)
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=5)

        label = font.render(btn.replace("BTN_", "").replace("SCROLL_", ""), True, (0, 0, 0))
        label_rect = label.get_rect(center=(x + w//2, y + h//2))
        screen.blit(label, label_rect)

    scroll_amount *= 0.8
    if abs(scroll_amount) < 0.1:
        scroll_amount = 0

    if "SCROLL_UP" in scroll_buttons:
        scroll_buttons.discard("SCROLL_UP")

    if "SCROLL_DOWN" in scroll_buttons:
        scroll_buttons.discard("SCROLL_DOWN")


    pygame.display.flip()
    pygame.time.delay(10)
