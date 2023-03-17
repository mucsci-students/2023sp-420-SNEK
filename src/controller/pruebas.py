# import sys,tty,os,termios
# def getKey():
#     old_settings = termios.tcgetattr(sys.stdin)
#     tty.setcbreak(sys.stdin.fileno())
#     try:
#         while True:
#             b = os.read(sys.stdin.fileno(), 3).decode()
#             if len(b) == 3:
#                 k = ord(b[2])
#             else:
#                 k = ord(b)
#             key_mapping = {
#                 127: 'backspace',
#                 10: 'return',
#                 32: 'space',
#                 9: 'tab',
#                 27: 'esc',
#                 65: 'up',
#                 66: 'down',
#                 67: 'right',
#                 68: 'left'
#             }
#             return key_mapping.get(k, chr(k))
#     finally:
#         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
# try:
#     while True:
#         k = getKey()
#         if k == 'esc':
#             quit()
#         else:
#             print(k)
# except (KeyboardInterrupt, SystemExit):
#     os.system('stty sane')
#     print('stopping.')


# from pynput import keyboard

# def on_press(key):
#     try:
#         print('alphanumeric key {0} pressed'.format(
#             key.char))
#     except AttributeError:
#         print('special key {0} pressed'.format(
#             key))

# def on_release(key):
#     print('{0} released'.format(
#         key))
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False

# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join() 









from pynput import keyboard

def on_activate_a():
    print('A pressed')

def on_activate_b():
    print('B pressed')

def on_activate_c():
    print('C pressed')

def quit():
    print('QUIT')
    h.stop()

with keyboard.GlobalHotKeys({
        '<up>': on_activate_a,
        'b': on_activate_b,
        'c': on_activate_c,
        '<ctrl>+c': quit}) as h:
    h.join()