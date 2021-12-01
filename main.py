def Reject():
    global State, Off
    basic.show_icon(IconNames.NO)
    soundExpression.sad.play()
    State = stRejected
    Off = 0

def on_button_pressed_a():
    control.reset()
input.on_button_pressed(Button.A, on_button_pressed_a)

def CleartoIdle():
    global Off, Count, Pulse, Stand, State
    basic.clear_screen()
    music.stop_all_sounds()
    Off = 0
    Count = 0
    Pulse = 0
    Stand = 0
    State = stIdle
def Approve():
    global State, Off
    basic.show_icon(IconNames.YES)
    soundExpression.spring.play()
    State = stApproved
    Off = 0
def CheckPulse():
    global Pulse
    if Pulse > 0:
        Pulse = 0
        music.play_tone(988, music.beat(BeatFraction.SIXTEENTH))
        if State != stApproved:
            led.toggle(1, 1)
StateTime = 0
CPUTick = 0
Volt = 0
Stand = 0
Pulse = 0
Count = 0
Off = 0
State = 0
stRejected = 0
stApproved = 0
stIdle = 0
stIdle = 0
stPlugged = 1
stPulsing = 2
stApproved = 3
stRejected = 4
State = 0
ADCStand = 1023 / 3.3 * 0.09
ADCPulse = 1023 / 3.3 * 0.42
music.set_volume(255)
soundExpression.yawn.play()
basic.show_string("A1933 CHECK")
serial.redirect_to_usb()
serial.write_line("")
serial.write_line("")
serial.write_line("A1933 CHECK")

def on_every_interval():
    serial.write_string("Count:" + ("" + str(Count)) + " Volt:" + ("" + str(Volt)) + " State:" + ("" + str(State)))
    serial.write_line(" CPU:" + ("" + str(Math.imul(input.running_time() / CPUTick * 1000, 1))) + "us")
loops.every_interval(1000, on_every_interval)

def on_every_interval2():
    global Stand, State, StateTime, Pulse, Off, Count
    if State == stIdle:
        if Stand > 50:
            basic.show_icon(IconNames.HAPPY)
            soundExpression.hello.play()
            Stand = 0
            State = stPlugged
            StateTime = input.running_time()
        Pulse = 0
        Off = 0
    elif State == stPlugged:
        if Off > 1000:
            Reject()
            Off = 0
        elif Pulse > 50:
            Pulse = 0
            Count = 0
            State = stPulsing
            StateTime = input.running_time()
        elif input.running_time() - StateTime > 10000:
            Reject()
        Stand = 0
    elif State == stPulsing:
        CheckPulse()
        if input.running_time() - StateTime > 8000:
            if Count < 50000 and Pulse == 0:
                Reject()
            else:
                Approve()
    elif State == stApproved:
        CheckPulse()
        if Off > 50:
            CleartoIdle()
    elif State == stRejected:
        if Off > 50:
            CleartoIdle()
loops.every_interval(350, on_every_interval2)

def on_in_background():
    global Volt, CPUTick, Pulse, Count, Stand, Off
    while True:
        for index in range(1000):
            Volt = pins.analog_read_pin(AnalogPin.P0)
            CPUTick += 1
            if Volt > ADCPulse:
                Pulse += 1
                Count += 1
            elif Volt > ADCStand:
                Stand += 1
            else:
                Off += 1
        basic.pause(0)
control.in_background(on_in_background)
