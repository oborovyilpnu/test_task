from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class TimerWidget(BoxLayout):
    current_time = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 50

        self.input = TextInput(
            hint_text='Enter seconds (0-300)',
            input_filter='int',
            multiline=False,
            font_size=30
        )
        self.input.bind(text=self.validate_input)
        self.add_widget(self.input)

        self.start_btn = Button(
            text='Start Countdown',
            size_hint=(1, 0.3),
            font_size=25
        )
        self.start_btn.bind(on_press=self.start_timer)
        self.add_widget(self.start_btn)

        self.timer_label = Label(
            text='0.0',
            font_size=60,
            bold=True
        )
        self.add_widget(self.timer_label)

    def validate_input(self, instance, value):
        try:
            num = int(value) if value else 0
            if num > 300:
                instance.text = '300'
            elif num < 0:
                instance.text = '0'
        except ValueError:
            instance.text = ''

    def start_timer(self, instance):
        if self.input.text.isdigit():
            self.current_time = int(self.input.text)
            self.start_btn.disabled = True
            Clock.schedule_interval(self.update_timer, 0.1)

    def update_timer(self, dt):
        self.current_time -= 0.1
        if self.current_time <= 0:
            self.current_time = 0
            Clock.unschedule(self.update_timer)
            self.start_btn.disabled = False

    def on_current_time(self, instance, value):
        self.timer_label.text = f'{max(value, 0):.1f}'


class TimerApp(App):
    def build(self):
        return TimerWidget()


if __name__ == '__main__':
    TimerApp().run()
