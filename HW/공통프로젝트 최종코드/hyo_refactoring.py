import cv2
import threading
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

class WeatherDisplay:

    def __init__(self):
        self.test = 0
        self.idx = 0
        self.wflag = 0

        self.get_msg = ""
        self.get_msg2 = "===="
        self.data = ["", 1.0, 2.0, 3.0, 4.0, 5, 6]
        self.category = 0
        self.info_temp = ""
        self.info_snow = ""
        self.info_rain = ""
        self.info_cloud = ""

        self.fontpath = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        self.color = (255, 255, 255, 0)
        
        self.capture = [[], [], [], []]

        self.emotion_gif = [
            "emotion/angry.gif",
            "emotion/disgusted.gif",
            "emotion/fearful.gif",
            "emotion/happy.gif",
            "emotion/neutral.gif",
            "emotion/sad.gif",
            "emotion/surprised.gif"
        ]

        self.weather_gif = [
            "weather/clear.gif",
            "weather/cloudy.gif",
            "weather/rain.gif",
            "weather/snow.gif",
            "weather/thunderstorm.gif"
        ]

        # capture init
        self.init_captures()

        # Start threads
        self.t = threading.Thread(target=self.ttq)
        self.t.start()
        self.t.demon = True

        self.t2 = threading.Thread(target=self.ttq2)
        self.t2.start()
        self.t2.demon = True

    def init_captures(self):
        for i in range(len(self.emotion_gif)):
            self.capture[0].append(cv2.VideoCapture(self.emotion_gif[i]))
        for i in range(11):
            self.capture[1].append(cv2.VideoCapture("sign/sign{}.gif".format(i)))
            self.capture[2].append(cv2.VideoCapture("sign/sign{}.gif".format(i)))
        for i in range(len(self.weather_gif)):
            self.capture[3].append(cv2.VideoCapture(self.weather_gif[i]))

    def CV2PIL(self, frame):
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def PIL2CV(self, pil_image):
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def what_day_is_today(self):
        return ["월", "화", "수", "목", "금", "토", "일"][datetime.today().weekday()] + "요일"

    def touchScreen(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.category += 1
            if self.category > 3:
                self.category = 0

    def ttq(self):
        while True:
            self.get_msg = input()

    def ttq2(self):
        while True:
            self.get_msg2 = input()

    def run(self):
        while True:
            keyCode = cv2.waitKey(77)
            if keyCode < 0:  # input None
                if self.capture[self.category][self.idx].get(cv2.CAP_PROP_POS_FRAMES) == self.capture[self.category][self.idx].get(cv2.CAP_PROP_FRAME_COUNT):
                    self.capture[self.category][self.idx].set(cv2.CAP_PROP_POS_FRAMES, 0)

                ret, frame = self.capture[self.category][self.idx].read()

                cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                if self.category == 3:
                    self.info_temp = "온도: " + self.info_temp
                    if self.info_rain == "강수없음":
                        self.info_rain = "강수: 없음"
                    else:
                        self.info_rain = "강수: " + self.info_rain
                    if self.info_snow == "적설없음":
                        self.info_snow = "적설: 없음"
                    else:
                        self.info_snow = "적설: " + self.info_snow
                    if self.info_cloud == "1":
                        self.info_cloud = "날씨: 맑음"
                    elif self.info_cloud == "3":
                        self.info_cloud = "날씨: 구름많음"
                    elif self.info_cloud == "4":
                        self.info_cloud = "날씨: 흐림"

                    now = datetime.now()
                    pil_image = self.CV2PIL(frame)
                    draw = ImageDraw.Draw(pil_image, 'RGBA')

                    font_kr = ImageFont.truetype(self.fontpath, 50)
                    draw.text((130, 370), now.strftime('%H:%M:%S'), font=font_kr, fill=self.color)
                    font_kr = ImageFont.truetype(self.fontpath, 20)
                    draw.text((175, 430), self.what_day_is_today(), font=font_kr, fill=self.color)

                    font_kr = ImageFont.truetype(self.fontpath, 24)
                    draw.text((570, 355), self.info_rain, font=font_kr, fill=self.color)
                    draw.text((570, 385), self.info_snow, font=font_kr, fill=self.color)
                    draw.text((570, 415), self.info_temp, font=font_kr, fill=self.color)
                    draw.text((570, 445), self.info_cloud, font=font_kr, fill=self.color)

                    cv2_image = self.PIL2CV(pil_image)
                    frame = cv2_image

                cv2.imshow("Image", frame)
                cv2.setMouseCallback("Image", self.touchScreen)

            if keyCode == ord('q'):  # input 'q'
                if self.category <= 2 and self.idx == 1:
                    self.idx = 0
                    continue
                elif self.category <= 2 and self.idx == 0:
                    self.idx = 1
                    continue

            if keyCode == 27:  # input 'esc' -> exit
                break
                 # release Stream
        for i in range(0, len(self.emotion_gif)):
            self.capture[0][i].release()
        for i in range(0, 11):
            self.capture[1][i].release()
        for i in range(0, 11):
            self.capture[2][i].release()

        for i in range(0, len(self.weather_gif)):
            self.capture[3][i].release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    weather_display = WeatherDisplay()
    weather_display.run()
