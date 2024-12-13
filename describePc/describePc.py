import platform
import psutil
import subprocess


def get_system_info():
    info = {}

    # Operating System Information
    info['OS'] = platform.system()
    info['OS Version'] = platform.version()
    info['OS Release'] = platform.release()

    # CPU Information
    info['CPU'] = platform.processor()
    info['CPU Cores (Physical)'] = psutil.cpu_count(logical=False)
    info['CPU Cores (Logical)'] = psutil.cpu_count(logical=True)
    info['CPU Frequency'] = psutil.cpu_freq().current

    # RAM Information
    virtual_memory = psutil.virtual_memory()
    info['Total RAM'] = virtual_memory.total
    info['Available RAM'] = virtual_memory.available
    info['Used RAM'] = virtual_memory.used
    info['RAM Usage Percentage'] = virtual_memory.percent

    # Disk Information
    info['Disks'] = []
    for partition in psutil.disk_partitions():
        disk_info = {
            'Device': partition.device,
            'Mountpoint': partition.mountpoint,
            'File System Type': partition.fstype
        }
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info['Total Size'] = usage.total
            disk_info['Used'] = usage.used
            disk_info['Free'] = usage.free
            disk_info['Usage Percentage'] = usage.percent
        except PermissionError:
            # This case can occur on some systems where access is restricted
            disk_info['Total Size'] = 'N/A'
            disk_info['Used'] = 'N/A'
            disk_info['Free'] = 'N/A'
            disk_info['Usage Percentage'] = 'N/A'
        info['Disks'].append(disk_info)

    # Peripheral Information
    try:
        lspci_output = subprocess.check_output(['lspci'], universal_newlines=True)
        info['Peripherals'] = lspci_output.strip().split('\n')
    except FileNotFoundError:
        info['Peripherals'] = 'lspci command not found. This may not be a Linux system.'

    return info


def print_system_info(info):
    print("System Information:")
    print(f"Operating System: {info['OS']} {info['OS Version']} ({info['OS Release']})")
    print(f"CPU: {info['CPU']}")
    print(f"CPU Cores (Physical): {info['CPU Cores (Physical)']}")
    print(f"CPU Cores (Logical): {info['CPU Cores (Logical)']}")
    print(f"CPU Frequency: {info['CPU Frequency']} MHz")
    print(f"Total RAM: {info['Total RAM'] / (1024 ** 3):.2f} GB")
    print(f"Available RAM: {info['Available RAM'] / (1024 ** 3):.2f} GB")
    print(f"Used RAM: {info['Used RAM'] / (1024 ** 3):.2f} GB")
    print(f"RAM Usage Percentage: {info['RAM Usage Percentage']}%")

    print("Disks:")
    for disk in info['Disks']:
        print(f"  Device: {disk['Device']}")
        print(f"  Mountpoint: {disk['Mountpoint']}")
        print(f"  File System Type: {disk['File System Type']}")
        print(f"  Total Size: {disk['Total Size'] / (1024 ** 3):.2f} GB" if disk[
                                                                                'Total Size'] != 'N/A' else "  Total Size: N/A")
        print(f"  Used: {disk['Used'] / (1024 ** 3):.2f} GB" if disk['Used'] != 'N/A' else "  Used: N/A")
        print(f"  Free: {disk['Free'] / (1024 ** 3):.2f} GB" if disk['Free'] != 'N/A' else "  Free: N/A")
        print(f"  Usage Percentage: {disk['Usage Percentage']}%" if disk[
                                                                        'Usage Percentage'] != 'N/A' else "  Usage Percentage: N/A")

    print("Peripherals:")
    if isinstance(info['Peripherals'], list):
        for peripheral in info['Peripherals']:
            print(f"  {peripheral}")
    else:
        print(f"  {info['Peripherals']}")


if __name__ == "__main__":
    system_info = get_system_info()
    print_system_info(system_info)
