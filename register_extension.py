import winreg
import os
import sys
import shutil

def register_file_type():
    file_ext = '.bpc'
    file_type = 'Backpack Calculator'
    file_desc = 'Backpack Calculator Datafile'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Используем путь к текущему исполняемому файлу
    program_path = f'"{sys.executable}" "{os.path.join(current_dir, "backpack_gui.py")}" "%1"'
    icon_path = os.path.join(current_dir, "icon_calc.png")

    try:
        # Register file extension
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_ext}")
        winreg.SetValue(key, "", winreg.REG_SZ, file_type)
        winreg.CloseKey(key)

        # Register file type
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}")
        winreg.SetValue(key, "", winreg.REG_SZ, file_desc)
        winreg.CloseKey(key)

        # Register icon
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\DefaultIcon")
        winreg.SetValue(key, "", winreg.REG_SZ, icon_path)
        winreg.CloseKey(key)

        # Register command
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\shell\\open\\command")
        winreg.SetValue(key, "", winreg.REG_SZ, program_path)
        winreg.CloseKey(key)

        print("File association registered successfully!")
        return True
    except Exception as e:
        print(f"Error registering file association: {str(e)}")
        return False

if __name__ == "__main__":
    register_file_type()