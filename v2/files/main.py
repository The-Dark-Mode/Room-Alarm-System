import tinytuya
import time
import cv2
import pygame

def play_alarm(d):
    pygame.mixer.init()

    # Load and play alarm sound
    alarm_sound = pygame.mixer.Sound("alarm.mp3")
    alarm_channel = alarm_sound.play(-1)  # Play alarm sound on loop

    # Wait for 1 second (if necessary)
    time.sleep(1)

    # Load and play police siren sound
    siren_sound = pygame.mixer.Sound("Police_Siren.mp3")
    siren_channel = siren_sound.play(-1)  # Play police siren sound on loop

    while True:
        # Turn on device
        turn_on(d)
        time.sleep(1)
        # Turn off device
        turn_off(d)
        time.sleep(1)

        # Check for ESC key
        if cv2.waitKey(1) == 27:
            break

    # Stop all sounds when ESC key is pressed
    alarm_channel.stop()
    siren_channel.stop()

def turn_on(d):
    print("Device turned on")
    d.turn_on()

def turn_off(d):
    print("Device turned off")
    d.turn_off()

def main():
    # Connect to Device
    d = tinytuya.OutletDevice(
        dev_id='id',
        address='private_ipv4',
        local_key='key', 
        version=3.3)

    # Get Status
    data = d.status() 
    print('set_status() result %r' % data)

    print("Activating")
    # Play alarm and control device
    play_alarm(d)

# Initialize the camera
camera = cv2.VideoCapture(0)

# Set up initial frame
_, prev_frame = camera.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

while True:
    # Capture current frame
    _, frame = camera.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)

    # Compute absolute difference between current frame and previous frame
    frame_diff = cv2.absdiff(prev_gray, frame_gray)
    _, frame_diff = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # Count non-zero pixels in the difference image
    motion_pixels = cv2.countNonZero(frame_diff)

    # If motion is detected (adjust threshold as needed)
    if motion_pixels > 1500:
        print("MOTION DETECTED!")
        main()

    # Update previous frame
    prev_gray = frame_gray.copy()

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
camera.release()
cv2.destroyAllWindows()