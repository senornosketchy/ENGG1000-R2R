def beepingflashing():
        import time
        while not btn.any()
            Sound.tone([(1000, 500, 500)] * 20)
        	Leds.set_color(Leds.RIGHT, Leds.RED)
            Leds.set_color(Leds.LEFT, Leds.RED)
            time.sleep(1)
            Leds.set_color(Leds.RIGHT, Leds.GREEN)
            Leds.set_color(Leds.LEFT, Leds.GREEN)
            time.sleep(1)
