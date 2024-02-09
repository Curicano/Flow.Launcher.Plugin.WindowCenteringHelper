from pyautogui import size
from pygetwindow import getAllWindows, PyGetWindowException
from flowlauncher import FlowLauncher


# import logging
# logging.basicConfig(filename="log.log",
#                     filemode="a",
#                     level=logging.INFO,
#                     encoding="utf-8",
#                     format="%(asctime)s - %(levelname)s - %(message)s")


class WindowCenteringHelper(FlowLauncher):
    ICON_PATH = "Images/app.png"
    query_results = []

    def query(self, query) -> list:
        self.getAllWindows(query)
        return self.query_results

    def addMessage(self, title: str, method: str = "", parameters: str = "", subtitle: str = "") -> None:
        self.query_results.append(
            {
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath": self.ICON_PATH,
                "ContextData": [parameters, True],
                "JsonRPCAction": {
                    "method": method,
                    "parameters": [parameters]
                },
                "score": 0
            }
        )

    def getAllWindows(self, query: str) -> None:
        if len(query.split()) > 1:
            if query.rsplit(None, 1)[-1].isdigit():
                title, size = query.rsplit(None, 1)
                if int(size) > 100:
                    size = 100
                elif int(size) < 20:
                    size = 20
            else:
                title = query
                size = None
        else:
            title = query
            size = None
        all_windows = getAllWindows()
        for window in all_windows:
            if window.title:
                if not window.isMaximized:
                    if not window.isMinimized:
                        if window.visible:
                            if title.lower() in window.title.lower():
                                self.addMessage(title=f"{window.title} {size if size else ''}",
                                                method="centeringWindow",
                                                parameters=[
                                                    window._hWnd, size]
                                                )

    def resizeWindow(self, window, percent: int) -> None:
        screen_width, screen_height = size()
        new_width = int(screen_width/100*percent)
        new_height = int(screen_height/100*percent)
        try:
            window.resizeTo(new_width, new_height)
        except PyGetWindowException:
            pass

    def centeringWindow(self, args: list) -> None:
        all_windows = getAllWindows()
        for window in all_windows:
            if window._hWnd == args[0]:
                if args[1]:
                    self.resizeWindow(window, int(args[1]))
                screen_width, screen_height = size()
                new_win_x, new_win_y = (
                    (screen_width - window.width) / 2), ((screen_height - window.height) / 2)
                try:
                    window.moveTo(int(new_win_x), int(new_win_y))
                except PyGetWindowException:
                    pass
