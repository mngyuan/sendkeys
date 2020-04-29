#! /usr/bin/env python
"""
CLI for sending keyboard events to MacOS apps.

Author: mngyuan
License: MIT
"""

import sys
import Quartz
import fire
from AppKit import NSEvent

pid = 14638

def keyboardTapCallback(proxy, type_, event, refcon):
    keycode = Quartz.CGEventGetIntegerValueField(
        event,
        Quartz.kCGKeyboardEventKeycode
    )
    # Quartz.CGEventType.keyDown doesn't exist?
    if type_ == 10:
        print(keycode)

    dupeEvent = Quartz.CGEventCreateCopy(event);
    Quartz.CGEventSetIntegerValueField(
        dupeEvent,
        Quartz.kCGEventTargetUnixProcessID,
        pid
    )
    Quartz.CGEventPostToPid(pid, dupeEvent)

    return event

def keyHook():
    tap = Quartz.CGEventTapCreate(
        Quartz.kCGHIDEventTap,
        Quartz.kCGHeadInsertEventTap,
        Quartz.kCGEventTapOptionDefault,
        Quartz.kCGEventMaskForAllEvents,
        keyboardTapCallback,
        None
    )

    if tap is None:
        print('failed to create event tap!')
        sys.exit(1)

    runLoopSource = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    Quartz.CFRunLoopAddSource(
        Quartz.CFRunLoopGetCurrent(),
        runLoopSource,
        Quartz.kCFRunLoopDefaultMode
    )

    Quartz.CGEventTapEnable(tap, True)

    Quartz.CFRunLoopRun()

def keyPress(*, pid):
    events = [
        Quartz.CGEventCreateKeyboardEvent(None, 0, True),
        Quartz.CGEventCreateKeyboardEvent(None, 0, False)
    ]
    for event in events:
        Quartz.CGEventPostToPid(pid, event)

if __name__ == "__main__":
    fire.Fire(keyHook)
