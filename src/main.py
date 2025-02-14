import curses
from youtube import curses_menu

# Menu options
menu = ["WhatsApp", "YouTube", "Settings", "Exit"]

def draw_menu(stdscr, selected_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    title = "ASCIIOS - Terminal Interface"
    stdscr.addstr(1, w//2 - len(title)//2, title, curses.A_BOLD)

    for idx, item in enumerate(menu):
        x = w//2 - len(item)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item)

    stdscr.refresh()

def main(stdscr):
    # Setup colors
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Selected item color

    selected_idx = 0

    while True:
        draw_menu(stdscr, selected_idx)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(menu) - 1:
            selected_idx += 1
        elif key == ord("\n"):  # Enter key
            if menu[selected_idx] == "Exit":
                break
            else:
                stdscr.clear()
                msg = f"Opening {menu[selected_idx]}..."
                stdscr.addstr(curses.LINES//2, curses.COLS//2 - len(msg)//2, msg)
                stdscr.refresh()
                curses.napms(1000)  # Simulate loading
                if menu[selected_idx] == "YouTube":
                    curses.wrapper(curses_menu)
        elif key == 27:  # ESC key to exit
            break

curses.wrapper(main)
