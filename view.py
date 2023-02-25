# from textual.app import App
# from textual import events
import time

from controller import Controller

# class MyView(App):
#     COLORS = [
#         "white",
#         "maroon",
#         "red",
#         "purple",
#         "fuchsia",
#         "olive",
#         "yellow",
#         "navy",
#         "teal",
#         "aqua",
#     ]

#     def on_mount(self) -> None:
#         self.screen.styles.background = "darkblue"


# if __name__ == "__main__":
#     app = MyView()
#     app.run()

if __name__ == "__main__":
    controller = Controller("virtual")

    # wait for ctrl-c
    try:
        while True:
            data = controller.readSerial()
            if data:
                controller.processData(data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
