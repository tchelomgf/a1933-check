input.onButtonPressed(Button.A, function () {
    basic.showNumber(Count)
})
input.onButtonPressed(Button.B, function () {
    Count = 0
    basic.showNumber(Count)
})
let Off = 0
let Stand = 0
let Pulse = 0
let CPUTick = 0
let Volt = 0
let Count = 0
// 1023 / 3.3 * 0.6
let ADCStand = 500
// 1023 / 3.3 * 2
let ADCPulse = 1000
music.setVolume(100)
// basic.showString("A1933 CHECK")
serial.redirectToUSB()
serial.writeLine("")
serial.writeLine("")
serial.writeLine("A1933 CHECK")
pins.analogSetPeriod(AnalogPin.P1, 1000000)
pins.analogWritePin(AnalogPin.P1, 1021)
loops.everyInterval(1000, function () {
    serial.writeString("" + Count + " : " + Volt + " : ")
    serial.writeLine("" + Math.imul(input.runningTime() / CPUTick * 1000, 1) + "us")
})
control.inBackground(function () {
    while (true) {
        for (let index = 0; index < 1000; index++) {
            Volt = pins.analogReadPin(AnalogPin.P0)
            CPUTick += 1
            if (Volt > ADCPulse) {
                Pulse += 1
                Count += 1
            } else if (Volt > ADCStand) {
                Stand += 1
            } else {
                Off += 1
            }
        }
        basic.pause(0)
    }
})
loops.everyInterval(400, function () {
    if (Pulse > 0) {
        Pulse = 0
        music.playTone(988, music.beat(BeatFraction.Sixteenth))
        led.toggle(1, 1)
    } else if (Stand > Off) {
        if (Off > 0) {
            Off = 0
            basic.showIcon(IconNames.Happy)
            soundExpression.hello.play()
            Stand = 0
        }
    } else if (Off > Stand) {
        if (Stand > 0) {
            Stand = 0
            basic.showIcon(IconNames.Yes)
            soundExpression.yawn.play()
        } else {
            basic.clearScreen()
            music.stopAllSounds()
            Off = 0
        }
    }

})
