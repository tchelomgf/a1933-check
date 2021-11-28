function Reject () {
    basic.showIcon(IconNames.No)
    // soundExpression.sad.play()
    State = stRejected
}
input.onButtonPressed(Button.A, function () {
    control.reset()
})
function CleartoIdle () {
    basic.clearScreen()
    music.stopAllSounds()
    Off = 0
    Count = 0
    Pulse = 0
    Stand = 0
    State = stIdle
}
function Approve () {
    basic.showIcon(IconNames.Yes)
    soundExpression.yawn.play()
    State = stApproved
}
function CheckPulse () {
    if (Pulse > 0) {
        Pulse = 0
        music.playTone(988, music.beat(BeatFraction.Sixteenth))
        led.toggle(1, 1)
    }
}
let StateTime = 0
let CPUTick = 0
let Volt = 0
let Stand = 0
let Pulse = 0
let Count = 0
let Off = 0
let State = 0
let stApproved = 0
let stRejected = 0
let stIdle = 0
stIdle = 0
stRejected = 3
stApproved = 4
let stPlugged = 1
let stPulsing = 2
State = stIdle
// 1023 / 3.3 * 0.6
let ADCStand = 300
// 1023 / 3.3 * 2
let ADCPulse = 1000
music.setVolume(100)
// basic.showString("A1933 CHECK")
serial.redirectToUSB()
serial.writeLine("")
serial.writeLine("")
serial.writeLine("A1933 CHECK")
loops.everyInterval(1000, function () {
    serial.writeString("Count:" + Count + " Volt:" + Volt + " State:" + State)
    serial.writeLine(" CPU:" + Math.imul(input.runningTime() / CPUTick * 1000, 1) + "us")
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
    if (State == stIdle) {
        if (Stand > 50) {
            basic.showIcon(IconNames.Happy)
            soundExpression.hello.play()
            Stand = 0
            State = stPlugged
            StateTime = input.runningTime()
        }
        Pulse = 0
        Off = 0
    } else if (State == stPlugged) {
        if (Off > 1000) {
            Reject()
            Off = 0
        } else if (Pulse > 50) {
            Pulse = 0
            Count = 0
            State = stPulsing
            StateTime = input.runningTime()
        } else {
            if (input.runningTime() - StateTime > 5000) {
                Reject()
            }
        }
        Stand = 0
    } else if (State == stPulsing) {
        CheckPulse()
        if (input.runningTime() - StateTime > 5000) {
            if (Count < 1000) {
                Reject()
            } else {
                Approve()
            }
        }
    } else if (State == stApproved) {
        CheckPulse()
        if (Off > 50) {
            CleartoIdle()
        }
    } else if (State == stRejected) {
        if (Off > 50) {
            CleartoIdle()
        }
    }
})
