import asyncio
import main

main.MOTOR_MODE = "DUMMY"
asyncio.run(main.entrypoint())