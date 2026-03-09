from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import time
import threading
from utils import format_time, print_progress


@dataclass
class Song:
    name: str
    timestamp: int
    singer: str


@dataclass
class IDevices(ABC):
    lapsed_time: int = 0

    @abstractmethod
    def play(self, song: Song): ...

    @abstractmethod
    def pause(self): ...


@dataclass
class BluetoothSpeaker(IDevices):
    def play(self, song):
        print(f"Playing song {song.name} using bluetooth Speaker")

    def pause(self):
        print("Bluetooth speaker paused")


@dataclass
class WiredSpeaker(IDevices):
    def play(self, song):
        print(f"Playing song {song.name} using wired Speaker")

    def pause(self):
        print("Wired speaker paused")


@dataclass
class PlaybackManager:
    devices: list[IDevices] = field(default_factory=list)
    curr_song: Song | None = None
    lapsed_time: int = 0
    is_playing: bool = False
    _play_thread: threading.Thread | None = None
    _stop_event: threading.Event = field(default_factory=threading.Event)
    _pause_event: threading.Event = field(default_factory=threading.Event)

    def add_devices(self, device: IDevices) -> None:
        self.devices.append(device)

    def play_song(self, song: Song) -> None:
        """Start playback in a background thread and return immediately.

        Use `pause()` to pause and `resume()` to continue. Call
        `wait_for_completion()` to block until the song finishes.
        """
        if self._play_thread and self._play_thread.is_alive():
            print("A song is already playing. Stop or wait for it to finish first.")
            return

        self.curr_song = song
        self.lapsed_time = 0
        self.is_playing = True
        self._stop_event.clear()
        self._pause_event.clear()

        def _playback_loop():
            # Notify devices that playback started
            for device in self.devices:
                device.play(song)

            total = song.timestamp
            print(f"Started playing '{song.name}' ({format_time(total)})")

            try:
                while self.lapsed_time < total and not self._stop_event.is_set():
                    if self._pause_event.is_set():
                        time.sleep(0.1)
                        continue

                    time.sleep(1)
                    self.lapsed_time += 1
                    print_progress(self.lapsed_time, total)

                if self.lapsed_time >= total:
                    print()
                    print(f"Song '{song.name}' completed.")
            finally:
                self.curr_song = None
                self.is_playing = False
                self._play_thread = None
                self._stop_event.clear()
                self._pause_event.clear()

        self._play_thread = threading.Thread(target=_playback_loop, daemon=True)
        self._play_thread.start()

    def pause(self) -> None:
        """Pause playback; can be resumed with `resume()`."""
        if not self._play_thread or not self._play_thread.is_alive():
            print("No active playback to pause.")
            return
        if self._pause_event.is_set():
            print("Playback already paused.")
            return
        self._pause_event.set()
        self.is_playing = False
        for device in self.devices:
            try:
                device.pause()
            except Exception:
                pass
        print(f"Paused at {format_time(self.lapsed_time)}")

    def resume(self) -> None:
        """Resume playback if paused."""
        if not self._play_thread or not self._play_thread.is_alive():
            print("No paused playback to resume.")
            return
        if not self._pause_event.is_set():
            print("Playback is not paused.")
            return
        self._pause_event.clear()
        self.is_playing = True
        print(f"Resumed '{self.curr_song.name}' at {format_time(self.lapsed_time)}")

    def wait_for_completion(self) -> None:
        """Block until current playback thread finishes."""
        if self._play_thread:
            self._play_thread.join()


if __name__ == "__main__":
    song1 = Song(name="Blinding Lights", timestamp=10, singer="The Weeknd")
    song2 = Song(name="Shape of You", timestamp=24, singer="Ed Sheeran")
    song3 = Song(name="Levitating", timestamp=33, singer="Dua Lipa")

    bluetooth_speaker = BluetoothSpeaker()
    wired_speaker = WiredSpeaker()

    playback_manager = PlaybackManager()

    playback_manager.add_devices(bluetooth_speaker)
    playback_manager.add_devices(wired_speaker)

    playback_manager.play_song(song1)
    # demo: pause after 3 seconds, resume after 2 seconds, then wait
    time.sleep(3)
    playback_manager.pause()
    time.sleep(2)
    playback_manager.resume()
    playback_manager.wait_for_completion()
