def on_button_pressed_a():
    basic.show_number(Count)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global Count
    Count = 0
    basic.show_number(Count)
input.on_button_pressed(Button.B, on_button_pressed_b)

Off = 0
Stand = 0
Pulse = 0
CPUTick = 0
Volt = 0
Count = 0
stIdle = 0
# 1023 / 3.3 * 0.6
ADCStand = 500
# 1023 / 3.3 * 2
ADCPulse = 1000
stPlug = 1
stPulse = 2
stApprove = 3
stReprove = 4
State = stIdle
music.set_volume(100)
# basic.showString("A1933 CHECK")
serial.redirect_to_usb()
serial.write_line("")
serial.write_line("")
serial.write_line("A1933 CHECK")
pins.analog_set_period(AnalogPin.P1, 1000000)
pins.analog_write_pin(AnalogPin.P1, 1021)

def on_every_interval():
    serial.write_string("" + str(Count) + " : " + ("" + str(Volt)) + " : ")
    serial.write_line("" + str(Math.imul(input.running_time() / CPUTick * 1000, 1)) + "us")
loops.every_interval(1000, on_every_interval)

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

def on_every_interval2():
    global Pulse, Off, Stand
    if Pulse > 0:
        Pulse = 0
        music.play_tone(988, music.beat(BeatFraction.SIXTEENTH))
        led.toggle(1, 1)
    elif Stand > Off:
        if Off > 0:
            Off = 0
            basic.show_icon(IconNames.HAPPY)
            soundExpression.hello.play()
            Stand = 0
    elif Off > Stand:
        if Stand > 0:
            Stand = 0
            basic.show_icon(IconNames.YES)
            soundExpression.yawn.play()
        else:
            basic.clear_screen()
            music.stop_all_sounds()
            Off = 0
loops.every_interval(400, on_every_interval2)
