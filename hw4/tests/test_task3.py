import pytest
import subprocess
from pathlib import Path
import time
from datetime import datetime


def test_process_communication(tmp_path):
    artifact_file = Path("tests/data/task3/artifact.txt")
    artifact_file.parent.mkdir(parents=True, exist_ok=True)

    proc = subprocess.Popen(
        ["python", "-c", "from hw4.task3 import main_process; main_process()"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    test_messages = ["Hello World", "TEST Message", "Python ROT13", "exit"]

    with open(artifact_file, "w") as log_file:
        for msg in test_messages:
            output_lines = []
            start_time = time.time()
            while time.time() - start_time < 10:
                line = proc.stdout.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                output_lines.append(line.strip())
                log_file.write(f"{line.strip()}\n")

                if "Введите сообщение" in line:
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")
                    proc.stdin.write(f"{msg}\n")
                    proc.stdin.flush()
                    log_file.write(f"[{timestamp}] User input: {msg}\n")
                    continue

                if "Main received from B:" in line:
                    break

            if msg.lower() == "exit":
                break

    time.sleep(1)
    proc.terminate()

    assert artifact_file.exists()
    print("\nАртефакт взаимодействия:")
    print(artifact_file.read_text())
