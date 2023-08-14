from pyautogui import size
from pygetwindow import getAllWindows
from flowlauncher import FlowLauncher


class WindowCenteringHelper(FlowLauncher):
    ICON_PATH = "Images/app.png"
    query_results = []

    def query(self, query) -> list:
        self.getAllWindows(query)
        return self.query_results

    def context_menu(self, data):
        return [
            {
                "title": "Place in the center and resize",
                "subTitle": r"80% of the total screen size",
                "icoPath": self.ICON_PATH,
                "jsonRPCAction": {
                    "method": "centeringWindow",
                    "parameters": data
                },
                "score": 0
            }
        ]

    def addMessage(self, title: str, method: str, parameters: str, subtitle: str = "") -> None:
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

    def getAllWindows(self, title: str = "") -> None:
        all_windows = getAllWindows()
        for window in all_windows:
            if window.title:
                if not window.isMaximized:
                    if window.visible:
                        if title.lower() in window.title.lower():
                            self.addMessage(title=f"{window.title} ({window._hWnd})",
                                            method="centeringWindow",
                                            parameters=window._hWnd
                                            )

    def resizeWindow(self, window) -> None:
        screen_width, screen_height = size()
        new_width = int(screen_width/100*80)
        new_height = int(screen_height/100*80)
        window.resizeTo(new_width, new_height)

    def centeringWindow(self, hwnd: str, resize: bool = False) -> None:
        all_windows = getAllWindows()
        for window in all_windows:
            if window._hWnd == hwnd:
                if resize:
                    self.resizeWindow(window)
                screen_width, screen_height = size()
                new_win_x, new_win_y = (
                    (screen_width - window.width) / 2), ((screen_height - window.height) / 2)
                window.moveTo(int(new_win_x), int(new_win_y))
