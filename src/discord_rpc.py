from pypresence import Presence
import psutil
import sys
import time

# get cpu usage in percentage_%
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# get used physical memory in GB
def get_mem_usage():
    memory = psutil.virtual_memory()
    return round(memory.used / (1024 ** 3), 2)

# get system uptime
def get_system_uptime():
    # get current time and minus with boot time to get total uptime
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_minutes = int(uptime_seconds / 60)
    uptime_hours = int(uptime_minutes / 60)

    if uptime_hours == 0:
        formatted_uptime = f"{uptime_minutes % 60} minutes"
    else:
        formatted_uptime = f"{uptime_hours % 24} hours, {uptime_minutes % 60} minutes"
    return formatted_uptime

# update application rpc
def update_presence(client_id, details, state, large_image, small_image):
    rpc = Presence(client_id)
    rpc.connect()

    try:
        while True:

            # Set up Rich Presence information
            presence_details = {"details": details.format(cpu_usage=get_cpu_usage(), mem_usage=get_mem_usage())}
            presence_state = {"state": state.format(get_system_uptime())}

            # Clear previous presence before updating
            rpc.clear()

            # Update the presence
            rpc.update(large_image=large_image, small_image=small_image, **presence_details, **presence_state)

            # Wait for some time before updating again
            time.sleep(15)  # You can adjust the time interval (in seconds) for updating the presence

    except KeyboardInterrupt:
        rpc.close()

    except Exception as e:
        rpc.close()
        # exit quietly
        sys.exit(0)

# only runs when executed as main script
if __name__ == "__main__":

    client_id = 'YOUR_CLIENT_ID'
    details = "CPU: {cpu_usage:.1f}%, RAM: {mem_usage:.2f} GB"
    state = "Uptime: {}"
    large_image = "YOUR_LARGE_IMAGE_NAME"
    small_image = "YOUR_SMALL_IMAGE_NAME"

    update_presence(client_id, details, state, large_image, small_image)
