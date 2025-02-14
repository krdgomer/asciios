import curses
import subprocess
import yt_dlp
import time
from youtube_search import YoutubeSearch

def search_youtube(query):
    """ YouTube üzerinde arama yapar ve ilk 10 sonucu döndürür. """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch10',
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = YoutubeSearch(query, max_results=10).to_dict()
        return [(entry['title'], entry['id']) for entry in info]

def play_video(video_url, resolution="144p"):
    """ Use yt_dlp to fetch the direct URL and play it in VLC. """
    # Fetch the direct video URL using yt_dlp
    ydl_opts = {
        'format': f'bv[height<={resolution}]+ba',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_url}", download=False)
        direct_url = info['url']  # Get the direct video URL

    # Play the video in VLC
    subprocess.Popen([
        "vlc",
        "-f",  # Fullscreen
        "--loop",  # Loop the video
        "--no-video-title",  # Hide the video title
        direct_url  # Direct video URL
    ])

def curses_menu(stdscr):
    curses.curs_set(0)  # İmleci gizle
    stdscr.clear()
    stdscr.refresh()
    
    stdscr.addstr(2, 2, "YouTube Araması: ", curses.A_BOLD)
    stdscr.refresh()
    
    # Kullanıcıdan arama terimini al
    curses.echo()
    search_query = stdscr.getstr(3, 2, 50).decode("utf-8")
    curses.noecho()
    
    # YouTube'dan sonuçları çek
    results = search_youtube(search_query)
    
    if not results:
        stdscr.addstr(5, 2, "Sonuç bulunamadı!", curses.A_BOLD)
        stdscr.refresh()
        time.sleep(2)
        return
    
    selected = 0
    
    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "YouTube Sonuçları (Yön Tuşları + Enter)", curses.A_BOLD)

        # Sonuçları ekrana yazdır
        for idx, (title, _) in enumerate(results):
            if idx == selected:
                stdscr.addstr(3 + idx, 2, f"> {title}", curses.A_REVERSE)
            else:
                stdscr.addstr(3 + idx, 2, title)
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_DOWN and selected < len(results) - 1:
            selected += 1
        elif key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == 10:  # Enter tuşu
            video_url = results[selected][1]
            curses.endwin()
            play_video(video_url)
            break

if __name__ == "__main__":
    curses.wrapper(curses_menu)
