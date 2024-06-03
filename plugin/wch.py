import pyautogui
from pygetwindow import getAllWindows, PyGetWindowException
from flowlauncher import FlowLauncher


class WindowCenteringHelper(FlowLauncher):
    ICON_PATH = "Images/app.png"
    query_results = []

    def query(self, query) -> list:
        title, size = self.parseQuery(query)
        self.searchWindow(title, size)
        return self.query_results

    def addMessage(self, title: str, method: str = "", parameters: str = "", subtitle: str = "", score: int = 0) -> None:
        self.query_results.append(
            {
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath": self.ICON_PATH,
                "ContextData": [],
                "JsonRPCAction": {
                    "method": method,
                    "parameters": [parameters]
                },
                "score": score
            }
        )

    def searchWindow(self, title: str, size: int | str, subtitle: str = "", score: int = 0) -> None:
        for window in getAllWindows():
            if window.title:
                if not window.isMaximized and not window.isMinimized and window.visible:
                    if title.lower() in window.title.lower():
                        self.addMessage(title=f"{window.title} {size}",
                                        method="centeringWindow",
                                        parameters=[
                                            window._hWnd, size],
                                        subtitle=subtitle,
                                        score=score
                                        )

    def resizeWindow(self, window, percent: int) -> None:
        screen_width, screen_height = pyautogui.size()
        new_width = int(screen_width/100*percent)
        new_height = int(screen_height/100*percent)
        try:
            window.resizeTo(new_width, new_height)
        except PyGetWindowException:
            pass

    def centeringWindow(self, args: list) -> None:
        for window in getAllWindows():
            if window._hWnd == args[0]:
                try:
                    if args[1]:
                        self.resizeWindow(window, int(args[1]))
                    screen_width, screen_height = pyautogui.size()
                    new_win_x, new_win_y = (
                        (screen_width - window.width) / 2), ((screen_height - window.height) / 2)
                    window.moveTo(int(new_win_x), int(new_win_y))
                except PyGetWindowException:
                    pass

    def parseQuery(self, query: str) -> list:
        if len(query.split()) > 1:
            if query.rsplit(None, 1)[-1].isdigit():
                title, size = query.rsplit(None, 1)
                size = max(20, min(int(size), 100))
            else:
                title = query
                size = ""
        else:
            title = query
            size = ""
        return title, size
